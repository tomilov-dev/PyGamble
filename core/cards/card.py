import sys
from pathlib import Path
from enum import Enum
from pydantic import BaseModel


class SuitDDM(str, Enum):
    """
    Represents a suit of playing cards.
    """

    HEARTS = "Hearts"
    DIAMONDS = "Diamonds"
    CLUBS = "Clubs"
    SPADES = "Spades"

    def __str__(self) -> str:
        return self.value


class RankDDM(str, Enum):
    """
    Represents a rank of playing cards.
    """

    TWO = "2"
    THREE = "3"
    FOUR = "4"
    FIVE = "5"
    SIX = "6"
    SEVEN = "7"
    EIGHT = "8"
    NINE = "9"
    TEN = "10"
    JACK = "Jack"
    QUEEN = "Queen"
    KING = "King"
    ACE = "Ace"

    def __str__(self) -> str:
        return self.value


class CardDDM(BaseModel):
    """
    Represents a playing card with a suit and a rank.
    """

    suit: SuitDDM
    rank: RankDDM

    def __str__(self) -> str:
        return f"{self.rank} of {self.suit}"

    def __hash__(self) -> int:
        return hash((self.suit, self.rank))

    def __eq__(self, other) -> bool:
        if isinstance(other, CardDDM):
            return self.suit == other.suit and self.rank == other.rank
        return False
