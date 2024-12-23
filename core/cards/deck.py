import sys
from pathlib import Path
from enum import Enum
from typing import Hashable
from pydantic import BaseModel
from pydantic import field_validator


ROOT_DIR = Path(__file__).parent.parent
sys.path.append(str(ROOT_DIR))
from rng.base import IRandomNumberGenerator
from rng.base import BaseRandomNumberGenerator
from cards.card import CardDDM
from cards.card import SuitDDM
from cards.card import RankDDM


class DeckDDM(BaseModel):
    """
    Represents a deck of playing cards.
    """

    cards: list[CardDDM] = []

    def __init__(self, size: int = 52) -> None:
        super().__init__()
        if size == 52:
            self.cards = [
                CardDDM(suit=suit, rank=rank) for suit in SuitDDM for rank in RankDDM
            ]
        elif size == 36:
            self.cards = [
                CardDDM(suit=suit, rank=rank)
                for suit in SuitDDM
                for rank in list(RankDDM)[4:]
            ]
        else:
            raise ValueError("Invalid deck size. Only 52 and 36 are supported.")


class PlayerHandDDM(BaseModel):
    """
    Represents a player's hand.
    """

    player_id: Hashable
    cards: list[CardDDM] = []

    def add_card(self, card: CardDDM) -> None:
        self.cards.append(card)

    def remove_card(self, card: CardDDM) -> None:
        self.cards.remove(card)


class DeckManager:
    """
    Represents a deck of playing cards.
    """

    def __init__(
        self,
        rng: IRandomNumberGenerator,
        deck: DeckDDM,
    ) -> None:
        self.rng = rng
        self.deck = deck

    def shuffle(self) -> None:
        """
        Shuffle the deck of cards using the provided random number generator.
        """

        self.rng.shuffle(self.deck.cards)

    def deal(self, num_cards: int) -> list[CardDDM]:
        """
        Deal a number of cards from the deck.

        :param num_cards: The number of cards to deal.
        :return: A list of dealt cards.
        """

        if num_cards > len(self.deck.cards):
            raise ValueError(
                "Not enough cards in the deck to deal the requested number of cards."
            )

        dealt_cards = self.deck.cards[:num_cards]
        self.deck.cards = self.deck.cards[num_cards:]
        return dealt_cards

    def __str__(self) -> str:
        return f"Deck of {len(self.deck.cards)} cards"
