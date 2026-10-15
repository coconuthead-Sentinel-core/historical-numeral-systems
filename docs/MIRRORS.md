# Mirrors

Where the three copies of this repository live, how to check they agree, and
what to do when they do not.

## Why three

Copies drift. When they drift silently, time gets spent hunting for which one
is right instead of doing the work. Three independent points, each checkable,
means the odd one out is identifiable rather than merely suspected.

**The order is fixed: GitHub first, then the laptop, then off-machine.** Work
is polished on GitHub, pulled to the laptop, and archived off-machine from
there. Reversing that order is how divergence starts.

## The three points

### Point 1 — GitHub. The source of truth.

<https://github.com/coconuthead-Sentinel-core/historical-numeral-systems>

Branch `main`. When the copies disagree, this one wins, and the others are
reconciled against it. CI runs here, so this is also the only point where
"the tests pass" is a verified statement rather than a local one.

### Point 2 — Laptop working clone.

`OneDrive\Desktop\Claude AI\Completed projects\historical-numeral-systems`

**This single point covers both the laptop and the OneDrive cloud copy**, and
that is a limitation, not a feature. The folder sits inside the OneDrive sync
root, so the laptop copy and the cloud copy are the same bytes. A sync fault,
a bad merge resolution, or a ransomware event takes both at once.

Counting those as two separate points is the mistake this document exists to
prevent. They are one point wearing two hats.

### Point 3 — Off-machine bundle, in Google Drive.

A `git bundle` — one file holding the complete history, every commit and
every branch. It is independent of GitHub and independent of OneDrive, which
is the whole purpose.

A bundle is better than a zip of the folder for three reasons: it carries the
full history rather than one snapshot, `git bundle verify` proves it is
internally intact, and it can be cloned from directly:

```bash
git clone historical-numeral-systems-<sha>.bundle recovered
```

Its location, tip commit and SHA-256 are recorded in
[`mirror-manifest.json`](mirror-manifest.json).

## Checking them

```bash
python tools/verify_mirrors.py
```

Points 1 and 2 are checked live. Point 3 is checked in full if a local copy of
the bundle is present, and otherwise reported as `RECORDED` from the manifest
rather than claimed as verified. The script says which it did.

Exit status is 0 when everything agrees, 1 otherwise, so it can be wired into
CI or a scheduled check.

### Reading the verdict

| Verdict | Meaning | Action |
|---|---|---|
| `all three agree` | Same commit everywhere. | None. |
| `BEHIND by N` | The bundle's tip is an **ancestor** of the live tip. | Normal. Re-archive when convenient. |
| `DIVERGED` | GitHub and the laptop disagree, or the bundle's tip is **not** an ancestor. | Stop. Reconcile against GitHub before committing. |
| `INCONCLUSIVE` | A live point did not answer. | Check the network, then re-run. |

**The bundle is normally one commit behind, and that is by design.** The
bundle is cut at a release commit; the manifest recording its hash is then
committed on top. So the manifest commit itself is the gap. The script
reports it as `BEHIND by 1`, not as a fault.

## Re-archiving

After a push worth preserving:

```bash
# 1. GitHub is already the truth -- confirm the laptop matches it
python tools/verify_mirrors.py

# 2. Cut a bundle at the current tip
git bundle create "historical-numeral-systems-$(git rev-parse --short HEAD).bundle" --all

# 3. Verify it before trusting it
git bundle verify "historical-numeral-systems-$(git rev-parse --short HEAD).bundle"

# 4. Upload to Google Drive, then record the tip commit, the SHA-256
#    and the Drive URL in docs/mirror-manifest.json, and commit that.
```

A bundle is small — this repository's is well under a megabyte — so keeping
several is cheap and gives you a history of archives rather than a single
point of failure.

## When GitHub goes sideways

This has happened. The order of recovery:

1. **Check the laptop clone.** `git log` and `git fsck` there. If it is clean
   and ahead, push it back up.
2. **If the laptop is also suspect, clone the bundle.** It is self-contained;
   you do not need GitHub or OneDrive to recover from it.
3. **Reconcile, then re-archive.** Do not leave two points agreeing and the
   third unexplained. An unexplained third point is how the next incident
   starts.

## Known limits

- **Points 2 and 3 are on, or derived from, the same physical machine.** If
  the laptop's disk fails before a re-archive, the bundle in Drive is the only
  off-machine copy, and it is only as current as the last upload.
- **`verify_mirrors.py` does not reach into Drive.** That would need
  credentials the script has no business holding. The Drive copy is verified
  by its recorded SHA-256, which means downloading it is a manual step.
- **The E: backup drive was not attached when this was set up.** If it
  returns, a bundle there would be a genuine fourth point on separate
  hardware, and the better home for the archive series.
