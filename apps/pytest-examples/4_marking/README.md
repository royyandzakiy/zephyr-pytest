```bash
pytest -v                       # everything
pytest -v -m slow               # only slow tests
pytest -v -m "not slow"         # skip slow
pytest -v -m "not slow and not xfail"
```