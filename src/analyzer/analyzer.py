"""Module that analyzes project's repository and creates file with its information"""

import glob
import os
import json


class Analyzer:
    """Class that analyzes project's repository and creates file with its information"""

    build_systems_list = {
        "**/CMakeLists.txt": "cmake",
        "**/*.cmake": "cmake",
        "**/configure.ac": "autoconf",
        "**/*meson": "meson",
        "**/*bazel": "bazel",
    }

    def __init__(self, repo_path: str):
        self.repo_path = repo_path
        self.results = {
            "tests": False,
            "benchmarks": False,
            "ci": False,
            "build_systems": {
                "cmake": False,
                "autoconf": False,
                "meson": False,
                "bazel": False,
            },
            "dependencies": [],
        }

    def _search_tests(self):
        if glob.glob(os.path.join(self.repo_path, "**/*test*"), recursive=True):
            self.results["tests"] = True

    def _search_benchmarks(self):
        if glob.glob(os.path.join(self.repo_path, "**/*benchmark*"), recursive=True):
            self.results["benchmarks"] = True

    def _search_ci(self):
        if glob.glob(os.path.join(self.repo_path, "**/ci"), recursive=True):
            self.results["ci"] = True

        if glob.glob(
            os.path.join(self.repo_path, "**/.github/workflows/*.yml"), recursive=True
        ):
            self.results["ci"] = True

    def _search_build_systems(self):
        for pattern, system in self.build_systems_list.items():
            if glob.glob(os.path.join(self.repo_path, pattern), recursive=True):
                self.results["build_systems"][system] = True

    def _search_dependencies(self):
        dep_path = os.path.join(self.repo_path, "third_party")
        if os.path.exists(dep_path):
            dirs = [
                d
                for d in os.listdir(dep_path)
                if os.path.isdir(os.path.join(dep_path, d))
            ]
            self.results["dependencies"].extend(dirs)

    def analyze(self):
        """Analyzes project and collects its information"""
        print(f"Analyzing {self.repo_path}\n")

        self._search_tests()
        self._search_benchmarks()
        self._search_ci()
        self._search_build_systems()
        self._search_dependencies()

        print("Analyzing done\n")

        with open("amphimixis.log", "w", encoding="utf8") as file:
            json.dump(self.results, file, indent=4)
