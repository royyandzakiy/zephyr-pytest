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
