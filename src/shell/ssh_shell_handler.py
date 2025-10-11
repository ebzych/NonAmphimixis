"""SSH shell handler implementation."""

import subprocess
from .shell_interface import IShell

_CLEAR_OUTPUT_FLAG = b"CLEAR_OUTPUT_FLAG\n"


class _SSHHandler(IShell):

    def __init__(self, ip: str, port: int, username: str, password: str | None) -> None:
        self.ip = ip
        self.port = port
        self.username = username
        self.password = password
        # pylint: disable=consider-using-with
        self.ssh = subprocess.Popen(
            ["ssh", "-q", "-p", str(port), f"{username}@{ip}"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        if self.ssh.stdin is None or self.ssh.stdout is None:
            raise BrokenPipeError()

        self.ssh.stdin.write(b"echo ")
        self.ssh.stdin.write(_CLEAR_OUTPUT_FLAG)
        self.ssh.stdin.flush()
        for i in self.ssh.stdout:
            if i == _CLEAR_OUTPUT_FLAG:
                break

    def __del__(self) -> None:
        self.ssh.kill()
        try:
            self.ssh.stdout.close()
        except AttributeError:
            pass

        try:
            self.ssh.stdin.close()
        except AttributeError:
            pass

    def run(self, command: str) -> None:
        if self.ssh.stdin is None:
            raise BrokenPipeError("Can't write to process' stdin")

        cmd_bytes = command.encode("UTF-8")

        self.ssh.stdin.write(cmd_bytes)
        self.ssh.stdin.write(b"\n")
        self.ssh.stdin.flush()

    def readline(self) -> str:
        if self.ssh.stdout is None:
            raise BrokenPipeError("Can't read from process' stdout")

        line_bytes = self.ssh.stdout.readline()
        if not isinstance(line_bytes, bytes):
            raise TypeError("Can't read a line from ssh session")

        line = line_bytes.decode("UTF-8")
        return line
