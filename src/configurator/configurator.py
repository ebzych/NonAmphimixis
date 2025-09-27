"""Module for configuring a new build"""

from os import path, getcwd
import json
import general


class _ComplexEncoder(json.JSONEncoder):
    def default(self, o):
        if hasattr(o, "reprJSON"):
            return o.reprJSON()
        else:
            return json.JSONEncoder.default(self, o)


def configure(project: general.Project, build_dict: dict[str, str]):
    """Function to configure a new build and save its configuration to a JSON file"""

    build_path = generate_build_path(project)

    auth = general.MachineAuthenticationInfo(
        build_dict["username"], build_dict["password"], int(build_dict["port"])
    )

    machine = general.MachineInfo(
        general.Arch(build_dict["arch"].lower()), build_dict["ip"], auth
    )
    
    if "script" in build_dict:
        build = general.Build(machine, build_path, True, build_dict["script"])
    else:
        build = general.Build(machine, build_path, False)
        
    build.config_flags = build_dict["config_flags"]
    build.compiler_flags =  build_dict["compiler_flags"]

    project.builds.append(build)

    config = build.__dict__

    config_name = f"{project.build_system}_{project.runner}.json"
    with open(config_name, "w", encoding="UTF-8") as file:
        json.dump(config, file, indent=4, cls=_ComplexEncoder)


def generate_build_path(project: general.Project):
    return path.join(getcwd(), f"{project.build_system}_{project.runner}")


def parse_config(project: general.Project):
    project.builds = []
    with open("input.json", "r", encoding="UTF-8") as f:
        input_config = json.load(f)
        for build in input_config["builds"]:
            configure(project, build)
