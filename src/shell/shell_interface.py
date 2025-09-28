"""Shell handler interface"""

from abc import ABC, abstractmethod


class IShell(ABC):
    """Abstract base class for shell handlers."""

    @abstractmethod
    def run(self, command: str):
        """Run a command in the shell."""
        raise NotImplementedError

    @abstractmethod
    def readline(self):
        """Read a line from the shell output."""
        raise NotImplementedError
