"""Module that analyzes project's repository and creates file with its information"""

import glob
import os
import json


class Analyzer:
    """Class that analyzes project's repository and creates file with its information"""

    ci_list = ["**/ci", "**/.github/workflows/*.yml"]

    build_systems_list = {
        "**/CMakeLists.txt": "cmake",
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
        if self.results["tests"] is True:
            print("tests: found")
        else:
            print("tests: not found")

    def _search_benchmarks(self):
        if glob.glob(os.path.join(self.repo_path, "**/*benchmark*"), recursive=True):
            self.results["benchmarks"] = True
        if self.results["benchmarks"] is True:
            print("benchmarks: found")
        else:
            print("benchmarks: not found")

    def _search_ci(self):
        for pattern in self.ci_list:
            if glob.glob(os.path.join(self.repo_path, pattern), recursive=True):
                self.results["ci"] = True
        if self.results["ci"] is True:
            print("ci: found")
        else:
            print("ci: not found")

    def _search_build_systems(self):
        print("build systems:")
        for pattern, system in self.build_systems_list.items():
            if glob.glob(os.path.join(self.repo_path, pattern), recursive=True):
                self.results["build_systems"][system] = True
            if self.results["build_systems"][system] is True:
                print(f"\t{system}")

    def _search_dependencies(self):
        dep_path = os.path.join(self.repo_path, "third_party")
        if os.path.exists(dep_path):
            dirs = [
                d
                for d in os.listdir(dep_path)
                if os.path.isdir(os.path.join(dep_path, d))
            ]
            self.results["dependencies"].extend(dirs)
        print("dependencies:")
        if self.results["dependencies"]:
            for dep in self.results["dependencies"]:
                print(f"\t{dep}")
        else:
            print("\tnot found")

    def analyze(self):
        """Analyzes project and collects its information"""

        if not os.path.exists(self.repo_path):
            print("Directory not found")
            return

        print(f"Analyzing {self.repo_path}\n")

        self._search_tests()
        self._search_benchmarks()
        self._search_ci()
        self._search_build_systems()
        self._search_dependencies()

        with open("amphimixis.log", "w", encoding="utf8") as file:
            json.dump(self.results, file, indent=4)
            print()
