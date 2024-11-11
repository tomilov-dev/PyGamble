import sys
from pathlib import Path
from abc import ABC, abstractmethod
from typing import Any
import random

ROOT_DIR = Path(__file__).parent.parent
sys.path.append(str(ROOT_DIR))


class IRandomNumberGenerator(ABC):
    """
    Interface for random number generators.
    """

    @abstractmethod
    def random(self) -> float:
        """
        Generate a random float in the range [0.0, 1.0).

        :return: A random float in the range [0.0, 1.0).
        """
        pass

    @abstractmethod
    def sequence(self, length: int) -> list[float]:
        """
        Generate a sequence of random floats in the range [0.0, 1.0).

        :param length: The length of the sequence.
        :return: A list of random floats.
        """
        pass

    @abstractmethod
    def int(self, min_value: int, max_value: int) -> int:
        """
        Generate a random integer in the range [min_value, max_value].

        :param min_value: The minimum value of the range.
        :param max_value: The maximum value of the range.
        :return: A random integer in the range [min_value, max_value].
        """
        pass

    @abstractmethod
    def float(self, min_value: float, max_value: float) -> float:
        """
        Generate a random float in the range [min_value, max_value].

        :param min_value: The minimum value of the range.
        :param max_value: The maximum value of the range.
        :return: A random float in the range [min_value, max_value].
        """
        pass

    @abstractmethod
    def choice(self, sequence: list[Any]) -> Any:
        """
        Return a random element from the sequence.

        :param sequence: The sequence of elements.
        :return: A random element from the sequence.
        """
        pass

    @abstractmethod
    def shuffle(self, sequence: list[Any]) -> None:
        """
        Shuffle the sequence in place.

        :param sequence: The sequence to shuffle.
        """
        pass


class BaseRandomNumberGenerator(IRandomNumberGenerator):
    """
    Basic implementation of a random number generator using the random module.
    """

    def random(self) -> float:
        return random.random()

    def sequence(self, length: int) -> list[float]:
        return [random.random() for _ in range(length)]

    def int(self, min_value: int, max_value: int) -> int:
        return random.randint(min_value, max_value)

    def float(self, min_value: float, max_value: float) -> float:
        return random.uniform(min_value, max_value)

    def choice(self, sequence: list[Any]) -> Any:
        return random.choice(sequence)

    def shuffle(self, sequence: list[Any]) -> None:
        random.shuffle(sequence)
