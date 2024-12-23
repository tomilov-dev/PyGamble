import sys
from pathlib import Path
from abc import ABC, abstractmethod
from typing import Any, Hashable
from pydantic import BaseModel

ROOT_DIR = Path(__file__).parent
sys.path.append(str(ROOT_DIR))
from player import PlayerDDM
from state import GameStateDDM
from state import GameStateManager


class SessionNotfound(Exception):
    """
    Exception raised when a session is not found.
    """

    pass


class SessionDDM(BaseModel):
    """
    Data model for session.

    :param id: Unique identifier for the session.
    :param players: List of player identifiers associated with the session.
    """

    id: Hashable
    players: list[Hashable]


class SessionManager(ABC):
    """
    Abstract base class for managing sessions.
    """

    @abstractmethod
    def save(self, session: SessionDDM) -> None:
        """
        Save the session.

        :param session: The session to save.
        """

        pass

    @abstractmethod
    def load(self, session_id: Hashable) -> SessionDDM:
        """
        Load the session.

        :param session_id: The identifier of the session to load.
        :return: The loaded session.
        :raises SessionNotfound: If the session is not found.
        """

        pass

    @abstractmethod
    def delete(self, session_id: Hashable) -> None:
        """
        Delete the session.

        :param session_id: The identifier of the session to delete.
        :raises SessionNotfound: If the session is not found.
        """

        pass

    @abstractmethod
    def update(self, session: SessionDDM) -> None:
        """
        Update the session.

        :param session: The updated session.
        :raises SessionNotfound: If the session is not found.
        """

        pass


class GameSessionManager:
    """
    Manages a game session, including players and game state.
    """

    def __init__(
        self,
        session_id: Hashable,
        players: list[PlayerDDM],
        session_manager: SessionManager,
        state_manager: GameStateManager,
    ) -> None:
        """
        Initialize the game session manager.

        :param session_id: Unique identifier for the session.
        :param players: List of players in the session.
        :param session_manager: The session manager to handle session storage.
        :param state_manager: The game state manager to handle game state storage.
        """

        self.session_id = session_id
        self.players = players
        self.session_manager = session_manager
        self.state_manager = state_manager
        self.game_state: GameStateDDM | None = None

    def new_game(self, game_state: GameStateDDM) -> None:
        """
        Start a new game with the given game state.

        :param game_state: The initial game state for the new game.
        """

        self.game_state = game_state
        self.save_state()
        self.save_session()

    def save_state(self) -> None:
        """
        Save the current game state.
        """

        if self.game_state is None:
            raise ValueError("No game state to save.")
        self.state_manager.save(self.game_state)

    def load_state(self) -> None:
        """
        Load the current game state.
        """

        self.game_state = self.state_manager.load(self.session_id)

    def save_session(self) -> None:
        """
        Save the current session.
        """

        session = SessionDDM(
            id=self.session_id,
            players=[player.id for player in self.players],
        )
        self.session_manager.save(session)

    def load_session(self) -> None:
        """
        Load the current session.
        """

        session = self.session_manager.load(self.session_id)
        self.players = [PlayerDDM(id=id) for id in session.players]


class MemorySessionManager(SessionManager):
    """
    In-memory implementation of SessionManager.
    """

    def __init__(self):
        """
        Initialize the in-memory storage.
        """

        self.storage = {}

    def save(self, session: SessionDDM) -> None:
        """
        Save the session in memory.

        :param session: The session to save.
        """

        self.storage[session.id] = session

    def load(self, session_id: Hashable) -> SessionDDM:
        """
        Load the session from memory.

        :param session_id: The identifier of the session to load.
        :return: The loaded session.
        :raises SessionNotfound: If the session is not found.
        """

        session = self.storage.get(session_id)
        if session is None:
            raise SessionNotfound(f"Session {session_id} not found.")
        return session

    def delete(self, session_id: Hashable) -> None:
        """
        Delete the session from memory.

        :param session_id: The identifier of the session to delete.
        :raises SessionNotfound: If the session is not found.
        """

        if session_id not in self.storage:
            SessionNotfound(f"Session {session_id} not found.")
        del self.storage[session_id]

    def update(self, session: SessionDDM) -> None:
        """
        Update the session in memory.

        :param session: The updated session.
        :raises SessionNotfound: If the session is not found.
        """

        if session.id not in self.storage:
            raise SessionNotfound(f"Session {session.id} not found.")
        self.storage[session.id] = session
