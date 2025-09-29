import sys
import general, analyzer, builder, configurator, profiler

analyzer_ = analyzer.Analyzer(sys.argv[1])

analyzer_.analyze()

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
