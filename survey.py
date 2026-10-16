"""Recount what the open-data portals list. Needs the network; build.py does not.

Reads   catalogue/portals.csv
Writes  catalogue/portals.csv   layers_seen only, by the method in catalogue/SCHEMA.md

    python survey.py --count [jurisdiction ...]

surveyed_on is left alone: it dates the last check by hand. A row whose request fails keeps
its old count.
"""

import json
import sys
import threading
import urllib.error
import urllib.parse
import urllib.request
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor

from common import PORTAL_COLS, PORTALS, read_csv, write_csv

USER_AGENT = "ontario-osm-data-sources survey (+https://github.com/skfd/ontario-osm-data-sources)"
PARALLEL = 8
SLOTS = threading.Semaphore(PARALLEL)  # requests in flight, across rows and the services in them


class ServiceError(Exception):
    """The server answered with an error of its own, not a network failure."""


class Secured(ServiceError):
    """The server wants a token: not public, so nothing to count."""


def get_text(url: str) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    for attempt in (1, 2):
        try:
            with SLOTS, urllib.request.urlopen(req, timeout=60) as r:
                body = r.read()
            try:
                return body.decode("utf-8-sig")
            except UnicodeDecodeError:  # a hand-edited JSON list saved as Windows-1252
                return body.decode("cp1252", "replace")
        except urllib.error.HTTPError as e:
            if 400 <= e.code < 500:  # an answer, not a failure: retrying will not change it
                raise ServiceError(f"{url}: HTTP {e.code}") from None
            if attempt == 2:
                raise
        except OSError:  # URLError, 5xx and timeouts
            if attempt == 2:
                raise


def get_json(url: str) -> dict:
    data = json.loads(get_text(url))
    if isinstance(data, dict) and "error" in data and len(data) == 1:
        error = data["error"]
        if isinstance(error, dict) and error.get("code") in (403, 498, 499):
            raise Secured(url)
        raise ServiceError(f"{url}: {error}")
    return data


def with_param(url: str, param: str) -> str:
    return url + ("&" if "?" in url else "?") + param


def rest_layers(root: str, warnings: list[str]) -> int:
    """Layers in every service of an ArcGIS REST root, folders walked one level. A folder or
    service that is secured or answers with an error counts 0; a network failure fails the
    whole count, so a timeout cannot pass for a smaller number."""
    top = get_json(with_param(root, "f=json"))
    services = list(top.get("services", []))
    secured = []
    for folder in top.get("folders", []):
        try:
            services += get_json(f"{root}/{urllib.parse.quote(folder)}?f=json").get("services", [])
        except Secured:
            secured.append(folder)
        except (ServiceError, ValueError) as e:
            warnings.append(f"folder {folder}: {e}")
    types = defaultdict(set)
    for s in services:
        types[s["name"]].add(s["type"])

    def count(name: str) -> int:
        kind = next((t for t in ("FeatureServer", "MapServer") if t in types[name]), None)
        if kind is None:
            return 1 if "ImageServer" in types[name] else 0
        url = f"{root}/{urllib.parse.quote(name)}/{kind}?f=json"
        try:
            layers = get_json(url).get("layers") or []
        except Secured:
            secured.append(f"{name}/{kind}")
            return 0
        except (ServiceError, ValueError) as e:
            warnings.append(f"{name}/{kind}: {e}")
            return 0
        return sum(1 for layer in layers if not layer.get("subLayerIds"))

    with ThreadPoolExecutor(PARALLEL) as pool:
        total = sum(pool.map(count, sorted(types)))
    if secured:
        warnings.append(f"{len(secured)} secured folders or services not counted")
    return total


def count(p: dict, warnings: list[str]) -> int:
    url, platform = p["api_url"], p["platform"]
    if "/sharing/rest/search" in url:
        return int(get_json(with_param(url, "num=1&f=json"))["total"])
    if platform == "arcgis-hub":
        return int(get_json(with_param(url, "limit=1"))["numberMatched"])
    if platform == "ckan":
        return int(get_json(with_param(url, "rows=0"))["result"]["count"])
    if platform == "opendatasoft":
        return int(get_json(with_param(url, "limit=0"))["total_count"])
    if platform == "socrata":
        return int(get_json(with_param(url, "limit=0"))["resultSetSize"])
    if platform == "arcgis-rest":
        return rest_layers(url.rstrip("/"), warnings)
    if platform == "custom":  # a download list with a JSON API: GRIN's, or a JKAN site's
        d = get_json(url)
        return len(d["results"] if isinstance(d, dict) else d)
    raise ValueError(f"no counting method for platform {platform!r}")


def counted(p: dict) -> bool:
    return bool(p["api_url"]) and "shared portal of" not in p["notes"] \
        and "not counted" not in p["notes"]


def main():
    args = sys.argv[1:]
    if not args or args[0] != "--count":
        sys.exit(__doc__)
    only = set(args[1:])
    portals = read_csv(PORTALS)
    todo = [p for p in portals if counted(p) and (not only or p["jurisdiction"] in only)]

    def run(p: dict):
        warnings = []
        try:
            return p, count(p, warnings), None, warnings
        except (OSError, ServiceError, ValueError, KeyError, TypeError) as e:
            return p, None, e, warnings

    counts = {}
    failed = 0
    with ThreadPoolExecutor(PARALLEL) as pool:
        for p, n, err, warnings in pool.map(run, todo):
            where = f"{p['jurisdiction']} {p['portal_url']}"
            for w in warnings:
                print(f"  warn  {where}: {w}")
            if err is not None:
                failed += 1
                print(f"  FAIL  {where}: {err} (kept {p['layers_seen'] or 'blank'})")
            else:
                counts[p["jurisdiction"], p["portal_url"]] = str(n)

    # The run takes a minute or more and others edit the file meanwhile: read it again, write
    # back only the counts, and never drop a column this checkout's PORTAL_COLS does not know.
    portals = read_csv(PORTALS)
    unknown = [c for c in (portals[0] if portals else {}) if c not in PORTAL_COLS]
    if unknown:
        sys.exit(f"portals.csv has columns {unknown} that common.PORTAL_COLS lacks; "
                 "nothing written, run again")
    changed = 0
    for p in portals:
        n = counts.get((p["jurisdiction"], p["portal_url"]))
        if n is not None and counted(p) and n != p["layers_seen"]:
            changed += 1
            print(f"  {p['layers_seen'] or 'blank':>5} -> {n:<5} {p['jurisdiction']} {p['portal_url']}")
            p["layers_seen"] = n

    write_csv(PORTALS, PORTAL_COLS, portals)
    print(f"{len(todo)} portals counted; {changed} changed, {failed} failed")

if __name__ == "__main__":
    main()
