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

### Point 3 — Archive bundle, kept in two places.

A `git bundle` — one file holding the complete history, every commit and
every branch. A bundle beats a zip of the folder for three reasons: it
carries the full history rather than one snapshot, `git bundle verify` proves
it is internally intact, and it can be cloned from directly:

```bash
git clone historical-numeral-systems-<sha>.bundle recovered
```

**The same bundle is kept in two locations, because they fail differently:**

| Location | Survives | Does not survive |
|---|---|---|
| `C:\Users\sbrya\source\sentinels-forge-archives\` | a OneDrive sync fault | disk loss |
| `OneDrive\Sentinels Forge Archives\` | disk loss | an OneDrive account event |

Together they close both gaps for the price of a 90 KB file. An immutable
archive is also far less exposed to a bad sync resolution than a live working
tree is, which is the second reason the bundle exists at all.

### Point 4 — Verification record, in Google Drive.

A plain-text record in Drive — independent of GitHub *and* of OneDrive —
carrying the commit id, the tree id, the bundle's SHA-256, and a SHA-256 per
tracked file.

```bash
python tools/make_verification_record.py > record.txt
```

**This is a cross-check, not a backup.** When the copies disagree, this is
the reference you read to find out what the truth was supposed to be.
Recovery itself uses GitHub or a bundle.

**Why a record rather than the bundle itself:** pushing the 90 KB binary
through an assistant's context costs on the order of **230,000 tokens** —
base64 is token-dense and the content has to pass through twice, once read
and once written. The text record is about 3,400 characters and carries the
same verifying information. If you want the bundle in Drive as well, upload
it by hand through the Drive web interface; that costs nothing and takes a
few seconds.

`record.txt` is git-ignored on purpose. It is a snapshot of the working tree
at one moment, so committing it would make it stale on the next change.
[`mirror-manifest.json`](mirror-manifest.json) holds the durable parts: tip
commit, SHA-256, and every location above.

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

Stated plainly, because a redundancy scheme whose limits are unstated is
mostly a feeling.

- **The working clone and the OneDrive bundle share one OneDrive account.**
  An account-level event takes both.
- **The working clone and the non-OneDrive bundle share one physical disk.**
  A disk failure takes both.
- **GitHub is the only copy independent of both the account and the disk.**
  That is why it is the source of truth and not merely the convenient one.
- **The Drive record is a record.** It proves what the truth was; it cannot
  restore anything. Do not mistake point 4 for a third backup.
- **`verify_mirrors.py` does not reach into Drive**, and will not be given
  credentials to. The Drive record is read by eye.
- **The E: backup drive was not attached when this was set up.** If it
  returns, a bundle there is a genuine separate-hardware point and the better
  home for the archive series.

## Re-archive checklist

Short version, for after a push worth keeping:

1. `python tools/verify_mirrors.py` — confirm GitHub and the laptop agree.
2. `git bundle create ... --all` and `git bundle verify` it.
3. Copy the bundle to **both** archive locations.
4. `python tools/make_verification_record.py > record.txt`, upload to Drive.
5. Update `docs/mirror-manifest.json` with the new tip commit, SHA-256 and
   byte count, and commit that.

Step 5 is why the bundle normally reads `BEHIND by 1`.
