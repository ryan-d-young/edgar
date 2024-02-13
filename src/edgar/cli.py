import argparse


ARG_PARSER = argparse.ArgumentParser(
    description='programmatic access to SEC EDGAR API')
ARG_PARSER.add_argument(
    'endpoint',
    metavar='endpoint',
    nargs=1,
    type=str,
    choices=['facts', 'concept', 'frame', 'submissions'])
ARG_PARSER.add_argument(
    '--args',
    metavar='args',
    nargs="*",
    type=str)
ARG_PARSER.add_argument(
    '--output',
    metavar='dest',
    nargs=1,
    type=str)
