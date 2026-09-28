## Build & Run tests via Twister

```bash
# normal tests
west twister -T apps/emul-shell-gpio/tests/emul_button_toggle -p native_sim/native

# slow tests
west twister -T apps/emul-shell-gpio/tests/emul_button_toggle \
  -p native_sim/native \
  --pytest-args="-m slow"
```

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