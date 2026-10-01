import pytest
from twister_harness import MCUmgr


@pytest.fixture(scope='session')
def is_mcumgr_available() -> None:
    """Fail instead of skip when the mcumgr CLI is missing (overrides twister_harness)."""
    if not MCUmgr.is_available():
        pytest.fail('mcumgr CLI not found on PATH, see the README for how to install it')
