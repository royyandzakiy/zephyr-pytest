## ESP32

Build & Run

```bash
west build -s apps/zephyr-examples/1_gpio-emul-shell -p always -b esp32s3_devkitc/esp32s3/procpu --no-sysbuild \
&& west flash --runner esp32 --esp-device /dev/ttyUSB0 \
&& python3 -m serial.tools.miniterm --raw /dev/ttyUSB0 115200
```

## Native Sim

Build & Run

```bash
west build -s apps/zephyr-examples/1_gpio-emul-shell -p always -b native_sim/native \
&& ./apps/zephyr-examples/1_gpio-emul-shell/build/zephyr/zephyr.exe
```

Build & Run tests manually

```bash
west build -d apps/zephyr-examples/1_gpio-emul-shell/build_test -s apps/zephyr-examples/1_gpio-emul-shell/tests/emul_button_toggle -p always -b native_sim/native \
&& ./apps/zephyr-examples/1_gpio-emul-shell/build_test/zephyr/zephyr.exe
```

Build & Run tests via Twister

```bash
west twister -T apps/zephyr-examples/1_gpio-emul-shell/tests/emul_button_toggle -p native_sim/native
```

## nRF

Build & Run

```bash
west build -s apps/zephyr-examples/1_gpio-emul-shell -p always -b nrf5340dk/nrf5340/cpuapp \
&& west flash --runner nrfutil \
&& python3 -m serial.tools.miniterm --raw /dev/ttyACM1 115200

west twister --device-testing -T apps/zephyr-examples/1_gpio-emul-shell/tests/emul_button_toggle --hardware-map apps/zephyr-examples/1_gpio-emul-shell/hardware-map.yaml
```