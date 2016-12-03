"""Module for managing spectrumuc nodes"""

from __future__ import print_function
import argparse

from . import colors
from . import database as db
from .constants import Node

database = db.Database()


def run(args):
    """run the nodes command"""
    print('nodes')


def subparser(parser):
    """setup the nodes argument parser"""

    assert isinstance(parser, argparse.ArgumentParser)

    subparsers = parser.add_subparsers()

    add_parser = subparsers.add_parser('add', help='add a node')
    add_parser.set_defaults(func=add)

    assign_parser = subparsers.add_parser(
        'assign', help='assign a node to a project')
    assign_parser.add_argument('node_id', help='id of the node to delete')
    assign_parser.add_argument(
        'project_id', help='id of the project to assign to')
    assign_parser.set_defaults(func=assign)

    delete_parser = subparsers.add_parser('delete', help='delete a node')
    delete_parser.add_argument('node_id', help='id of the node to delete')
    delete_parser.set_defaults(func=delete)

    edit_parser = subparsers.add_parser('edit', help='edit a node')
    edit_parser.add_argument('node_id', help='id of the node to edit')
    edit_parser.set_defaults(func=edit)

    status_parser = subparsers.add_parser(
        'status', help='view status of nodes')
    status_parser.add_argument(
        'node_id', nargs='?', help='id of the node to see the status of')
    status_parser.set_defaults(func=status)

    list_parser = subparsers.add_parser('list', help='list all nodes')
    list_parser.set_defaults(func=list_nodes)


def add(args):
    AddCommand().run(args)


def assign(args):
    AssignCommand().run(args)


def delete(args):
    raise NotImplementedError(
        'Currently Deleting must be done by an admin through the Firebase Console')


def edit(args):
    EditCommand().run(args)


def status(args):
    StatusCommand().run(args)


def list_nodes(args):
    ListCommand().run(args)


class AddCommand(object):

    def run(self, args):
        email, password = ask_node_account_info()
        node = ask_node_info()
        node_user = database.add_user(email, password)
        print("Node User Created...")
        database.set_node(node_user['localId'], node)
        print("Node Database Entry Created")


class AssignCommand(object):

    def run(self, args):
        node = {
            Node.PROJECT: args.project_id
        }
        database.update_node(args.node_id, node)


class EditCommand(object):

    def run(self, args):
        node = ask_node_info()
        database.update_node(args.node_id, node)
        print("Success")


class StatusCommand(object):

    def run(self, args):
        if args.node_id:
            node = database.get_node(args.node_id)
            print_node_detail(args.node_id, node)
        else:
            nodes = database.get_nodes()
            for key in nodes:
                print_node_detail(key, nodes[key])


class ListCommand(object):

    def run(self, args):
        nodes = database.get_nodes()
        for key in nodes:
            print_node(key, nodes[key])


def ask_node_account_info():
        # FIXME Validation anyone?
    hostname = raw_input('Enter PI Hostname: > ')
    password = raw_input('Enter Password for node user account: > ')
    email = hostname + Node.EMAIL_DOMAIN
    return email, password


def ask_node_info():
    # FIXME Validation anyone? refactor
    node = {
        Node.NAME: raw_input('Enter Name: > '),
        Node.DESCRIPTION: raw_input('Enter Description: > '),
        Node.LOCATION: {
            Node.LATITUDE: raw_input('Enter Latitude (decimal): > '),
            Node.LONGITUDE: raw_input('Enter Longitude (decimal): > ')
        },
        Node.PROJECT: raw_input('Enter Project ID: > '),
    }
    return node


def print_node_detail(key, node):
    base_string = """
---------------------------------------------------------
        NODE: {0}
            Name:       {1}
     Description:       {2}
    Approx Color:       {3}
        Location:
              Lat:      {4}
              Long:     {5}
          Online:       {6}
         Project:       {7}
---------------------------------------------------------"""

    try:
        rgb = (node[Node.COLOR]['red'],
               node[Node.COLOR]['green'],
               node[Node.COLOR]['blue'])

        color_name = colors.get_colour_name(rgb)[1]
    except KeyError:
        color_name = 'None'

    try:
        online_status = node[Node.ONLINE]
    except KeyError:
        online_status = "None"

    output_string = base_string.format(
        key,
        node[Node.NAME],
        node[Node.DESCRIPTION],
        color_name,
        node[Node.LOCATION][Node.LATITUDE],
        node[Node.LOCATION][Node.LONGITUDE],
        online_status,
        node[Node.PROJECT]
    )
    print(output_string)


def print_node(key, node):

    base_string = """
---------------------------------------------------------
        NODE: {0}
               Name:      {1}
        Description:      {2}
            Project:      {3}
---------------------------------------------------------"""

    output_string = base_string.format(
        key,
        node[Node.NAME],
        node[Node.DESCRIPTION],
        node[Node.PROJECT]
    )
    print(output_string)
