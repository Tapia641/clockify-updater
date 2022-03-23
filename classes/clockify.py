import json
from typing import Dict
import requests
import logging
import logging.config


class Clockify:
    __slots__ = ['API_KEY', 'ENDPOINT', 'HEADERS', 'DELAY', 'USER']

    def __init__(self, key):
        self.DELAY = 1
        self.API_KEY = key
        self.ENDPOINT = 'https://api.clockify.me/api/v1'
        self.HEADERS = {'Content-Type': 'application/json', 'X-Api-Key': self.API_KEY}

    def get_user(self) -> Dict:
        url = self.ENDPOINT + f'/user'
        logging.info("Gathering user information...")
        r = requests.get(url, headers=self.HEADERS)
        response = r.json()
        user = {}
        try:
            user['user_id'] = response['id']
            user['email'] = response['email']
            user['name'] = response['name']
            user['workspace_id'] = response['activeWorkspace']
            user['timeZone'] = response['settings']['timeZone']
            return user
        except KeyError:
            logging.info(
                f"We could not get the information from {url} with the api key.")
            raise

    def get_projects(self, workspace_id: str) -> Dict:
        url = self.ENDPOINT + f'/workspaces/{workspace_id}/projects'
        logging.info(f"Gathering projects information from {workspace_id}...")
        r = requests.get(url, headers=self.HEADERS)
        response = r.json()
        projects = {}
        for project in response:
            project_id = project['id']
            projects[project_id] = {"name": project['name'], "billable": project['billable'],
                                    "clientName": project['clientName']}
        return projects

    def get_entries(self, workspace_id: str, user_id: str) -> Dict:
        url = self.ENDPOINT + \
              f'/workspaces/{workspace_id}/user/{user_id}/time-entries'
        r = requests.get(url, headers=self.HEADERS)
        response = r.json()
        return response

    def get_workspaces(self):
        url = self.ENDPOINT + f'/workspaces'
        logging.info("Gathering workspaces information...")
        r = requests.get(url, headers=self.HEADERS)
        response = r.json()
        data_workspaces = {}
        try:
            for element in response:
                workspace_id = element['id']
                workspace_name = element['name']
                data_workspaces[element['id']] = [workspace_id, workspace_name]
            return data_workspaces
        except KeyError:
            logging.info(
                f"We could not get the information from {url} with the api key.")
            raise

    def get_all_users(self, workspace_id: str, name_workspace: str) -> Dict:
        url = self.ENDPOINT + f'workspaces/{workspace_id}/users'
        logging.info(
            f"Getting users information from the workspace: {name_workspace}.")
        r = requests.get(url, headers=self.HEADERS)
        response = r.json()
        users = {}
        for user in response:
            user_id = user['id']
            user_name = user['name']
            user_email = user['email']
            user_time_settings = user['settings']
            users[user_id] = [user_name, user_email, user_time_settings]
        return users

    def get_all_tasks(self, workspace_id: str) -> Dict:
        projects = self.get_projects(workspace_id)
        tasks = []
        for project_id in projects:
            # GET /workspaces/{workspaceId}/projects/{projectId}/tasks
            url = self.ENDPOINT + f'workspaces/{workspace_id}/projects/{project_id}/tasks'
            logging.info(
                f"Getting tasks information from the workspace: {workspace_id}.")
            r = requests.post(url, headers=self.HEADERS)
            response = r.json()
            template = {}
            if r.status_code == 200:
                for task in response:
                    template['id'] = task['id']
                    template['name'] = task['name']
                    template['project_id'] = task['projectId']
                    template['billable'] = task['billable']
                    template['status'] = task['status']
                    tasks.append(template)
        return tasks

    def add_new_entry(self, workspace_id: str, user_id: str, start, end, billable, description, project_id, task_id,
                      tag_ids):
        logging.info(f"Adding entry information in {workspace_id}...")
        url = self.ENDPOINT + f'/workspaces/{workspace_id}/user/{user_id}/time-entries'
        data = {
            "start": start,
            "end": end,
            "billable": billable,
            "description": description,
            "projectId": project_id,
            "taskId": task_id,
            "tagIds": tag_ids
        }
        r = requests.post(url, headers=self.HEADERS, data=json.dumps(data))
        response = r.json()
        return response

    def delete_time_entry(self, workspace_id: str, entry_id: str):
        logging.info(f"Deleting entry in {workspace_id}...")
        url = self.ENDPOINT + f'/workspaces/{workspace_id}/time-entries/{entry_id}'
        r = requests.delete(url, headers=self.HEADERS)
        if r.status_code == 204:
            logging.info(f"The entry {entry_id} was deleted")
        else:
            logging.error(f"Error with {entry_id}  status: {r.status_code} ")
