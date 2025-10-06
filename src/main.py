import sys
import general, analyzer, builder, configurator, profiler

try:
    analyzer_ = analyzer.Analyzer(sys.argv[1])

    analyzer_.analyze()
except FileNotFoundError as e:
    print(f"{e}")
    exit(-1)

project = general.Project(
    sys.argv[1],
    [],
    general.build_systems_dict["make"],
    general.build_systems_dict["cmake"],
)

configurator.parse_config(project)

builder.Builder.process(project)

profiler_ = profiler.Profiler(project.builds[0])

profiler_.execution_time()

print(profiler_.stats)
