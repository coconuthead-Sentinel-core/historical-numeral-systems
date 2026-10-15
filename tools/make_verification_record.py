#!/usr/bin/env python3
"""
Produce the plain-text verification record that goes to Google Drive.

    python tools/make_verification_record.py > record.txt

The record carries the commit, the tree id, the archive bundle's SHA-256,
and a SHA-256 per tracked file. It is a CROSS-CHECK, not a backup: when the
copies disagree, this is the independent reference you read to find out what
the truth was supposed to be. Recovery itself uses GitHub or a bundle.

Why a text record rather than the bundle itself: pushing a 90 KB binary
through an assistant's context costs on the order of 230,000 tokens, because
base64 is token-dense and the content has to pass through twice. The record
is about 3,400 characters and carries the same verifying information.

``record.txt`` is deliberately git-ignored. It is a snapshot of the working
tree at one moment; committing it would make it stale the moment anything
changes, and the manifest already records the durable parts.
"""
from __future__ import annotations
import hashlib
import pathlib
import subprocess
import sys
from datetime import datetime

REPO = pathlib.Path(__file__).resolve().parent.parent
MANIFEST = REPO / "docs" / "mirror-manifest.json"


def git(*args: str) -> str:
    return subprocess.run(
        ["git", *args], cwd=REPO, capture_output=True, text=True
    ).stdout.strip()


def sha256_of(path: pathlib.Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 16), b""):
            digest.update(chunk)
    return digest.hexdigest()


def bundle_path() -> pathlib.Path | None:
    """The archive bundle named in the manifest, if it is reachable."""
    import json
    try:
        data = json.loads(MANIFEST.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None
    recorded = data.get("off_machine_bundle", {}).get("local_copy")
    if not recorded:
        return None
    path = pathlib.Path(recorded)
    return path if path.exists() else None


def main() -> int:
    lines: list[str] = []
    add = lines.append

    add("HISTORICAL-NUMERAL-SYSTEMS - VERIFICATION RECORD")
    add("=" * 64)
    add("")
    add("Purpose: an independent cloud reference for cross-checking the")
    add("other copies. This record lives in Google Drive, which is")
    add("independent of both GitHub and OneDrive. It is a RECORD, not a")
    add("backup - recovery uses GitHub or a git bundle.")
    add("")
    add("Recorded      : "
        + datetime.now().astimezone().isoformat(timespec="seconds"))
    add("Repository    : coconuthead-Sentinel-core/historical-numeral-systems")
    add("Branch        : main")
    add("")
    add("COMMIT UNDER RECORD")
    add("  commit  : " + git("rev-parse", "HEAD"))
    add("  short   : " + git("rev-parse", "--short", "HEAD"))
    add("  tree    : " + git("rev-parse", "HEAD^{tree}"))
    add("  authored: " + git("log", "-1", "--format=%cI"))
    add("  subject : " + git("log", "-1", "--format=%s"))

    dirty = git("status", "--porcelain")
    if dirty:
        add("")
        add("  WARNING: the working tree had uncommitted changes when this")
        add("  record was made, so the per-file hashes below do not")
        add("  correspond to the commit above. Commit first, then re-record.")

    bundle = bundle_path()
    add("")
    add("ARCHIVE BUNDLE")
    if bundle is None:
        add("  none reachable at the path in docs/mirror-manifest.json")
    else:
        add("  filename: " + bundle.name)
        add("  sha256  : " + sha256_of(bundle))
        add("  bytes   : " + str(bundle.stat().st_size))
        add("  recover : git clone <bundle> recovered")

    add("")
    add("WHERE THE COPIES ARE")
    add("  See docs/MIRRORS.md and docs/mirror-manifest.json. The short")
    add("  version: GitHub is the truth; the laptop clone sits inside the")
    add("  OneDrive sync root and so is ONE point wearing two hats; two")
    add("  bundle copies are kept, one inside OneDrive and one outside it.")
    add("")
    add("HOW TO CHECK")
    add("  python tools/verify_mirrors.py")
    add("  git bundle verify <bundle>")
    add("  Compare the commit above against GitHub's main.")

    files = [f for f in git("ls-files").splitlines() if f]
    add("")
    add(f"TRACKED FILES AND SHA-256 ({len(files)} files)")
    add("-" * 64)
    for name in files:
        path = REPO / name
        digest = sha256_of(path) if path.exists() else "MISSING" * 2
        add(digest[:16] + "  " + name)
    add("-" * 64)
    add("Hashes are of the working-tree bytes on Windows, so files stored")
    add("with LF in git appear here with CRLF. Compare like with like: use")
    add("the commit and tree ids above for a git-level comparison.")

    sys.stdout.write("\n".join(lines) + "\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
