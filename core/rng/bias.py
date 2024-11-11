import sys
from pathlib import Path
import random
from typing import Any
from typing import Callable

ROOT_DIR = Path(__file__).parent.parent
sys.path.append(str(ROOT_DIR))
from rng.base import IRandomNumberGenerator


class BiasedRandomNumberGeneratorDecorator(IRandomNumberGenerator):
    """
    Implementation of a biased random number generator.

    This class decorates an existing IRandomNumberGenerator implementation and adds a bias to the generated random numbers.
    The bias can be positive or negative, shifting the results up or down respectively.

    Attributes:
        rng (IRandomNumberGenerator): The underlying random number generator to be biased.
        bias (float): The bias to be applied to the random numbers. Positive values shift results up, negative values shift results down.
    """

    def __init__(self, rng: IRandomNumberGenerator, base_bias: float = 0.0) -> None:
        """
        Initialize the biased random number generator.

        :param rng: The IRandomNumberGenerator implementation to be biased.
        :param base_bias: The base_bias to be applied to the random numbers. Positive values shift results up, negative values shift results down.
        """
        self.rng = rng
        self.base_bias = base_bias

    def random(self) -> float:
        return min(max(self.rng.random() + self.base_bias, 0.0), 0.9999999999999999)

    def sequence(self, length: int) -> list[float]:
        return [self.random() for _ in range(length)]

    def int(self, min_value: int, max_value: int) -> int:
        biased_value = self.rng.float(min_value, max_value) + self.base_bias * (
            max_value - min_value
        )
        return int(min(max(biased_value, min_value), max_value))

    def float(self, min_value: float, max_value: float) -> float:
        return min(
            max(
                self.rng.float(min_value, max_value)
                + self.base_bias * (max_value - min_value),
                min_value,
            ),
            max_value,
        )

    def choice(self, sequence: list) -> Any:
        index = int(
            min(max(self.rng.random() + self.base_bias, 0.0), 0.9999999999999999)
            * len(sequence)
        )
        return sequence[min(index, len(sequence) - 1)]

    def shuffle(self, sequence: list[Any]) -> None:
        for i in range(len(sequence) - 1, 0, -1):
            j = self.int(0, i)
            sequence[i], sequence[j] = sequence[j], sequence[i]


class RandomBiasedRandomNumberGeneratorDecorator(IRandomNumberGenerator):
    """
    Implementation of a random biased random number generator.

    This class decorates an existing IRandomNumberGenerator implementation and adds a random bias to the generated random numbers.
    The bias is applied in a random manner to make it harder to detect.

    Attributes:
        rng (IRandomNumberGenerator): The underlying random number generator to be biased.
        base_bias (float): The base bias to be applied to the random numbers.
        bias_distribution (Callable[[], float]): The function to generate the random bias.
    """

    def __init__(
        self,
        rng: IRandomNumberGenerator,
        base_bias: float = 0.0,
        bias_distribution: Callable[[], float] = lambda: random.uniform(0.5, 1.5),
    ) -> None:
        """
        Initialize the random biased random number generator.

        :param rng: The IRandomNumberGenerator implementation to be biased.
        :param base_bias: The base bias to be applied to the random numbers.
        :param bias_distribution: The function to generate the random bias. Default is random.uniform(0.5, 1.5).
        """
        self.rng = rng
        self.base_bias = base_bias
        self.bias_distribution = bias_distribution

    def random(self) -> float:
        bias = self.base_bias * self.bias_distribution()
        return min(max(self.rng.random() + bias, 0.0), 0.9999999999999999)

    def sequence(self, length: int) -> list[float]:
        return [self.random() for _ in range(length)]

    def int(self, min_value: int, max_value: int) -> int:
        biased_value = self.float(min_value, max_value)
        return int(min(max(biased_value, min_value), max_value))

    def float(self, min_value: float, max_value: float) -> float:
        bias = self.base_bias * self.bias_distribution()
        return min(
            max(self.rng.float(min_value, max_value) + bias, min_value),
            max_value,
        )

    def choice(self, sequence: list) -> Any:
        index = int(self.random() * len(sequence))
        return sequence[min(index, len(sequence) - 1)]

    def shuffle(self, sequence: list[Any]) -> None:
        for i in range(len(sequence) - 1, 0, -1):
            j = self.int(0, i)
            sequence[i], sequence[j] = sequence[j], sequence[i]


