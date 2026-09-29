```bash
# Build the OLD & UPDATED firmware
west build -b nrf5340dk/nrf5340/cpuapp -d build_old -- -DFIRMWARE_VERSION=OLD \
&& west build -b nrf5340dk/nrf5340/cpuapp -d build_updated -- -DFIRMWARE_VERSION=UPDATED \
&& west flash --runner nrfutil -d build_old \
&& python3 -m serial.tools.miniterm --raw /dev/ttyACM1 115200

west twister -T apps/mcumgr-hello/tests/firmware_update -p nrf5340dk/nrf5340/cpuapp
```
