"""Module that analyzes project's repository and creates file with its information"""

import glob
import os


class Analyzer:
    """Class that analyzes project's repository and creates file with its information"""

    def __init__(self, repo_path: str):
        self.repo_path = repo_path

    def analyze(self):
        """Analyzes project and collects its information"""
        print(f"Analyzing {self.repo_path}\n")

        results = {
            "tests": False,
            "benchmarks": False,
            "ci": False,
            "build_systems": {
                "cmake": False,
                "autoconf": False,
                "meson": False,
                "ninja": False,
                "bazel": False,
            },
            "dependencies": [],
        }

        if glob.glob(os.path.join(self.repo_path, "**/*test*"), recursive=True):
            results["tests"] = True

        if glob.glob(os.path.join(self.repo_path, "**/*benchmark*"), recursive=True):
            results["benchmarks"] = True

        if glob.glob(os.path.join(self.repo_path, "**/ci"), recursive=True):
            results["ci"] = True

        if glob.glob(
            os.path.join(self.repo_path, "**/.github/workflows/*.yml"), recursive=True
        ):
            results["ci"] = True

        if glob.glob(os.path.join(self.repo_path, "**/CMakeLists.txt"), recursive=True):
            results["build_systems"]["cmake"] = True

        if glob.glob(os.path.join(self.repo_path, "**/*.cmake"), recursive=True):
            results["build_systems"]["cmake"] = True

        if glob.glob(os.path.join(self.repo_path, "**/configure.ac"), recursive=True):
            results["build_systems"]["autoconf"] = True

        if glob.glob(os.path.join(self.repo_path, "**/*meson"), recursive=True):
            results["build_systems"]["meson"] = True

        if glob.glob(os.path.join(self.repo_path, "**/*ninja"), recursive=True):
            results["build_systems"]["ninja"] = True

        if glob.glob(os.path.join(self.repo_path, "**/*bazel"), recursive=True):
            results["build_systems"]["bazel"] = True

        dep_path = os.path.join(self.repo_path, "third_party")
        if os.path.exists(dep_path):
            dirs = [
                d
                for d in os.listdir(dep_path)
                if os.path.isdir(os.path.join(dep_path, d))
            ]
            results["dependencies"].extend(dirs)

        print("Analyzing done\n")

        with open("amphimixis.log", "a+", encoding="utf8") as file:
            for key, value in results.items():
                if key == "build_systems":
                    print("build_systems:")
                    for key2, value2 in results["build_systems"].items():
                        if value2:
                            file.write(f"\t-{key2}\n")
                            print("\t-", key2)
                elif key == "dependencies":
                    if value:
                        file.write(f"{key}:\n")
                        print(f"{key}:")
                        for dep in value:
                            file.write(f"\t-{dep}\n")
                            print("\t-", dep)
                    else:
                        file.write(f"{key}: could not find\n")
                        print(f"{key}: could not find")
                else:
                    line = f"{key}: {'found' if value else 'could not find'}"
                    file.write(line + "\n")
                    print(line)

        return results
