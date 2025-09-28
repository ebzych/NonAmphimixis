"""Module for shell operations."""

import os
from abc import ABC, abstractmethod
import ipaddress
import subprocess
import paramiko


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


class Shell:
    """Shell class to manage shell operations."""

    def __init__(self, ip: str, port: str, username: str, password: str):
        self._shell: IShell
        self.username = username
        self.password = password
        self.ip = ipaddress.ip_address(ip)
        self.port = port

    def connect(self):
        """Connect to the shell based on the IP address."""
        if self.ip.is_loopback:
            self._shell = _LocalShellHandler()
        else:
            self._shell = _SSHHandler(
                str(self.ip), int(self.port), self.username, self.password
            )

    def run(self, command: str):
        """Run the command through the shell."""
        self._shell.run(command)

    def readline(self) -> str:
        """Read a line from the shell output."""
        return self._shell.readline()


class _SSHHandler(IShell):
    def __init__(self, ip: str, port: int, username: str, password: str | None):
        self.ip = ip
        self.port = port
        self.username = username
        self.password = password
        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.ssh.connect(
            self.ip, self.port, username=self.username, password=self.password
        )
        channel = self.ssh.invoke_shell()
        self.stdin = channel.makefile("wb")
        self.stdout = channel.makefile("r")

    def __del__(self):
        self.ssh.close()
        try:
            self.stdout.close()
            self.stdin.close()
        except AttributeError:
            pass

    def run(self, command: str):
        if self.stdin is None:
            raise BrokenPipeError("Can't write to process' stdin")

        cmd_bytes = command.encode("UTF-8")

        self.stdin.write(cmd_bytes)
        self.stdin.write(b"\n")
        self.stdin.flush()

    def readline(self) -> str:
        if self.stdout is None:
            raise BrokenPipeError("Can't read from process' stdout")
        return self.stdout.readline()


class _LocalShellHandler(IShell):
    def __init__(self):
        default_shell = os.getenv("SHELL")
        if default_shell is None:
            raise TypeError("Can't get default shell path")
        self.shell = subprocess.Popen(
            [default_shell],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
        )

    def __del__(self):
        self.shell.kill()
        self.shell.wait()

    def run(self, command: str):
        if self.shell.stdin is None:
            raise BrokenPipeError("Can't write to process' stdin")

        cmd_bytes = command.encode("UTF-8")

        if self.shell.stdin.write(cmd_bytes) != len(cmd_bytes):
            raise IOError("Not all data has been written")

        if self.shell.stdin.write(b"\n") != 1:
            raise IOError("Not all data has been written")

        self.shell.stdin.flush()

    def readline(self) -> str:
        if self.shell.stdout is None:
            raise BrokenPipeError("Can't read from process' stdout")
        return self.shell.stdout.readline().decode()
