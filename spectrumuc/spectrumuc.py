"""spectrumuc.spectrumuc: provides entry point main(), calls subcommands in their own modules"""

from __future__ import print_function

__version__ = "0.0.0"


import sys
import argparse

from . import nodes
from . import projects

def main():
    """
    Run the program
    """

    print ("Executing spectrumuc version %s." % __version__)

    parser = argparse.ArgumentParser(prog='spectrumuc')
    subparsers = parser.add_subparsers(help='Allowed subcommands')


    # create the parser for the "nodes" command
    nodes_parser = subparsers.add_parser('nodes', help='manage spectrumuc nodes')
    nodes.subparser(nodes_parser)
    nodes_parser.set_defaults(func=nodes.run)

    # create the parser for the "projects" command
    projects_parser = subparsers.add_parser('projects', help='manage spectrumuc projects')
    projects.subparser(projects_parser)
    projects_parser.set_defaults(func=projects.run)

    args = parser.parse_args()
    args.func(args)
