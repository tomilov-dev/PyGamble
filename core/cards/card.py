import sys
from pathlib import Path


ROOT_DIR = Path(__file__).parent.parent
sys.path.append(str(ROOT_DIR))
from rng.base import IRandomNumberGenerator


class Suit:
    """
    Represents a suit of playing cards.
    """

    suits = ["Hearts", "Diamonds", "Clubs", "Spades"]

    def __init__(self, name: str) -> None:
        if name not in Suit.suits:
            raise ValueError(f"Invalid suit: {name}")
        self.name = name

    def __repr__(self) -> str:
        return self.name


class Rank:
    """
    Represents a rank of playing cards.
    """

    ranks = [
        "2",
        "3",
        "4",
        "5",
        "6",
        "7",
        "8",
        "9",
        "10",
        "Jack",
        "Queen",
        "King",
        "Ace",
    ]

    def __init__(self, name: str) -> None:
        if name not in Rank.ranks:
            raise ValueError(f"Invalid rank: {name}")
        self.name = name

    def __repr__(self) -> str:
        return self.name


class Card:
    """
    Represents a playing card with a suit and a rank.
    """

    def __init__(self, suit: Suit, rank: Rank) -> None:
        self.suit = suit
        self.rank = rank

    def __repr__(self) -> str:
        return f"{self.rank} of {self.suit}"


class Deck:
    """
    Represents a deck of playing cards.
    """

    def __init__(self, rng: IRandomNumberGenerator) -> None:
        self.rng = rng
        self.cards: list[Card] = [
            Card(Suit(suit), Rank(rank)) for suit in Suit.suits for rank in Rank.ranks
        ]
        self.shuffle()

    def shuffle(self) -> None:
        """
        Shuffle the deck of cards using the provided random number generator.
        """
        self.rng.shuffle(self.cards)

    def deal(self, num_cards: int) -> list[Card]:
        """
        Deal a number of cards from the deck.

        :param num_cards: The number of cards to deal.
        :return: A list of dealt cards.
        """
        if num_cards > len(self.cards):
            raise ValueError(
                "Not enough cards in the deck to deal the requested number of cards."
            )
        dealt_cards = self.cards[:num_cards]
        self.cards = self.cards[num_cards:]
        return dealt_cards

    def __repr__(self) -> str:
        return f"Deck of {len(self.cards)} cards"
