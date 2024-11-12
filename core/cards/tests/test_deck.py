import sys
from pathlib import Path
import pytest

ROOT_DIR = Path(__file__).parent.parent.parent
sys.path.append(str(ROOT_DIR))

from rng.base import BaseRandomNumberGenerator
from cards.card import CardDDM
from cards.deck import Deck
from cards.deck import DeckManager


def test_deck_initialization():
    deck = Deck(size=52)
    assert len(deck.cards) == 52
    assert all(isinstance(card, CardDDM) for card in deck.cards)

    deck = Deck(size=36)
    assert len(deck.cards) == 36
    assert all(isinstance(card, CardDDM) for card in deck.cards)

    with pytest.raises(ValueError):
        Deck(size=40)


def test_deck_manager_shuffle():
    rng = BaseRandomNumberGenerator()
    deck = Deck(size=52)
    manager = DeckManager(rng=rng, deck=deck)

    original_order = deck.cards.copy()
    manager.shuffle()
    assert len(deck.cards) == 52
    assert set(deck.cards) == set(original_order)
    assert deck.cards != original_order


def test_deck_manager_deal():
    rng = BaseRandomNumberGenerator()
    deck = Deck(size=52)
    manager = DeckManager(rng=rng, deck=deck)

    dealt_cards = manager.deal(5)
    assert len(dealt_cards) == 5
    assert len(deck.cards) == 47

    with pytest.raises(ValueError):
        manager.deal(48)
