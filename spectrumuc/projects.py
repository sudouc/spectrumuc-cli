"""Module for managing spectrumuc projects"""

from __future__ import print_function
import argparse
from .constants import Project
from . import database as db
from . import nodes

database = db.Database()


def run(args):
    """run the projects command"""
    print('projects')


def subparser(parser):
    """setup the projects argument parser"""

    assert isinstance(parser, argparse.ArgumentParser)

    subparsers = parser.add_subparsers()

    add_parser = subparsers.add_parser('add', help='add a project')
    add_parser.set_defaults(func=add)

    delete_parser = subparsers.add_parser('delete', help='delete a project')
    delete_parser.add_argument(
        'project_id', help='id of the project to delete')
    delete_parser.set_defaults(func=delete)

    edit_parser = subparsers.add_parser('edit', help='edit a project')
    edit_parser.add_argument('project_id', help='id of the project to edit')
    edit_parser.set_defaults(func=edit)

    status_parser = subparsers.add_parser(
        'status', help='view status of a project')
    status_parser.add_argument(
        'project_id', help='id of the project to see the status of')
    status_parser.set_defaults(func=status)

    list_parser = subparsers.add_parser('list', help='list all projects')
    list_parser.set_defaults(func=list_projects)


def add(args):
    AddCommand().run(args)


def delete(args):
    raise NotImplementedError(
        'Currently Deleting must be done by an admin through the Firebase Console')


def edit(args):
    pass


def status(args):
    StatusCommand().run(args)


def list_projects(args):
    ListCommand().run(args)


class AddCommand(object):

    def run(self, args):
        email, password = self.ask_user_info()
        project = self.ask_project_info()
        project_user = database.add_user(email, password)
        print("Project User Created...")
        database.set_project(project_user['localId'], project)
        print("Project Database Entry Created")

    def ask_user_info(self):
        # FIXME Validation anyone? Also refactor into a get user details method
        email = raw_input('Enter Project Email > ')
        password = raw_input('Enter Password: > ')
        return email, password

    def ask_project_info(self):

        # FIXME Validation anyone?
        project = {
            Project.NAME: raw_input('Enter Name: > '),
            Project.DESCRIPTION: raw_input('Enter Description: > '),
        }

        return project


class EditCommand(object):

    def run(self, args):
        project = self.ask_project_info()
        database.update_project(args.project_id, project)
        print("Success")

    def ask_project_info(self):
        # FIXME Validation anyone?
        project = {
            Project.NAME: raw_input('Enter Name: > '),
            Project.DESCRIPTION: raw_input('Enter Description: > '),
        }

        return project


class StatusCommand(object):

    def run(self, args):
        project = database.get_project(args.project_id)
        try:
            node_list = database.get_nodes(project_key=args.project_id)
        except IndexError:
            node_list = None
        print_project(args.project_id, project, node_list=node_list)

class ListCommand(object):

    def run(self, args):
        projects = database.get_projects()
        for key in projects:
            print_project(key, projects[key])


def print_project(key, project, node_list=None):

    base_string = """
---------------------------------------------------------
                Key:      {0}
               Name:      {1}
        Description:      {2}
---------------------------------------------------------"""

    output_string = base_string.format(
        key, project[Project.NAME], project[Project.DESCRIPTION])
    print(output_string)

    if node_list:
        print("NODES:")
        for node_key in node_list:
            nodes.print_node_detail(node_key, node_list[node_key])
    else:
        print("No Nodes Assigned")
