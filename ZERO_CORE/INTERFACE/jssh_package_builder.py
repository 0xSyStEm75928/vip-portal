#!/usr/bin/env python3
import os
import json
import hashlib
import zipfile
from datetime import datetime, timezone

ROOT = os.path.expanduser("~/ZERO_CORE")
DIST = os.path.join(ROOT, "DIST")
PACKAGE_JSON = os.path.join(DIST, "JSSH_PACKAGE.json")
ZIP = os.path.join(DIST, "JSSH-PORTABLE.zip")

FILES = [
    "PANDEMONIUM/state/JSSH_PORTABLE.json",
    "INTERFACE/zero_core_jssh_portable.py",
    "LICENSE"
]

def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()

def main():
    os.makedirs(DIST, exist_ok=True)

    records = []

    for rel in FILES:
        path = os.path.join(ROOT, rel)

        if os.path.isfile(path):
            records.append({
                "path": rel,
                "state": "PRESENT",
                "sha256": sha256(path),
                "size": os.path.getsize(path)
            })
        else:
            records.append({
                "path": rel,
                "state": "MISSING"
            })

    package = {
        "schema": "JSSH.package.v1",
        "product": {
            "name": "JSSH",
            "edition": "PORTABLE",
            "version": "1.0.0"
        },
        "identity": {
            "license_number": "JSSH-2026-0001",
            "scope": "JSSH"
        },
        "runtime": {
            "format": "JSON",
            "projection": "JSON_NATIVE",
            "mode": "READ_ONLY"
        },
        "package": {
            "type": "PORTABLE_DISTRIBUTION",
            "files": records
        },
        "generated_at":
            datetime.now(timezone.utc).isoformat()
    }

    raw = json.dumps(
        package,
        sort_keys=True,
        ensure_ascii=False,
        separators=(",", ":")
    ).encode()

    package["integrity"] = {
        "algorithm": "sha256",
        "digest": hashlib.sha256(raw).hexdigest()
    }

    with open(PACKAGE_JSON, "w", encoding="utf-8") as f:
        json.dump(package, f, indent=2, ensure_ascii=False)
        f.write("\n")

    with zipfile.ZipFile(
        ZIP,
        "w",
        compression=zipfile.ZIP_DEFLATED
    ) as z:

        z.write(
            PACKAGE_JSON,
            "JSSH_PACKAGE.json"
        )

        for rel in FILES:
            path = os.path.join(ROOT, rel)

            if os.path.isfile(path):
                z.write(
                    path,
                    os.path.basename(rel)
                )

    print("JSSH PACKAGE")
    print("============")
    print("PRODUCT : JSSH PORTABLE")
    print("LICENSE : JSSH-2026-0001")
    print("VERSION : 1.0.0")
    print()
    print("PACKAGE : " + ZIP)
    print("MANIFEST: " + PACKAGE_JSON)
    print()
    print("PACKAGE_READY=True")

if __name__ == "__main__":
    main()
