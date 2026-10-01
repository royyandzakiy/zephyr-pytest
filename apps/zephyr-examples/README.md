# zephyr-examples

Zephyr apps tested with pytest through Twister's pytest harness. They're numbered in the order I'd read them, after [pytest-examples](../pytest-examples/README.md).

| Folder | What it shows | Test layout |
|--------|---------------|-------------|
| [1_gpio-emul-shell](1_gpio-emul-shell/README.md) | pressing an emulated button from a shell command, on `native_sim` and the nRF5340 DK | separate test image under `tests/`, because the test hooks must not ship |
| [2_mcumgr-dfu](2_mcumgr-dfu/README.md) | a firmware upgrade over MCUmgr, with MCUboot swapping in the new image | `testcase.yaml` + `pytest/` next to the app, tested as it ships |

Run everything Twister can find here on `native_sim` (only `1_gpio-emul-shell` allows it):

```bash
west twister -T apps/zephyr-examples -p native_sim/native
```

The hardware runs need `--device-testing --flash-before` and a hardware map. Each app's README has the exact command.
