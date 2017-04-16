#!/usr/bin/env python
import argparse
import json
import os
import sys

from bioblend import galaxy

from common_parser import get_common_args
from . import get_galaxy_connection


def import_workflow(gi, path):
    """
    Given a connection to a Galaxy Instance (gi) and a path to a Galaxy workflow file,
    this function will import the worklfow into Galaxy.
    """
    print path
    with open(path, 'r') as wf_file:
        import_uuid = json.load(wf_file).get('uuid')
    existing_uuids = [d.get('latest_workflow_uuid') for d in gi.workflows.get_workflows()]
    if import_uuid not in existing_uuids:
        gi.workflows.import_workflow_from_local_path(path)


def main():
    """
        This script uses bioblend to import .ga workflow files into a running instance of Galaxy
    """
    parent = get_common_args()
    parser = argparse.ArgumentParser(parents=[parent])
    parser.add_argument("-w", "--workflow_path",
                        required=True,
                        help='Path to a workflow file or a directory with multiple workflow files ending with ".ga"')

    args = parser.parse_args()
    gi = get_galaxy_connection(args)

    if os.path.isdir(args.workflow_path):
        for file_path in os.listdir(args.workflow_path):
            if file_path.endswith('.ga'):
                import_workflow(gi, os.path.join(args.workflow_path, file_path))
    else:
        import_workflow(gi, args.workflow_path)


if __name__ == '__main__':
    main()
