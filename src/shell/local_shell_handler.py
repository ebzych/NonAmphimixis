"""Local shell handler implementation."""

import os
import subprocess
from .shell_interface import IShell


class _LocalShellHandler(IShell):
    def __init__(self) -> None:
        default_shell = os.getenv("SHELL")
        if default_shell is None:
            raise TypeError("Can't get default shell path")
        self.shell = subprocess.Popen(
            [default_shell],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
        )

    def __del__(self) -> None:
        self.shell.kill()
        self.shell.wait()

    def run(self, command: str) -> None:
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
