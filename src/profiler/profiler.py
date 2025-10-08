"""Module for profiling executables within a project."""

import os
import subprocess
import time
from .. import general

STATS_EXECUTION_TIME_FIELD = "execution_time"


def _executable_choose(files):
    return files[0]


def _choose_executable(build: general.Build) -> str:
    executables = []
    files = os.listdir(os.path.join(build.build_path))
    for file in files:
        if os.path.isdir(os.path.join(build.build_path, file)):
            continue

        with open(os.path.join(build.build_path, file), "rb") as data:
            _bytes = data.read(4)
            if _bytes[:2] == "MZ" or _bytes == b"\x7fELF":
                executables.append(file)

    return os.path.join(build.build_path, _executable_choose(executables))


class Profiler:
    """Class for profiling an executable within a project."""

    def __init__(self, build: general.Build, executable: str = ""):
        self.build = build
        if executable == "":
            self.executable = _choose_executable(build)
        else:
            self.executable = executable

        self.stats: dict[str, str] = {}

    def execution_time(self):
        """Measure execution time of the executable."""
        start_time = time.time()
        with subprocess.Popen(
            [self.executable],
            cwd=self.build.build_path,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        ) as process:
            process.wait()

        end_time = time.time()
        self.stats.update({STATS_EXECUTION_TIME_FIELD: str(end_time - start_time)})

    def perf_stat_collect(self):
        """Collect performance statistics using 'perf stat'."""
        raise NotImplementedError

    def perf_record_collect(self):
        """Collect performance records using 'perf record'."""
        raise NotImplementedError

    def save_stats(self):
        """Save collected statistics to a file."""
        raise NotImplementedError


if __name__ == "__main__":
    raise NotImplementedError
