# CREATE A TEMPLATE TO UPLOAD TO CLOCKIFY

import csv
from Classes.clockify import Clockify
from datetime import datetime
# import datetime

from dateutil import tz


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

        # Create datetime
        input_format = "%Y-%m-%dT%H:%M:%SZ"
        start = datetime.strptime(entries[0]['timeInterval']['start'], input_format)
        end = datetime.strptime(entries[0]['timeInterval']['end'], input_format)

        # set zones
        from_zone = tz.gettz('UTC')
        to_zone = tz.gettz(user['timeZone'])

        # Datetime from UTC by default
        start = start.replace(tzinfo=from_zone)
        end = end.replace(tzinfo=from_zone)

        # Convert time zones
        start = str(start.astimezone(to_zone)).replace('-06:00', '')
        end = str(end.astimezone(to_zone)).replace('-06:00', '')

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
            end = entry['timeInterval']['end']
            template.append([entry['projectId'], entry['description'], entry['billable'], entry['taskId'],
                             start, end, *entry['tagIds'][:]])
        self.create_csv(template, "MyEntries")

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
                    start = str(start.astimezone(from_zone))
                    end = str(end.astimezone(from_zone))

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
