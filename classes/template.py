# CREATE A TEMPLATE TO UPLOAD TO CLOCKIFY

import csv
from classes.clockify import Clockify
from datetime import datetime
# import datetime

from dateutil import tz

from classes.files import Files


class Template:
    __slots__ = ['USER', 'API', 'HEADERS_TASKS', 'HEADERS_PROJECTS', 'HEADERS_ENTRIES']

    def __init__(self, api):
        self.API = api
        self.HEADERS_ENTRIES = {'PROJECT_ID': [], 'DESCRIPTION': [], 'BILLABLE': [], 'TASK_ID': [], 'START': [],
                                'END': [],
                                'TAGS_IDS': []}
        self.HEADERS_PROJECTS = {'PROJECT_ID': [], 'NAME': [], 'BILLABLE': [], 'BILLABLE': [], 'CLIENT_NAME': []}
        self.HEADERS_TASKS = {'TASK_ID': [], 'NAME': [], 'PROJECT_ID': [], 'BILLABLE': [], 'STATUS': []}
        self.USER = Clockify(self.API)

    def generate_projects(self):
        user = self.USER.get_user()
        projects = self.USER.get_projects(user['workspace_id'])
        template = self.HEADERS_PROJECTS

        for id_ in projects:
            template['PROJECT_ID'].append(id_)
            template['NAME'].append(projects[id_]['name'])
            template['BILLABLE'].append(projects[id_]['billable'])
            template['CLIENT_NAME'].append(projects[id_]['clientName'])
        return template

    def generate_entries(self, number_entries: int):
        user = self.USER.get_user()
        entries = self.USER.get_entries(user['workspace_id'], user['user_id'])
        template = self.HEADERS_ENTRIES
        number_start = 0

        for entry in entries:

            if not number_start < number_entries:
                break
            else:
                number_start += 1

            # Create datetime
            input_format = "%Y-%m-%dT%H:%M:%SZ"
            start = datetime.strptime(entry['timeInterval']['start'], input_format)
            end = datetime.strptime(entry['timeInterval']['end'], input_format)

            # set zones
            from_zone = tz.gettz('UTC')
            to_zone = tz.gettz(user['timeZone'])

            # Datetime from UTC by default
            start = start.replace(tzinfo=from_zone)
            end = end.replace(tzinfo=from_zone)

            # Convert time zones
            start = str(start.astimezone(to_zone)).replace('-06:00', '')
            end = str(end.astimezone(to_zone)).replace('-06:00', '')

            template['PROJECT_ID'].append(entry['projectId'])
            template['DESCRIPTION'].append(entry['description'])
            template['BILLABLE'].append(entry['billable'])
            template['TASK_ID'].append(entry['taskId'])
            template['START'].append(start)
            template['END'].append(end)
            template['TAGS_IDS'].append(entry['tagIds'])

        return template

    def generate_tasks(self):
        user = self.USER.get_user()
        tasks = self.USER.get_all_tasks(user['workspace_id'])
        template = self.HEADERS_TASKS

        for task in tasks:
            template['TASK_ID'].append(task['id'])
            template['NAME'].append(task['name'])
            template['PROJECT_ID'].append(task['project_id'])
            template['BILLABLE'].append(task['billable'])
            template['STATUS'].append(task['status'])
        return template

    def generate_example(self, number):
        entries_ = self.generate_entries(10)
        projects_ = self.generate_projects()
        tasks_ = self.generate_tasks()
        Files.create_template(entries=entries_, projects=projects_, tasks=tasks_)

    # def generate_entries(self):
    #     user = self.USER.get_user()
    #     entries = self.USER.get_entries(user['workspace_id'], user['user_id'])
    #     template = self.HEADERS_ENTRIES
    #     input_format = "%Y-%m-%dT%H:%M:%SZ"
    #     for entry in entries:
    #         start = entry['timeInterval']['start']
    #         end = entry['timeInterval']['end']
    #         template.append([entry['projectId'], entry['description'], entry['billable'], entry['taskId'],
    #                          start, end, *entry['tagIds'][:]])
    #     self.create_csv(template, "MyEntries")

    @staticmethod
    def create_csv(rows: list, name: str):
        with open(f'Examples/{name}.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(rows)

    def load_template(self, path_file: str):
        user = self.USER.get_user()
        with open(f'{path_file}') as file:
            csv_reader = csv.reader(file, delimiter=',')
            entries = []
            for row in csv_reader:
                if not row[0] == "PROJECT_ID" and not row[0] == "":
                    # Convert 3/11/2022 8:12 to 2022-03-11T16:56:14Z
                    date_start = row[4].split(" ")[0].split("/")
                    hour_start = row[4].split(" ")[1].split(":")
                    date_end = row[5].split(" ")[0].split("/")
                    hour_end = row[5].split(" ")[1].split(":")

                    start = datetime(int(date_start[2]), int(date_start[0]), int(date_start[1]),
                                     int(hour_start[0]), int(hour_start[1]), 0)
                    end = datetime(int(date_end[2]), int(date_end[0]), int(date_end[1]),
                                   int(hour_end[0]), int(hour_end[1]), 0)

                    start = start.strftime('%Y-%m-%dT%H:%M:%SZ')
                    end = end.strftime('%Y-%m-%dT%H:%M:%SZ')

                    input_format = "%Y-%m-%dT%H:%M:%SZ"
                    start = datetime.strptime(start, input_format)
                    end = datetime.strptime(end, input_format)

                    # set zones
                    from_zone = tz.gettz('UTC')
                    to_zone = tz.gettz(user['timeZone'])

                    # Datetime from UTC by default
                    start = start.replace(tzinfo=to_zone)
                    end = end.replace(tzinfo=to_zone)

                    # Convert time zones
                    start = start.astimezone(from_zone)
                    end = end.astimezone(from_zone)

                    start = start.strftime('%Y-%m-%dT%H:%M:%SZ')
                    end = end.strftime('%Y-%m-%dT%H:%M:%SZ')

                    data = {
                        "start": start,
                        "end": end,
                        "billable": row[2],
                        "description": row[1],
                        "projectId": row[0],
                        "taskId": row[3],
                        "tagIds": [row[6]]
                    }
                    entries.append(data)
        return entries
