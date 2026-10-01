# mcumgr-hello

A hello world that prints `OLD` or `UPDATED`, used to try a firmware upgrade over MCUmgr from pytest.

```bash
# Build the OLD & UPDATED firmware, plain app, no bootloader
west build -b nrf5340dk/nrf5340/cpuapp -s apps/mcumgr-hello -d build_old -- -DFIRMWARE_VERSION=OLD \
&& west build -b nrf5340dk/nrf5340/cpuapp -s apps/mcumgr-hello -d build_updated -- -DFIRMWARE_VERSION=UPDATED \
&& west flash --runner nrfutil -d build_old \
&& python3 -m serial.tools.miniterm --raw /dev/ttyACM1 115200
```

## Test: firmware update over MCUmgr

[tests/firmware_update](tests/firmware_update/testcase.yaml) builds `src/main.cpp` with MCUboot (sysbuild) and an SMP server on the shell UART. The pytest side then:

1. waits for the shell on the OLD image
2. builds the same test app again with `FIRMWARE_VERSION=UPDATED`, into `<build_dir>/updated`
3. uploads its `zephyr.signed.bin` with `mcumgr image upload`, marks it with `image test`, and resets
4. waits for MCUboot to swap and checks for `Hello World! - UPDATED FIRMWARE`

Needs the `mcumgr` CLI in the container. If it's missing the test is skipped, not failed:

```bash
go install github.com/apache/mynewt-mcumgr-cli/mcumgr@latest
```

Through Twister:

```bash
west twister --device-testing -T apps/mcumgr-hello/tests/firmware_update --hardware-map apps/mcumgr-hello/hardware-map.yaml

west twister --device-testing --flash-before -T apps/mcumgr-hello/tests/firmware_update --hardware-map apps/mcumgr-hello/hardware-map.yaml
```

Plain pytest, against a build you made yourself. The `dut` fixture flashes it:

```bash
west build -b nrf5340dk/nrf5340/cpuapp --sysbuild -p always -d build_fw apps/mcumgr-hello/tests/firmware_update

pytest apps/mcumgr-hello/tests/firmware_update/pytest -p twister_harness.plugin \
  --twister-harness --device-type=hardware --build-dir=build_fw \
  --platform=nrf5340dk/nrf5340/cpuapp --device-serial=/dev/ttyACM1 \
  --runner=nrfutil --device-id=1050073602
```
