# emul-shell-gpio

A Zephyr button + LED app, and a Twister test that presses the button without anyone touching the board.

[src/main.cpp](src/main.cpp) toggles `led0` on every edge of `sw0` and prints `Button pressed! LED is now ON/OFF`. The test image in [tests/emul_button_toggle](tests/emul_button_toggle/testcase.yaml) builds the same `main.cpp` and adds [test_harness.c](tests/emul_button_toggle/test_harness.c), which moves `sw0` onto an emulated GPIO controller (`zephyr,gpio-emul`) and registers a `test_btn` shell command. That command drives the pin with `gpio_emul_input_set`, so the app code runs the same interrupt path it would for a real press. The harness only goes into the test image, never into the app build.

[pytest/test_gpio_toggle.py](tests/emul_button_toggle/pytest/test_gpio_toggle.py) sends `test_btn` twice through Twister's `shell` fixture and expects ON, then OFF.

## Layout

```
emul-shell-gpio/
├── src/main.cpp            # the app
├── boards/                 # app overlays per board (led0 / sw0 aliases)
├── hardware-map.yaml       # which probe and serial port Twister uses
└── tests/emul_button_toggle/
    ├── testcase.yaml       # harness: pytest, platform_allow
    ├── test_harness.c      # test_btn shell command, test image only
    ├── app.overlay         # emulated button AND led, used by native_sim
    ├── boards/             # nRF5340 DK overlay, moves only sw0
    └── pytest/             # the pytest side
```

On the nRF5340 DK, `boards/nrf5340dk_nrf5340_cpuapp.overlay` replaces `app.overlay` rather than adding to it, and it only moves `sw0`. `led0` stays on the real LED1, so you can watch it blink while pytest asserts on the log.

## Build & Run the app

```bash
# native_sim
west build -s apps/emul-shell-gpio -d build -p always -b native_sim/native \
&& ./build/zephyr/zephyr.exe

# nRF5340 DK
west build -s apps/emul-shell-gpio -p always -b nrf5340dk/nrf5340/cpuapp \
&& west flash --runner nrfutil \
&& python3 -m serial.tools.miniterm --raw /dev/ttyACM1 115200

# ESP32-S3
west build -s apps/emul-shell-gpio -p always -b esp32s3_devkitc/esp32s3/procpu --no-sysbuild \
&& west flash --runner esp32 --esp-device /dev/ttyUSB0 \
&& python3 -m serial.tools.miniterm --raw /dev/ttyUSB0 115200
```

If `build/` was ever made by a Windows host build, delete it first. The cache keeps the Windows paths and `west build -p` fails trying to reach them.

## Hardware setup

[hardware-map.yaml](hardware-map.yaml) is the only file with anything specific to my probe in it. Find your own probe ID with `west twister --generate-hardware-map map.yml`, copy the `id` and `serial` over, and comment out the boards that aren't plugged in.

## Build & Run tests via Twister

### Native Sim

```bash
# normal tests
west twister -T apps/emul-shell-gpio/tests/emul_button_toggle -p native_sim/native

# slow tests
west twister -T apps/emul-shell-gpio/tests/emul_button_toggle \
  -p native_sim/native \
  --pytest-args="-m slow"
```

Result

```bash
# normal tests
==== Test test_button_toggle_slow started at 2026-09-28 10:42:29.852201 ====
*** Booting Zephyr OS build v4.4.0 ***
GPIO Button + LED Toggle started
Ready. Press the button to toggle LED.
uart:~$ 
uart:~$ 
uart:~$ 
uart:~$ 
uart:~$ test_btn
Test: Triggering emulated button press
Button pressed! LED is now ON
Button pressed! LED is now ON
uart:~$ 
uart:~$ test_btn
Test: Triggering emulated button press
Button pressed! LED is now OFF
Button pressed! LED is now OFF
uart:~$ 
uart:~$ 
Stopped at 0.320s

# slow tests
...
Button pressed! LED is now OFF
Button pressed! LED is now OFF
uart:~$ 
uart:~$ 
Stopped at 6.300s
```

### nRF5340dk

```bash
west twister -T apps/emul-shell-gpio/tests/emul_button_toggle -p nrf5340dk/nrf5340/cpuapp --device-testing --device-serial /dev/ttyACM0

west twister -T apps/emul-shell-gpio/tests/emul_button_toggle --device-testing --hardware-map apps/emul-shell-gpio/hardware-map.yaml
```

Result: we can see the 3 second break in the slow test

```bash
2026-09-28 14:23:46,418 apps/emul-shell-gpio/tests/emul_button_toggle/pytest/test_gpio_toggle.py::test_button_toggle
2026-09-28 14:23:52,372 -------------------------------- live log call ---------------------------------
2026-09-28 14:23:52,373 #: uart:~$ uart:~$ test_btn
2026-09-28 14:23:52,375 #: Test: Triggering emulated button press
2026-09-28 14:23:52,475 #: uart:~$
2026-09-28 14:23:53,431 #: uart:~$ Button pressed! LED is now ON
2026-09-28 14:23:53,486 #: uart:~$ uart:~$ test_btn
2026-09-28 14:23:53,488 #: Test: Triggering emulated button press
2026-09-28 14:23:53,540 #: uart:~$
2026-09-28 14:23:54,498 #: uart:~$ Button pressed! LED is now OFF
2026-09-28 14:23:54,684 PASSED
2026-09-28 14:23:54,852 apps/emul-shell-gpio/tests/emul_button_toggle/pytest/test_gpio_toggle.py::test_button_toggle_slow
2026-09-28 14:24:03,304 -------------------------------- live log call ---------------------------------
2026-09-28 14:24:03,306 #: uart:~$ uart:~$ test_btn
2026-09-28 14:24:03,308 #: Test: Triggering emulated button press
2026-09-28 14:24:03,409 #: uart:~$
2026-09-28 14:24:04,315 #: uart:~$ Button pressed! LED is now ON
2026-09-28 14:24:07,339 #: uart:~$ uart:~$ test_btn
2026-09-28 14:24:07,343 #: Test: Triggering emulated button press
2026-09-28 14:24:07,394 #: uart:~$
2026-09-28 14:24:08,351 #: uart:~$ Button pressed! LED is now OFF
2026-09-28 14:24:08,383 PASSED
```

## Limitations

- The `Button pressed!` line comes out up to a second after the `test_btn` prompt. `printk` goes through deferred logging here, and the log thread only wakes every 1000 ms (`CONFIG_LOG_PROCESS_THREAD_SLEEP_MS`) or after 10 queued messages. That's why both tests call `readlines_until` after `exec_command`. Without it, pytest reads up to the prompt and misses the line.
- On `native_sim` every `Button pressed!` line shows up twice (see the result above). I haven't checked why yet, my guess is printk reaching two log backends. The test passes anyway since it only checks that the line is there.
- The test assumes the LED starts OFF, and each pytest test reflashes the board to get there.
- There are overlays for `qemu_cortex_m3` and `esp32_devkitc`, but neither is in `platform_allow`, so Twister never picks them.
