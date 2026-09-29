import logging
import time
import pytest
from twister_harness import DeviceAdapter, Shell, McuMgr

logger = logging.getLogger(__name__)

def test_upgrade(dut: DeviceAdapter, shell: Shell, mcumgr: McuMgr):
    shell.exec_command('kernel version')
    dut.disconnect() # free serial port, mcumgr takes over

    mcumgr.image_upload('../../../build_updated/zephyr/zephyr.bin')
    mcumgr.reset_device()

    dut.connect()
    lines = dut.readlines_until(regex='Hello World!', timeout=10)
    output = '\n'.join(lines)

    assert 'Hello World! - UPDATED FIRMWARE' in output
    logger.info('MCUmgr image upgrade test completed successfully')