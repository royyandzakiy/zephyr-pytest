# mcumgr-hello

A hello world that prints `OLD` or `UPDATED`, used to try a firmware upgrade over MCUmgr from pytest.

```bash
# Build the OLD & UPDATED firmware, both with MCUboot (sysbuild), from the test folder
west build -b nrf5340dk/nrf5340/cpuapp --sysbuild -p always \
  -d apps/mcumgr-hello/build_old \
  -s apps/mcumgr-hello/tests/firmware_update \
&& west build -b nrf5340dk/nrf5340/cpuapp --sysbuild -p always \
  -d apps/mcumgr-hello/build_updated \
  -s apps/mcumgr-hello/tests/firmware_update -- \
  -DFIRMWARE_VERSION=UPDATED \
&& west flash --runner nrfutil -d apps/mcumgr-hello/build_old \
&& python3 -m serial.tools.miniterm --raw /dev/ttyACM1 115200

# to test flash the updated firmware
west flash --runner nrfutil -d apps/mcumgr-hello/build_updated \
&& python3 -m serial.tools.miniterm --raw /dev/ttyACM1 115200
```

The app folder itself (`apps/mcumgr-hello`) has no MCUboot and no SMP server, so it can't receive an update. Use the test folder for anything MCUmgr.

`FIRMWARE_VERSION` is read with `zephyr_get()`, so plain `-DFIRMWARE_VERSION=UPDATED` reaches the app under sysbuild. A prefixed form has to use the sysbuild image name, which is the source folder name: `-Dfirmware_update_FIRMWARE_VERSION=UPDATED`, not the CMake `project()` name. The build log prints `FIRMWARE_VERSION: ...` so you can check.

On the nRF5340 DK, MCUboot only boots because of [sysbuild/mcuboot.conf](tests/firmware_update/sysbuild/mcuboot.conf). Without it, vanilla Zephyr v4.4's MCUboot BusFaults before the console is up and the board stays silent; the file explains the chain.

## Test: firmware update over MCUmgr

[tests/firmware_update](tests/firmware_update/testcase.yaml) builds `src/main.cpp` with MCUboot (sysbuild) and an SMP server on the shell UART. The pytest side then:

1. waits for the shell on the OLD image
2. builds the same test app again with `FIRMWARE_VERSION=UPDATED`, into `<build_dir>/updated`
3. uploads its `zephyr.signed.bin` with `mcumgr image upload`, marks it with `image test`, and resets
4. waits for MCUboot to swap and checks for `Hello World! - UPDATED FIRMWARE`

Needs the `mcumgr` CLI on `PATH`. If it's missing, [pytest/conftest.py](tests/firmware_update/pytest/conftest.py) fails the test instead of letting twister_harness skip it:

```bash
go install github.com/apache/mynewt-mcumgr-cli/mcumgr@latest \
&& export PATH="$PATH:$(go env GOPATH)/bin" \
&& mcumgr version
```

Through Twister:

```bash
west twister --device-testing --flash-before -T apps/mcumgr-hello/tests/firmware_update --hardware-map apps/mcumgr-hello/hardware-map.yaml
```

Plain pytest, against a build you made yourself. The `dut` fixture flashes it:

```bash
west build -b nrf5340dk/nrf5340/cpuapp --sysbuild -p always -d build_fw apps/mcumgr-hello/tests/firmware_update

pytest apps/mcumgr-hello/tests/firmware_update/pytest -p twister_harness.plugin \
  --twister-harness --device-type=hardware --build-dir=build_fw \
  --platform=nrf5340dk/nrf5340/cpuapp --device-serial=/dev/ttyACM1 \
  --runner=nrfutil --device-id=1050073602 --flash-before
```

`--flash-before` (in both commands) flashes first and opens the serial port after. Without it the harness holds the port while flashing: on the ESP32-S3, where flashing and the console share one USB port, the chip then boots into download mode.
