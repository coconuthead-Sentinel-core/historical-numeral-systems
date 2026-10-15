#!/usr/bin/env python3
"""
Verify that the three copies of this repository agree.

    python tools/verify_mirrors.py

THE THREE POINTS

  1. GitHub        the source of truth. Checked live with `git ls-remote`.
  2. Laptop        the working clone. Checked from the local git database.
                   It lives inside the OneDrive sync root, so this one
                   point covers both the laptop and the OneDrive cloud
                   copy -- they are the same bytes, and a sync fault
                   takes both at once. That is why point 3 is off-machine.
  3. Off-machine   a git bundle in Google Drive. A bundle is a single file
                   holding the full history, so its tip commit and its
                   SHA-256 are both checkable.

WHAT THIS SCRIPT CAN AND CANNOT CHECK

Points 1 and 2 are verified live. Point 3 is verified against the recorded
SHA-256 in ``docs/mirror-manifest.json`` -- this script does not reach into
Drive, because that needs credentials it has no business holding. If a local
copy of the bundle is present it IS verified in full, with
``git bundle verify`` plus a hash comparison. Otherwise the manifest entry
is reported as RECORDED, not as VERIFIED, and the difference is printed
rather than glossed.

Exit status is 0 when everything reachable agrees, 1 otherwise, so this can
run in CI or a scheduled check.
"""
from __future__ import annotations
import hashlib
import json
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
MANIFEST = REPO / "docs" / "mirror-manifest.json"
BRANCH = "main"


def run(args: list[str], cwd: Path = REPO) -> tuple[int, str]:
    """Run a command, returning (returncode, stripped stdout)."""
    try:
        proc = subprocess.run(
            args, cwd=cwd, capture_output=True, text=True, timeout=60
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        return 1, f"{type(exc).__name__}: {exc}"
    return proc.returncode, (proc.stdout or proc.stderr).strip()


def sha256_of(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 16), b""):
            digest.update(chunk)
    return digest.hexdigest()


def github_sha() -> tuple[str | None, str]:
    code, out = run(["git", "ls-remote", "origin", f"refs/heads/{BRANCH}"])
    if code != 0 or not out:
        return None, f"unreachable ({out.splitlines()[0] if out else 'no output'})"
    return out.split()[0], "reachable"


def local_sha() -> tuple[str | None, str]:
    code, out = run(["git", "rev-parse", "HEAD"])
    if code != 0:
        return None, f"error ({out})"
    dirty_code, dirty = run(["git", "status", "--porcelain"])
    note = "clean" if dirty_code == 0 and not dirty else "UNCOMMITTED CHANGES"
    return out, note


def load_manifest() -> dict | None:
    if not MANIFEST.exists():
        return None
    try:
        return json.loads(MANIFEST.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"  manifest unreadable: {exc}")
        return None


def check_bundle(entry: dict) -> tuple[str | None, str]:
    """Verify a bundle if a local copy is reachable; else report RECORDED."""
    recorded_sha = entry.get("tip_commit")
    recorded_hash = entry.get("sha256")
    local_path = entry.get("local_copy")

    if not local_path:
        return recorded_sha, "RECORDED (no local copy to verify against)"

    path = Path(local_path)
    if not path.is_absolute():
        path = REPO / path
    if not path.exists():
        return recorded_sha, f"RECORDED (local copy absent at {path})"

    actual_hash = sha256_of(path)
    if recorded_hash and actual_hash != recorded_hash:
        return None, (
            f"HASH MISMATCH\n      recorded {recorded_hash}\n"
            f"      actual   {actual_hash}"
        )

    code, out = run(["git", "bundle", "verify", str(path)])
    if code != 0:
        return None, f"bundle verify FAILED ({out.splitlines()[0] if out else ''})"

    code, out = run(["git", "bundle", "list-heads", str(path)])
    if code != 0 or not out:
        return None, "could not list bundle heads"
    tip = out.split()[0]
    return tip, "VERIFIED (bundle intact, hash matches)"


def is_ancestor(maybe_ancestor: str, descendant: str) -> bool:
    code, _ = run(
        ["git", "merge-base", "--is-ancestor", maybe_ancestor, descendant]
    )
    return code == 0


def commits_between(older: str, newer: str) -> str:
    code, out = run(["git", "rev-list", "--count", f"{older}..{newer}"])
    return out if code == 0 else "?"


def verdict_for(results: list[tuple[str, str, str | None, str]]) -> int:
    """Decide the verdict, distinguishing BEHIND from DIVERGED.

    An archive snapshot is taken at a moment, so a bundle whose tip is an
    ANCESTOR of the live tip is merely behind -- normal, and reported with
    the gap. A tip that is not an ancestor is a real divergence and is the
    thing worth waking up for.
    """
    by_name = {name: sha for _, name, sha, _ in results}
    missing = [name for name, sha in by_name.items() if not sha]

    truth = by_name.get("GitHub (truth)")
    local = by_name.get("Laptop + OneDrive")
    bundle = by_name.get("Off-machine bundle")

    if not truth or not local:
        print("  VERDICT: INCONCLUSIVE -- a live point did not answer.")
        print(f"           UNREACHABLE: {', '.join(missing)}")
        return 1

    if truth != local:
        print("  VERDICT: DIVERGED -- GitHub and the laptop disagree.")
        print("           GitHub is the source of truth. Reconcile the")
        print("           laptop against it before committing anything.")
        return 1

    if bundle is None:
        print(f"  VERDICT: live points agree at {truth[:12]}")
        print("           Off-machine bundle NOT VERIFIED. Re-archive it.")
        return 1

    if bundle == truth:
        print(f"  VERDICT: all three agree at {truth[:12]}")
        return 0

    if is_ancestor(bundle, truth):
        gap = commits_between(bundle, truth)
        print(f"  VERDICT: live points agree at {truth[:12]}")
        print(f"           Bundle is BEHIND by {gap} commit(s) at "
              f"{bundle[:12]} -- an archive snapshot, not a divergence.")
        print("           Re-archive when the gap stops being deliberate.")
        return 0

    print("  VERDICT: DIVERGED -- the bundle is not an ancestor of the")
    print(f"           live tip. Bundle {bundle[:12]} sits off the main")
    print("           line of history. Investigate before trusting it.")
    return 1


def main() -> int:
    print("Three-point mirror check")
    print("=" * 72)

    results: list[tuple[str, str, str | None, str]] = []

    gh, gh_note = github_sha()
    results.append(("1", "GitHub (truth)", gh, gh_note))

    loc, loc_note = local_sha()
    results.append(("2", "Laptop + OneDrive", loc, loc_note))

    manifest = load_manifest()
    if manifest is None:
        results.append(("3", "Off-machine bundle", None, "no manifest found"))
    else:
        entry = manifest.get("off_machine_bundle", {})
        tip, note = check_bundle(entry)
        results.append(("3", "Off-machine bundle", tip, note))

    for number, name, sha, note in results:
        shown = sha[:12] if sha else "-".ljust(12)
        print(f"  POINT {number}  {name:<22} {shown}  {note}")

    print("-" * 72)

    verdict = verdict_for(results)

    if manifest:
        entry = manifest.get("off_machine_bundle", {})
        print()
        print("  Off-machine copy:")
        print(f"    Drive file : {entry.get('drive_title', 'unrecorded')}")
        print(f"    Drive URL  : {entry.get('drive_url', 'unrecorded')}")
        print(f"    recorded at: {manifest.get('recorded_at', 'unrecorded')}")

    return verdict


if __name__ == "__main__":
    sys.exit(main())
