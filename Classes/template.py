# CREATE A TEMPLATE TO UPLOAD TO CLOCKIFY

import csv
from Classes.clockify import Clockify


class Template:
    __slots__ = ['HEADER', 'USER']

    def __init__(self):
        self.HEADER = [['PROJECT_ID', 'DESCRIPTION', 'BILLABLE', 'TASK_ID', 'START', 'END', 'TAGS_IDS']]
        self.USER = Clockify('MmFhNmZlNDQtNDcwNy00YTdlLWI0MGQtYTM3YzA5YzYzODE2')

    def generate_example(self):
        user = self.USER.get_user()
        entries = self.USER.get_entries(user['workspace'], user['id'])
        template = self.HEADER
        template.append(
            [entries[0]['projectId'], entries[0]['description'], entries[0]['billable'], entries[0]['taskId'],
             entries[0]['timeInterval']['start'], entries[0]['timeInterval']['end'], entries[0]['tagIds']])
        self.create_csv(template, "Example")

    def create_template(self):
        user = self.USER.get_user()
        entries = self.USER.get_entries(user['workspace'], user['id'])
        template = self.HEADER
        for entry in entries:
            template.append([entry['projectId'], entry['description'], entry['billable'], entry['taskId'],
                             entry['timeInterval']['start'], entry['timeInterval']['end'], entry['tagIds']])
        self.create_csv(template, "MyEntries")

    @staticmethod
    def create_csv(rows: list, name: str):
        with open(f'Examples/{name}.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(rows)
