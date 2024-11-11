import sys
from pathlib import Path

import pytest

ROOT_DIR = Path(__file__).parent.parent.parent
sys.path.append(str(ROOT_DIR))

from rng.base import IRandomNumberGenerator
from rng.base import BaseRandomNumberGenerator
from rng.secure import SecureRandomNumberGenerator
from rng.tests.test_base import IRandomNumberGeneratorTest
from rng.bias import BiasedRandomNumberGeneratorDecorator
from rng.bias import RandomBiasedRandomNumberGeneratorDecorator
from rng.bias import NonLinearBiasedRandomNumberGeneratorDecorator
from rng.bias import NoisyBiasedRandomNumberGeneratorDecorator


class TestBaseRandomNumberGeneratorWithBiasedDeco(IRandomNumberGeneratorTest):
    """
    Test class for BaseRandomNumberGenerator with bias-decorator.
    """

    @pytest.fixture
    def rng(self) -> IRandomNumberGenerator:
        base_rng = BaseRandomNumberGenerator()
        return BiasedRandomNumberGeneratorDecorator(base_rng, base_bias=0.1)


class TestSecureRandomNumberGeneratorWithBiasedDeco(IRandomNumberGeneratorTest):
    """
    Test class for SecureRandomNumberGenerator with bias-decorator.
    """

    @pytest.fixture
    def rng(self) -> IRandomNumberGenerator:
        secure_rng = SecureRandomNumberGenerator()
        return BiasedRandomNumberGeneratorDecorator(secure_rng, base_bias=0.1)


class TestBaseRandomNumberGeneratorWithRandomBiasedDeco(IRandomNumberGeneratorTest):
    """
    Test class for BaseRandomNumberGenerator with random-bias-decorator.
    """

    @pytest.fixture
    def rng(self) -> IRandomNumberGenerator:
        base_rng = BaseRandomNumberGenerator()
        return RandomBiasedRandomNumberGeneratorDecorator(base_rng, base_bias=0.1)


class TestSecureRandomNumberGeneratorWithRandomBiasedDeco(IRandomNumberGeneratorTest):
    """
    Test class for SecureRandomNumberGenerator with random-bias-decorator.
    """

    @pytest.fixture
    def rng(self) -> IRandomNumberGenerator:
        secure_rng = SecureRandomNumberGenerator()
        return RandomBiasedRandomNumberGeneratorDecorator(secure_rng, base_bias=0.1)


class TestBaseRandomNumberGeneratorWithNonLinearBiasedDeco(IRandomNumberGeneratorTest):
    """
    Test class for BaseRandomNumberGenerator with non-linear-bias-decorator.
    """

    @pytest.fixture
    def rng(self) -> IRandomNumberGenerator:
        base_rng = BaseRandomNumberGenerator()
        return NonLinearBiasedRandomNumberGeneratorDecorator(base_rng, base_bias=0.1)


class TestSecureRandomNumberGeneratorWithNonLinearBiasedDeco(
    IRandomNumberGeneratorTest
):
    """
    Test class for SecureRandomNumberGenerator with non-linear-bias-decorator.
    """

    @pytest.fixture
    def rng(self) -> IRandomNumberGenerator:
        secure_rng = SecureRandomNumberGenerator()
        return NonLinearBiasedRandomNumberGeneratorDecorator(secure_rng, base_bias=0.1)


class TestBaseRandomNumberGeneratorWithNoisyBiasedDeco(IRandomNumberGeneratorTest):
    """
    Test class for BaseRandomNumberGenerator with noisy-bias-decorator.
    """

    @pytest.fixture
    def rng(self) -> IRandomNumberGenerator:
        base_rng = BaseRandomNumberGenerator()
        return NoisyBiasedRandomNumberGeneratorDecorator(base_rng, base_bias=0.1)


class TestSecureRandomNumberGeneratorWithNoisyBiasedDeco(IRandomNumberGeneratorTest):
    """
    Test class for SecureRandomNumberGenerator with noisy-bias-decorator.
    """

    @pytest.fixture
    def rng(self) -> IRandomNumberGenerator:
        secure_rng = SecureRandomNumberGenerator()
        return NoisyBiasedRandomNumberGeneratorDecorator(secure_rng, base_bias=0.1)


class TestBiasedRandomNumberGeneratorDecoratorWithBaseImpl:
    """
    Additional tests for BiasedRandomNumberGeneratorDecorator to verify bias functionality.
    """

    @pytest.fixture
    def biased_rng(self) -> IRandomNumberGenerator:
        base_rng = BaseRandomNumberGenerator()
        return BiasedRandomNumberGeneratorDecorator(base_rng, base_bias=0.1)

    def test_with_bias(self, biased_rng: IRandomNumberGenerator):
        value = biased_rng.random()
        assert 0.0 <= value <= 1.0
        assert value >= 0.1

    def test_sequence_with_bias(self, biased_rng: IRandomNumberGenerator):
        length = 10
        sequence = biased_rng.sequence(length)
        assert len(sequence) == length
        assert all(0.0 <= value <= 1.0 for value in sequence)
        assert all(value >= 0.1 for value in sequence)

    def test_int_with_bias(self, biased_rng: IRandomNumberGenerator):
        min_value = 1
        max_value = 10
        value = biased_rng.int(min_value, max_value)
        assert min_value <= value <= max_value

    def test_float_with_bias(self, biased_rng: IRandomNumberGenerator):
        min_value = 1.0
        max_value = 10.0
        value = biased_rng.float(min_value, max_value)
        assert min_value <= value <= max_value
        assert value >= min_value + 0.1 * (max_value - min_value)

    def test_choice_with_bias(self, biased_rng: IRandomNumberGenerator):
        sequence = [1, 2, 3, 4, 5]
        value = biased_rng.choice(sequence)
        assert value in sequence


class TestBiasedRandomNumberGeneratorDecoratorWithSecureImpl:
    @pytest.fixture
    def biased_rng(self) -> IRandomNumberGenerator:
        secure_rng = SecureRandomNumberGenerator()
        return BiasedRandomNumberGeneratorDecorator(secure_rng, base_bias=0.1)
