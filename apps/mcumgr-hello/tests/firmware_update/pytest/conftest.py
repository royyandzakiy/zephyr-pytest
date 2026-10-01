# tests/firmware_update/pytest/conftest.py

import pytest
from twister_harness import MCUmgr


@pytest.fixture(scope='session')
def is_mcumgr_available() -> None:
    """Fail, don't skip, when the mcumgr CLI is missing.

    Overrides the twister_harness fixture of the same name, which calls
    pytest.skip(). Twister then reports "0 of 0 executed, 1 skipped" with no
    error, which looks like a pass at a glance. In this test mcumgr is the
    whole point, so a missing binary is a broken setup.
    """
    if not MCUmgr.is_available():
        pytest.fail(
            'mcumgr CLI not found on PATH. Install it with '
            '`go install github.com/apache/mynewt-mcumgr-cli/mcumgr@latest` '
            'and add $(go env GOPATH)/bin to PATH, or rebuild the devcontainer image.'
        )
