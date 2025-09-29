"""Module for configuring a new build"""

from os import path, getcwd
import pickle
import yaml
import general


def parse_config(project: general.Project) -> None:
    """Module enter function"""

    project.builds = []
    with open("input.yml", "r", encoding="UTF-8") as f:
        input_config = yaml.safe_load(f)

        if not isinstance(input_config["build_system"], str):
            raise TypeError("Invalid build system type :(, look config file")

        project.build_system = general.build_systems_dict[
            input_config["build_system"].lower()
        ]

        if not isinstance(input_config["runner"], str):
            raise TypeError("Invalid runner type ^~^, look config file")

        project.runner = general.build_systems_dict[input_config["runner"].lower()]

        for build in input_config["builds"]:
            configure(
                project,
                get_by_id(input_config["platforms"], build["platform_id"]),
                get_by_id(input_config["receipts"], build["receipt_id"]),
            )


def configure(
    project: general.Project,
    platform_info: dict[str, str],
    receipt_info: dict[str, str],
) -> None:
    """Function to configure a new build and save its configuration to a Pickle file"""

    build_path = generate_build_path(platform_info["id"], receipt_info["id"])

    auth = general.MachineAuthenticationInfo(
        platform_info["username"], platform_info["password"], int(platform_info["port"])
    )

    machine = general.MachineInfo(
        general.Arch(platform_info["arch"].lower()), platform_info["ip"], auth
    )

    if "script" in receipt_info:
        build = general.Build(machine, build_path, True, receipt_info["script"])
    else:
        build = general.Build(machine, build_path, False)

    build.config_flags = receipt_info["config_flags"]
    build.compiler_flags = receipt_info["compiler_flags"]

    project.builds.append(build)

    config = build.__dict__

    config_name = f"{platform_info['id']}_{receipt_info['id']}_config"
    with open(config_name, "wb") as file:
        pickle.dump(config, file)


def generate_build_path(platform_id: str, receipt_id: str) -> str:
    """Function to create path to build depending on platform and receipt id"""

    return path.join(getcwd(), f"{platform_id}_{receipt_id}")


def get_by_id(items: list[dict[str, str]], target_id: str) -> dict[str, str]:
    """Finds platform or receipt by id"""

    for item in items:
        if item["id"] == target_id:
            return item
    return {}
