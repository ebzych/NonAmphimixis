"""Module that analyzes project's repository and creates file with its information"""


class Analyzer:
    """Class that analyzes project's repository and creates file with its information"""

    def __init__(self, repo_path: str):
        self.repo_path = repo_path

    def analyze(self):
        """Analyzes project and collects its information"""
        print(f"Analyzing {self.repo_path}")

    def create_project_file(self):
        """Creates file with information about project"""
        raise NotImplementedError