class NonLinearBiasedRandomNumberGeneratorDecorator(IRandomNumberGenerator):
    """
    Implementation of a non-linear biased random number generator.

    This class decorates an existing IRandomNumberGenerator implementation and adds a non-linear bias to the generated random numbers.
    The bias is applied in a non-linear manner to make it harder to detect.

    Attributes:
        rng (IRandomNumberGenerator): The underlying random number generator to be biased.
        base_bias (float): The base bias to be applied to the random numbers.
        bias_function (Callable[[float], float]): The function to apply the non-linear bias.
    """

    def __init__(
        self,
        rng: IRandomNumberGenerator,
        base_bias: float = 0.0,
        bias_function: Callable[[float], float] = lambda x: x**2,
    ) -> None:
        """
        Initialize the non-linear biased random number generator.

        :param rng: The IRandomNumberGenerator implementation to be biased.
        :param base_bias: The base bias to be applied to the random numbers.
        :param bias_function: The function to apply the non-linear bias. Default is x**2.
        """
        self.rng = rng
        self.base_bias = base_bias
        self.bias_function = bias_function

    def random(self) -> float:
        value = self.rng.random()
        bias = self.base_bias * (value**2)
        return min(max(value + bias, 0.0), 0.9999999999999999)

    def sequence(self, length: int) -> list[float]:
        return [self.random() for _ in range(length)]

    def int(self, min_value: int, max_value: int) -> int:
        biased_value = self.float(min_value, max_value)
        return int(min(max(biased_value, min_value), max_value))

    def float(self, min_value: float, max_value: float) -> float:
        value = self.rng.float(min_value, max_value)
        bias = self.base_bias * ((value - min_value) / (max_value - min_value)) ** 2
        return min(max(value + bias, min_value), max_value)

    def choice(self, sequence: list) -> Any:
        index = int(self.random() * len(sequence))
        return sequence[min(index, len(sequence) - 1)]

    def shuffle(self, sequence: list[Any]) -> None:
        for i in range(len(sequence) - 1, 0, -1):
            j = self.int(0, i)
            sequence[i], sequence[j] = sequence[j], sequence[i]


class NoisyBiasedRandomNumberGeneratorDecorator(IRandomNumberGenerator):
    """
    Implementation of a noisy biased random number generator.

    This class decorates an existing IRandomNumberGenerator implementation and adds noise to the generated random numbers.
    The noise is added to make the bias harder to detect.

    Attributes:
        rng (IRandomNumberGenerator): The underlying random number generator to be biased.
        base_bias (float): The base bias to be applied to the random numbers.
        noise_function (Callable[[], float]): The function to generate the noise.
    """

    def __init__(
        self,
        rng: IRandomNumberGenerator,
        base_bias: float = 0.0,
        noise_function: Callable[[], float] = lambda: random.uniform(-0.05, 0.05),
    ) -> None:
        """
        Initialize the noisy biased random number generator.

        :param rng: The IRandomNumberGenerator implementation to be biased.
        :param base_bias: The base bias to be applied to the random numbers.
        :param noise_function: The function to generate the noise. Default is random.uniform(-0.05, 0.05).
        """

        self.rng = rng
        self.base_bias = base_bias
        self.noise_function = noise_function

    def random(self) -> float:
        noise = self.noise_function()
        return min(
            max(self.rng.random() + self.base_bias + noise, 0.0),
            0.9999999999999999,
        )

    def sequence(self, length: int) -> list[float]:
        return [self.random() for _ in range(length)]

    def int(self, min_value: int, max_value: int) -> int:
        biased_value = self.float(min_value, max_value)
        return int(min(max(biased_value, min_value), max_value))

    def float(self, min_value: float, max_value: float) -> float:
        noise = self.noise_function()
        return min(
            max(
                self.rng.float(min_value, max_value) + self.base_bias + noise,
                min_value,
            ),
            max_value,
        )

    def choice(self, sequence: list) -> Any:
        index = int(self.random() * len(sequence))
        return sequence[min(index, len(sequence) - 1)]

    def shuffle(self, sequence: list[Any]) -> None:
        for i in range(len(sequence) - 1, 0, -1):
            j = self.int(0, i)
            sequence[i], sequence[j] = sequence[j], sequence[i]
