"""SSH shell handler implementation."""

import paramiko
from .shell_interface import IShell


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
