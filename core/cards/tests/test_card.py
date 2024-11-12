import sys
from pathlib import Path

ROOT_DIR = Path(__file__).parent.parent.parent
sys.path.append(str(ROOT_DIR))

from cards.card import RankDDM
from cards.card import CardDDM
from cards.card import SuitDDM


def test_suit_ddm():
    assert str(SuitDDM.HEARTS) == "Hearts"
    assert str(SuitDDM.DIAMONDS) == "Diamonds"
    assert str(SuitDDM.CLUBS) == "Clubs"
    assert str(SuitDDM.SPADES) == "Spades"


def test_rank_ddm():
    assert str(RankDDM.TWO) == "2"
    assert str(RankDDM.THREE) == "3"
    assert str(RankDDM.FOUR) == "4"
    assert str(RankDDM.FIVE) == "5"
    assert str(RankDDM.SIX) == "6"
    assert str(RankDDM.SEVEN) == "7"
    assert str(RankDDM.EIGHT) == "8"
    assert str(RankDDM.NINE) == "9"
    assert str(RankDDM.TEN) == "10"
    assert str(RankDDM.JACK) == "Jack"
    assert str(RankDDM.QUEEN) == "Queen"
    assert str(RankDDM.KING) == "King"
    assert str(RankDDM.ACE) == "Ace"


def test_card_ddm():
    card = CardDDM(suit=SuitDDM.HEARTS, rank=RankDDM.ACE)
    assert card.suit == SuitDDM.HEARTS
    assert card.rank == RankDDM.ACE
    assert str(card) == "Ace of Hearts"

    card = CardDDM(suit=SuitDDM.CLUBS, rank=RankDDM.TEN)
    assert card.suit == SuitDDM.CLUBS
    assert card.rank == RankDDM.TEN
    assert str(card) == "10 of Clubs"
