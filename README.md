# Local publish bundle

This bundle copies the publish-ready Unity Meshy Studio repository into:

`C:\Users\steel\Desktop\Code\unity-meshy-studio`

and stages all changes with Git.

## Run

Double-click:

`stage-to-local-repo.cmd`

or run PowerShell:

```powershell
powershell -ExecutionPolicy Bypass -File .\stage-to-local-repo.ps1
```

The script does **not** commit or push. It only copies and stages the files.

After reviewing:

```powershell
cd C:\Users\steel\Desktop\Code\unity-meshy-studio
git diff --cached --stat
git commit -m "Publish Unity Meshy Studio v1.1.0"
git push -u origin main
```
