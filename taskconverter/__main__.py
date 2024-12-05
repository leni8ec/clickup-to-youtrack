from taskconverter.providers import youtrack, clickup


def clickup_to_youtrack(input_file: str, output_file: str):
    tasks = clickup.parse(input_file)
    youtrack.dump(tasks, output_file)


print('STARTED!')

# todo: parse cli arguments
# import argparse
# clickup_to_youtrack()
