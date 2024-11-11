import sys
from pathlib import Path
import secrets
from typing import Any

ROOT_DIR = Path(__file__).parent.parent
sys.path.append(str(ROOT_DIR))
from rng.base import IRandomNumberGenerator


class SecureRandomNumberGenerator(IRandomNumberGenerator):
    """
    Implementation of a random number generator using the secrets module for cryptographic security.

    This class provides methods to generate cryptographically secure random numbers and sequences.
    It uses the secrets.SystemRandom class to ensure that the random numbers are suitable for security-sensitive applications.
    """

    def random(self) -> float:
        return secrets.SystemRandom().random()

    def sequence(self, length: int) -> list[float]:
        return [secrets.SystemRandom().random() for _ in range(length)]

    def int(self, min_value: int, max_value: int) -> int:
        return secrets.randbelow(max_value - min_value + 1) + min_value

    def float(self, min_value: float, max_value: float) -> float:
        return min_value + (max_value - min_value) * secrets.SystemRandom().random()

    def choice(self, sequence: list) -> Any:
        return secrets.choice(sequence)

    def shuffle(self, sequence: list[Any]) -> None:
        secrets.SystemRandom().shuffle(sequence)
