# Apply this upgrade to the existing CleanListen repository

This folder is an **overlay**, not a replacement for the original repository. Keep the existing `data/` and `notebook/` directories.

Recommended branch workflow:

```bash
git checkout main
git pull
git checkout -b productize/cleanlisten-v0.1

# Copy the contents of this upgrade folder into the repository root.
# Do not delete the existing data/ or notebook/ directories.

git add README.md pyproject.toml .gitignore CONTRIBUTING.md \
  src tests docs examples .github PR_BODY.md

git commit -m "Productize CleanListen CLI and evaluation workflow"
git push -u origin productize/cleanlisten-v0.1
```

Use `PR_BODY.md` as the draft pull-request description.
