import sys
from pathlib import Path

import pytest

ROOT_DIR = Path(__file__).parent.parent.parent
sys.path.append(str(ROOT_DIR))

from rng.secure import SecureRandomNumberGenerator
from rng.base import IRandomNumberGenerator
from rng.tests.test_base import IRandomNumberGeneratorTest


class TestBaseRandomNumberGenerator(IRandomNumberGeneratorTest):
    """
    Test class for BaseRandomNumberGenerator.
    """

    @pytest.fixture
    def rng(self) -> IRandomNumberGenerator:
        return SecureRandomNumberGenerator()
