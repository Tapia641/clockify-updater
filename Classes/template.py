# CREATE A TEMPLATE TO UPLOAD TO CLOCKIFY

import csv
from Classes.clockify import Clockify
from datetime import datetime
import datetime


class Template:
    __slots__ = ['HEADER', 'USER', 'API']

    def __init__(self, api):
        self.API = api
        self.HEADER = [['PROJECT_ID', 'DESCRIPTION', 'BILLABLE', 'TASK_ID', 'START', 'END', 'TAGS_IDS']]
        self.USER = Clockify(self.API)

    def generate_example(self):
        user = self.USER.get_user()
        entries = self.USER.get_entries(user['workspace_id'], user['user_id'])
        template = self.HEADER
        input_format = "%Y-%m-%dT%H:%M:%SZ"
        start = datetime.strptime(entries[0]['timeInterval']['start'], input_format)
        end = datetime.strptime(entries[0]['timeInterval']['end'], input_format)
        template.append(
            [entries[0]['projectId'], entries[0]['description'], entries[0]['billable'], entries[0]['taskId'],
             start, end, entries[0]['tagIds'][0]])
        self.create_csv(template, "Example")

    def generate_entries(self):
        user = self.USER.get_user()
        entries = self.USER.get_entries(user['workspace_id'], user['user_id'])
        template = self.HEADER
        input_format = "%Y-%m-%dT%H:%M:%SZ"
        for entry in entries:
            start = entry['timeInterval']['start']
            # start = datetime.strptime(entry['timeInterval']['start'], input_format)
            end = entry['timeInterval']['end']
            # end = datetime.strptime(entry['timeInterval']['end'], input_format)
            template.append([entry['projectId'], entry['description'], entry['billable'], entry['taskId'],
                             start, end, *entry['tagIds'][:]])
        self.create_csv(template, "MyEntries")

    @staticmethod
    def create_csv(rows: list, name: str):
        with open(f'Examples/{name}.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(rows)

    @staticmethod
    def load_template(path_file: str):
        # TODO convertir  UTC
        with open(f'{path_file}') as file:
            csv_reader = csv.reader(file, delimiter=',')
            entries = []
            for row in csv_reader:
                if not row[0] == "PROJECT_ID" and not row[0] == "":
                    if len(row[4].split(" ")) > 1:
                        if '/' in row[4]:
                            # Convert 3/11/2022 8:12 to 2022-03-11T16:56:14Z
                            date_start = row[4].split(" ")[0].split("/")
                            hour_start = row[4].split(" ")[1].split(":")
                            date_end = row[5].split(" ")[0].split("/")
                            hour_end = row[5].split(" ")[1].split(":")
                            start = datetime.datetime(int(date_start[2]), int(date_start[0]), int(date_start[1]),
                                                      int(hour_start[0]), int(hour_start[1]), 0)
                            end = datetime.datetime(int(date_end[2]), int(date_end[0]), int(date_end[1]),
                                                    int(hour_end[0]), int(hour_end[1]), 0)
                        else:
                            # Convert 2022-03-11 16:56:14 to 2022-03-11T16:56:14Z
                            date_start = row[4].split(" ")[0].split("-")
                            hour_start = row[4].split(" ")[1].split(":")
                            date_end = row[5].split(" ")[0].split("-")
                            hour_end = row[5].split(" ")[1].split(":")
                            start = datetime.datetime(int(date_start[0]), int(date_start[1]), int(date_start[2]),
                                                      int(hour_start[0]),
                                                      int(hour_start[1]), 0)
                            end = datetime.datetime(int(date_end[0]), int(date_end[1]), int(date_end[2]),
                                                    int(hour_end[0]),
                                                    int(hour_end[1]), 0)

                        start = start.strftime('%Y-%m-%dT%H:%M:%SZ')
                        end = end.strftime('%Y-%m-%dT%H:%M:%SZ')
                    else:
                        start = row[4]
                        end = row[5]
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
