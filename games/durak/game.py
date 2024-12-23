import sys
from pathlib import Path
from typing import Hashable

ROOT_DIR = Path(__file__).parent.parent
sys.path.append(str(ROOT_DIR))
from core.cards.card import CardDDM
from core.cards.card import SuitDDM
from core.cards.card import RankDDM
from core.cards.deck import DeckDDM
from core.cards.deck import PlayerHandDDM
from core.cards.deck import DeckManager
from core.player import PlayerDDM
from core.rng.base import IRandomNumberGenerator


class DurakGame:
    """
    Represents a game of Durak.
    """

    def __init__(
        self,
        deck_size: int,
        players: list[PlayerDDM],
        rng: IRandomNumberGenerator,
    ) -> None:
        if len(players) * 6 > deck_size:
            raise ValueError("Not enough cards in the deck to deal to all players.")

        self.players = players
        self.deck = DeckDDM(size=deck_size)
        self.manager = DeckManager(rng=rng, deck=self.deck)
        self.manager.shuffle()

        self.players_hands = {
            player.id: PlayerHandDDM(player_id=player.id) for player in self.players
        }
        self.trump_card = self.deck.cards[-1]
        self.trump_suit = self.trump_card.suit
        self.deal_initial_cards()

        self.current_attacker_index = 0
        self.current_defender_index = 1

    def deal_initial_cards(self) -> None:
        for _ in range(6):
            for hand in self.players_hands.values():
                hand.add_card(self.manager.deal(1)[0])

    def play_turn(
        self,
        attacker_id: Hashable,
        defender_id: Hashable,
        attack_card: CardDDM,
        defend_card: CardDDM | None = None,
    ) -> bool:
        attacker_hand = self.players_hands[attacker_id].cards
        defender_hand = self.players_hands[defender_id].cards

        if attack_card not in attacker_hand:
            raise ValueError("Attacker does not have the specified card.")

        attacker_hand.remove(attack_card)
        print(f"Attacker plays: {attack_card}")

        if not defend_card:
            print("Defender cannot beat the card and takes it.")
            defender_hand.append(attack_card)
            return False

        if defend_card not in defender_hand:
            raise ValueError("Defender does not have the specified card.")

        if (
            defend_card.suit == attack_card.suit and defend_card.rank > attack_card.rank
        ) or (
            defend_card.suit == self.trump_suit and attack_card.suit != self.trump_suit
        ):
            defender_hand.remove(defend_card)
            print(f"Defender beats with: {defend_card}")
            return True
        else:
            raise ValueError("Defend card is not valid.")

    def next_turn(self) -> None:
        self.current_attacker_index = (self.current_attacker_index + 1) % len(
            self.players
        )
        self.current_defender_index = (self.current_defender_index + 1) % len(
            self.players
        )

    def __str__(self) -> str:
        return f"Trump card: {self.trump_card}, Players' hands: {self.players_hands}"
