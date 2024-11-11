import sys
from pathlib import Path

import pytest

ROOT_DIR = Path(__file__).parent.parent.parent
sys.path.append(str(ROOT_DIR))

from rng.base import IRandomNumberGenerator
from rng.base import BaseRandomNumberGenerator


class IRandomNumberGeneratorTest:
    """
    Base test class for IRandomNumberGenerator implementations.
    """

    @pytest.fixture
    def rng(self) -> IRandomNumberGenerator:
        """
        Fixture to be overridden by subclasses to provide the specific RNG implementation.
        """
        raise NotImplementedError

    def test_random(self, rng: IRandomNumberGenerator):
        value = rng.random()
        assert 0.0 <= value < 1.0

    def test_sequence(self, rng: IRandomNumberGenerator):
        length = 10
        sequence = rng.sequence(length)
        assert len(sequence) == length
        assert all(0.0 <= value < 1.0 for value in sequence)

    def test_int(self, rng: IRandomNumberGenerator):
        min_value = 1
        max_value = 10
        value = rng.int(min_value, max_value)
        assert min_value <= value <= max_value

    def test_float(self, rng: IRandomNumberGenerator):
        min_value = 1.0
        max_value = 10.0
        value = rng.float(min_value, max_value)
        assert min_value <= value <= max_value

    def test_choice(self, rng: IRandomNumberGenerator):
        sequence = [1, 2, 3, 4, 5]
        value = rng.choice(sequence)
        assert value in sequence

    def test_shuffle(self, rng: IRandomNumberGenerator):
        sequence = [1, 2, 3, 4, 5]
        original_sequence = sequence.copy()
        rng.shuffle(sequence)
        assert len(sequence) == len(original_sequence)
        assert set(sequence) == set(original_sequence)
        assert sequence != original_sequence  # Ensure the sequence is shuffled


class TestBaseRandomNumberGenerator(IRandomNumberGeneratorTest):
    """
    Test class for BaseRandomNumberGenerator.
    """

    @pytest.fixture
    def rng(self) -> IRandomNumberGenerator:
        return BaseRandomNumberGenerator()
