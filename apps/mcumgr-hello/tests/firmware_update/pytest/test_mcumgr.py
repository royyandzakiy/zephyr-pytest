# tests/firmware_update/pytest/test_mcumgr.py

import logging
import subprocess
from pathlib import Path

from twister_harness import DeviceAdapter, MCUmgr, Shell

logger = logging.getLogger(__name__)

TEST_DIR = Path(__file__).resolve().parents[1]  # tests/firmware_update


def build_updated_image(dut: DeviceAdapter) -> Path:
    """Build this same test app again with FIRMWARE_VERSION=UPDATED.

    Built with sysbuild like the image on the board, so MCUboot mode, signing
    key and imgtool arguments all match. The app is its own sysbuild image,
    named after its source folder, so the CMake variable needs that prefix.
    """
    build_dir = Path(dut.device_config.build_dir)
    app_name = Path(dut.device_config.app_build_dir).name
    out_dir = build_dir / 'updated'

    command = [
        'west', 'build', '-p', 'always', '--sysbuild',
        '-b', dut.device_config.platform,
        '-d', str(out_dir),
        '-s', str(TEST_DIR),
        '--', f'-D{app_name}_FIRMWARE_VERSION=UPDATED',
        # Higher than the 0.0.0+0 on the board. Some MCUboot modes (overwrite-
        # only on the ESP32-S3, swap-using-offset on the nRF5340) refuse an
        # image that isn't newer.
        f'-D{app_name}_CONFIG_MCUBOOT_IMGTOOL_SIGN_VERSION="0.0.1+0"',
    ]
    logger.info('CMD: %s', ' '.join(command))
    subprocess.run(command, check=True)

    image = out_dir / app_name / 'zephyr' / 'zephyr.signed.bin'
    assert image.is_file(), f'no signed image at {image}'
    # Catch a build that silently stayed OLD before spending a whole upload on it.
    assert b'UPDATED' in image.read_bytes(), f'{image} was not built with FIRMWARE_VERSION=UPDATED'
    return image


def clear_buffer(dut: DeviceAdapter) -> None:
    """Drop anything already read, so the boot log after reset starts clean."""
    disconnect = False
    if not dut.is_device_connected():
        dut.connect()
        disconnect = True
    dut.clear_buffer()
    if disconnect:
        dut.disconnect()


def test_upgrade(dut: DeviceAdapter, shell: Shell, mcumgr: MCUmgr):
    # OLD firmware is up and the shell answers
    shell.exec_command('kernel version')

    image = build_updated_image(dut)

    dut.disconnect()  # free serial port, mcumgr takes over
    mcumgr.image_upload(image)

    # Mark slot 1 as pending. Without this MCUboot ignores the upload and
    # boots the OLD image again.
    mcumgr.image_test(mcumgr.get_hash_to_test())

    clear_buffer(dut)
    mcumgr.reset_device()

    dut.connect()
    lines = dut.readlines_until(regex='Hello World!', timeout=60)  # swap takes a while
    output = '\n'.join(lines)

    assert 'Hello World! - UPDATED FIRMWARE' in output
    logger.info('MCUmgr image upgrade test completed successfully')
