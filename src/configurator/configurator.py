from NonAmphimixis.src.general import general
import json


def configure(project: general.Project):
    args = []
    name = input("Name curremt config\n")
    while True:
        arg = input("Enter arg\n")
        if arg == "":
            break

        args.append(arg)
    config = {
        "config_name": name,
        "args": str(args),
        "project_path": project.path,
        "build_path": project.builds_path,
        "build_system": project.build_system
    }
    with open(f"{name}.json", "w") as file:
        json.dump(config, file, indent=4)
