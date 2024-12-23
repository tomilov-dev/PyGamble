import sys
from pathlib import Path
import pytest

ROOT_DIR = Path(__file__).parent.parent.parent
sys.path.append(str(ROOT_DIR))

from rng.base import BaseRandomNumberGenerator
from cards.card import CardDDM, SuitDDM, RankDDM
from cards.deck import DeckDDM, DeckManager, PlayerHandDDM


def test_deck_initialization():
    deck = DeckDDM(size=52)
    assert len(deck.cards) == 52
    assert all(isinstance(card, CardDDM) for card in deck.cards)

    deck = DeckDDM(size=36)
    assert len(deck.cards) == 36
    assert all(isinstance(card, CardDDM) for card in deck.cards)

    with pytest.raises(ValueError):
        DeckDDM(size=40)


def test_deck_manager_shuffle():
    rng = BaseRandomNumberGenerator()
    deck = DeckDDM(size=52)
    manager = DeckManager(rng=rng, deck=deck)

    original_order = deck.cards.copy()
    manager.shuffle()
    assert len(deck.cards) == 52
    assert set(deck.cards) == set(original_order)
    assert deck.cards != original_order


def test_deck_manager_deal():
    rng = BaseRandomNumberGenerator()
    deck = DeckDDM(size=52)
    manager = DeckManager(rng=rng, deck=deck)

    dealt_cards = manager.deal(5)
    assert len(dealt_cards) == 5
    assert len(deck.cards) == 47

    with pytest.raises(ValueError):
        manager.deal(48)


def test_player_hand_add_card():
    player_hand = PlayerHandDDM(player_id=1)
    card = CardDDM(suit=SuitDDM.HEARTS, rank=RankDDM.ACE)
    player_hand.add_card(card)
    assert len(player_hand.cards) == 1
    assert player_hand.cards[0] == card


def test_player_hand_remove_card():
    player_hand = PlayerHandDDM(player_id=1)
    card = CardDDM(suit=SuitDDM.HEARTS, rank=RankDDM.ACE)
    player_hand.add_card(card)
    assert len(player_hand.cards) == 1
    player_hand.remove_card(card)
    assert len(player_hand.cards) == 0
