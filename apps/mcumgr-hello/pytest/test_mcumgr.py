import logging
import subprocess
from pathlib import Path

from twister_harness import DeviceAdapter, MCUmgr, Shell

logger = logging.getLogger(__name__)

APP_DIR = Path(__file__).resolve().parents[1]


def build_updated_image(dut: DeviceAdapter) -> Path:
    """Build the app again with FIRMWARE_VERSION=UPDATED, same sysbuild setup as the board."""
    build_dir = Path(dut.device_config.build_dir)
    app_name = Path(dut.device_config.app_build_dir).name  # sysbuild image name
    out_dir = build_dir / 'updated'

    command = [
        'west', 'build', '-p', 'always', '--sysbuild',
        '-b', dut.device_config.platform,
        '-d', str(out_dir),
        '-s', str(APP_DIR),
        '--', '-DFIRMWARE_VERSION=UPDATED',
        # newer than the 0.0.0+0 on the board, MCUboot rejects downgrades
        f'-D{app_name}_CONFIG_MCUBOOT_IMGTOOL_SIGN_VERSION="0.0.1+0"',
    ]
    logger.info('CMD: %s', ' '.join(command))
    subprocess.run(command, check=True)

    image = out_dir / app_name / 'zephyr' / 'zephyr.signed.bin'
    assert image.is_file(), f'no signed image at {image}'
    assert b'UPDATED' in image.read_bytes(), f'{image} was not built with FIRMWARE_VERSION=UPDATED'
    return image


def clear_buffer(dut: DeviceAdapter) -> None:
    disconnect = False
    if not dut.is_device_connected():
        dut.connect()
        disconnect = True
    dut.clear_buffer()
    if disconnect:
        dut.disconnect()


def test_upgrade(dut: DeviceAdapter, shell: Shell, mcumgr: MCUmgr):
    shell.exec_command('kernel version')

    image = build_updated_image(dut)

    dut.disconnect()  # mcumgr needs the serial port
    mcumgr.image_upload(image)
    mcumgr.image_test(mcumgr.get_hash_to_test())  # mark pending, or MCUboot won't swap

    clear_buffer(dut)
    mcumgr.reset_device()

    dut.connect()
    lines = dut.readlines_until(regex='Hello World!', timeout=60)
    output = '\n'.join(lines)

    assert 'Hello World! - UPDATED FIRMWARE' in output
