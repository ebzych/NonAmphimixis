"""Module for configuring a new build"""

import os
import json
import general


def configure(
    project: general.Project,
    build_path: str,
    machine: general.RemoteMachine,
    is_specified_script: bool,
    specified_script: str,
    build_system: general.IBuildSystem,
    config_flags: str,
    compiler_flags: str,
    runner: general.IBuildSystem,
):
    """Function to configure a new build and save its configuration to a JSON file"""

    project.build_system = build_system
    project.runner = runner

    build_name = input("Name current build:\n")
    build_path = os.path.join(build_path, build_name)
    os.makedirs(build_path, exist_ok=True)

    build = general.Build(machine, build_path)
    build.is_specified_script = is_specified_script
    build.specified_script = specified_script
    build.config_flags = config_flags
    build.compiler_flags = compiler_flags

    project.builds.append(build)

    config = build.__dict__

    config_path = os.path.join(build_path, "config.json")
    with open(config_path, "w", encoding="UTF-8") as file:
        json.dump(config, file, indent=4)
