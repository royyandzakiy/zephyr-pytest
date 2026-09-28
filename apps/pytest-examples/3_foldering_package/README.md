## To Run

```bash
pip install -e .
pytest -vvv
```

## Results

note: recorded before the folders were renamed, so the prompt still says `3_foldering_project`.

```bash
root@ff4455457a36:/workspaces/zephyr-pytest/apps/pytest-examples/3_foldering_project# pip install -e .
Obtaining file:///workspaces/zephyr-pytest/apps/pytest-examples/3_foldering_project
  Installing build dependencies ... done
  Checking if build backend supports build_editable ... done
  Getting requirements to build editable ... done
  Preparing editable metadata (pyproject.toml) ... done
Building wheels for collected packages: foldering
  Building editable for foldering (pyproject.toml) ... done
  Created wheel for foldering: filename=foldering-0.1.0-0.editable-py3-none-any.whl size=1212 sha256=9d9d1c0797210783f363dafe25d579b0b773daf79aadf8381afceab4153191f4
  Stored in directory: /tmp/pip-ephem-wheel-cache-71onj7vf/wheels/30/54/01/14e21d6db53edeeac0e339dd3266405fd5e04e7e2a5454a151
Successfully built foldering
Installing collected packages: foldering
Successfully installed foldering-0.1.0
root@ff4455457a36:/workspaces/zephyr-pytest/apps/pytest-examples/3_foldering_project# pytest -vvv
============================== test session starts ==============================
platform linux -- Python 3.12.3, pytest-9.1.1, pluggy-1.6.0 -- /opt/python-venv/bin/python3
cachedir: .pytest_cache
rootdir: /workspaces/zephyr-pytest/apps/pytest-examples/3_foldering_project
configfile: pyproject.toml
plugins: platformdirs-4.12.0
collected 1 item                                                                

tests/test_calc.py::test_add PASSED                                       [100%]

=============================== 1 passed in 0.37s ===============================
root@ff4455457a36:/workspaces/zephyr-pytest/apps/pytest-examples/3_foldering_project# 
```