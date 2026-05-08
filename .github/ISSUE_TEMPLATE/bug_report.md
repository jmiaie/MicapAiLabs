---
name: Bug report
about: Something isn't working as expected
labels: bug
---

**Describe the bug**
A clear description of what went wrong.

**To Reproduce**
```python
# Minimal code that reproduces the issue
from ompa import Ompa

ao = Ompa(vault_path="./test-vault")
# ...
```

**Expected behavior**
What you expected to happen.

**Actual behavior**
What actually happened, including any error messages or tracebacks.

**Environment**
- OMPA version: (run `pip show ompa`)
- Python version: (run `python --version`)
- OS: 
- Install type: `pip install ompa` / `pip install ompa[all]` / source

**Additional context**
Any other context, logs, or screenshots.
