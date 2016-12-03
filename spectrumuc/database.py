"""firebase.py manages the firebase configuration"""
from __future__ import print_function
import pyrebase
import os
import sys
import tempfile
import json
from requests.exceptions import HTTPError

from .constants import Node, Project

DEBUG_USER = 'ar@dair.io'
DEBUG_PASSWORD = '5pectrum'

config = {
  "apiKey": "AIzaSyCG2-TArRw69Pkk4Pot1LY5ThFd6f0axI4",
  "authDomain": "sudo-spectrumuc.firebaseapp.com",
  "databaseURL": "https://sudo-spectrumuc.firebaseio.com",
  "storageBucket": "sudo-spectrumuc.appspot.com"
}

class Database(object):

    user = None

    def __init__(self):
        self.firebase = pyrebase.initialize_app(config)

    def login_if_not(self):
        """Login if the user is not already logged in"""
        if not self.user:
            self.user = self.refresh_using_token_from_file()
            if not self.user:
                self.user = self.prompt_login()

    def refresh_using_token_from_file(self):
        """Get the token from a tempfile and log the user in with that"""
        token_filepath = os.path.join(tempfile.gettempdir(), 'spectrum_uc_token')
        try:
            with open(token_filepath, 'rb') as token_file:
                refresh_token = token_file.readline()
        except IOError, e:
            return None
        if refresh_token == '':
            return None
        return self.firebase.auth().refresh(refresh_token)

    def prompt_login(self):
        """Prompt the user fro a username and password, use them to login and set the user"""

        #FIXME Validation?
        email = DEBUG_USER #raw_input('ADMIN EMAIL: ')
        password = DEBUG_PASSWORD #raw_input('ADMIN PASSWORD: ')

        try:
            login_result = self.login(email, password)
        except HTTPError, e:
            error = json.loads(e.strerror)
            print("Encountered Error:", error['error']['message'])
            sys.exit(1)

        return login_result

    def login(self, email, password):
        """Attempt to login to firebase, return the user object"""
        return self.firebase.auth().sign_in_with_email_and_password(email, password)

    def add_user(self, email, password):
        """Add a user to firebase with the username and password given

        :return: the user auth object
        """
        try:
            usr = self.firebase.auth().create_user_with_email_and_password(email, password)
        except HTTPError, e:
            error = json.loads(e.strerror)
            print("Encountered Error:", error['error']['message'])
            sys.exit(0)

        return usr

    def get_node(self, key):
        """"Get info about a specific node, given the key"""
        node = self.firebase.database().child(Node.PATH + '/' + key).get().val()
        return node

    def get_nodes(self, project_key=None):
        """Get the nodes associated with the given project key, or get all nodes"""
        if project_key:
            nodes = self.firebase.database().child(Node.PATH).order_by_child(Node.PROJECT).equal_to(project_key).get()
            nodes = nodes.val()
        else:
            nodes = self.firebase.database().child(Node.PATH).get().val()

        return nodes

    def set_node(self, key, node):
        """
        Set Node Details in the database

        :param key: id of the node (node UID)
        :param node: dict containing the node values
        """

        self.login_if_not()
        self.firebase.database().child(Node.PATH).child(key).set(node, self.user['idToken'])

    def update_node(self, key, node):
        """
        Update Node details in the database, dict doesn't have to have all keys

        :param key: id of the node (node UID)
        :param node: dict containing the node values
        """
        self.login_if_not()
        self.firebase.database().child(Node.PATH).child(key).update(node, self.user['idToken'])

    def set_project(self, key, project):
        """
        Set Project Details in the database

        :param key: id of the project (project UID)
        :param project: dict containing the node values
        """
        self.login_if_not()
        self.firebase.database().child(Project.PATH).child(key).set(project, self.user['idToken'])

    def update_project(self, key, project):
        """
        Update Project details in the database, dict doesn't have to have all keys

        :param key: id of the project (Project UID)
        :param project: dict containing the node values
        """
        self.login_if_not()
        self.firebase.database().child(Project.PATH).child(key).update(project, self.user['idToken'])

    def get_project(self, key=None):
        """Get the project with the given key"""
        project = self.firebase.database().child(Project.PATH + '/' + key).get().val()
        return project

    def get_projects(self):
        """Get all projects"""
        projects = self.firebase.database().child(Project.PATH).get().val()
        return projects
