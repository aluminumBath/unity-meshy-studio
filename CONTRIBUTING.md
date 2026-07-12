# Contributing

Small, focused PRs are easiest to review. A few ground rules:

- Skills should stay short and task-specific. If a skill needs an essay,
  it probably wants to be two skills.
- No credentials, no generated binaries, no copyrighted sample assets.
- Run `python tools/validate_release.py` before pushing.
- If you touch the editor scripts, test them in the Unity version the README
  documents — API churn there is the most common breakage.
- Anything that weakens the credit-confirmation or credential handling will
  be rejected, even if it's more convenient. Those safeguards are the point.

Describe behavior changes (and any security implications) in the PR body.
