# 2_mcumgr-dfu

A hello world that prints `OLD` or `UPDATED`, with MCUboot and an MCUmgr (SMP) server on the shell UART. The pytest test uploads an UPDATED image over MCUmgr and checks that MCUboot boots it.

This app is tested as it ships, so there is one `CMakeLists.txt` and the test sits next to it: [testcase.yaml](testcase.yaml) plus [pytest/](pytest/). Compare [1_gpio-emul-shell](../1_gpio-emul-shell/README.md), which needs a separate test image under `tests/` because its test hooks must not ship.

## Layout

```
2_mcumgr-dfu/
├── CMakeLists.txt        # FIRMWARE_VERSION switch
├── prj.conf              # shell + MCUmgr over the shell transport
├── sysbuild.conf         # builds MCUboot alongside the app
├── sysbuild/mcuboot.conf # extra Kconfig for the MCUboot image
├── testcase.yaml         # Twister: harness pytest, sysbuild
├── hardware-map.yaml     # probe ID and serial port per board
├── pytest/               # test_mcumgr.py, conftest.py
└── src/main.cpp
```

## Build & run by hand

```bash
# OLD and UPDATED, both with MCUboot
west build -b nrf5340dk/nrf5340/cpuapp --sysbuild -p always -d apps/zephyr-examples/2_mcumgr-dfu/build_old -s apps/zephyr-examples/2_mcumgr-dfu \
&& west build -b nrf5340dk/nrf5340/cpuapp --sysbuild -p always -d apps/zephyr-examples/2_mcumgr-dfu/build_updated -s apps/zephyr-examples/2_mcumgr-dfu -- -DFIRMWARE_VERSION=UPDATED \
&& west flash --runner nrfutil -d apps/zephyr-examples/2_mcumgr-dfu/build_old \
&& python3 -m serial.tools.miniterm --raw /dev/ttyACM1 115200

# flash UPDATED directly, to check it boots
west flash --runner nrfutil -d apps/zephyr-examples/2_mcumgr-dfu/build_updated \
&& python3 -m serial.tools.miniterm --raw /dev/ttyACM1 115200
```

The build log prints `FIRMWARE_VERSION: ...`, so you can check which variant you got. If you prefix the variable for a sysbuild image, the prefix is the source folder name (`2_mcumgr-dfu_`), not the CMake `project()` name.

## Test: firmware update over MCUmgr

The test:

1. waits for the shell on the OLD image
2. builds the app again with `FIRMWARE_VERSION=UPDATED`, into `<build_dir>/updated`
3. uploads its `zephyr.signed.bin` with `mcumgr image upload`, marks it with `image test`, and resets
4. waits for MCUboot to swap and checks for `Hello World! - UPDATED FIRMWARE`

It needs the `mcumgr` CLI on `PATH`. The devcontainer image ships it. Otherwise install it by hand (gone after a container rebuild). If it's missing, the test fails instead of skipping:

```bash
go install github.com/apache/mynewt-mcumgr-cli/mcumgr@latest \
&& export PATH="$PATH:$(go env GOPATH)/bin" \
&& mcumgr version
```

Through Twister:

```bash
west twister --device-testing --flash-before -T apps/zephyr-examples/2_mcumgr-dfu --hardware-map apps/zephyr-examples/2_mcumgr-dfu/hardware-map.yaml
```

Plain pytest, against a build you made yourself. The `dut` fixture flashes it:

```bash
west build -b nrf5340dk/nrf5340/cpuapp --sysbuild -p always -d build_fw apps/zephyr-examples/2_mcumgr-dfu

pytest apps/zephyr-examples/2_mcumgr-dfu/pytest -p twister_harness.plugin \
  --twister-harness --device-type=hardware --build-dir=build_fw \
  --platform=nrf5340dk/nrf5340/cpuapp --device-serial=/dev/ttyACM1 \
  --runner=nrfutil --device-id=1050073602 --flash-before
```

`--flash-before` flashes first and opens the serial port after. Without it, the ESP32-S3 boots into download mode, because flashing and the console share one USB port.

## Limitations

- On the nRF5340 DK, vanilla Zephyr v4.4's MCUboot only boots with the two settings in [sysbuild/mcuboot.conf](sysbuild/mcuboot.conf). Without them it faults before the console is up and the board stays silent.
- Only the nRF5340 DK and the ESP32-S3 DevKitC are set up in `hardware-map.yaml`.
