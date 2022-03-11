import json
from Classes.clockify import Clockify
import Configuration.configuration as configuration
import logging
import os
import csv

from Classes.template import Template


def create_csv(rows: list, name: str):
    with open(f'tmp/files/{name}.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(rows)


def validate_configuration():
    config = configuration.load_config()
    print(config)


if __name__ == '__main__':

    # Folder's configuration
    current_directory = os.getcwd()
    tmp_directory = os.path.join(current_directory, 'tmp')
    if not os.path.exists(tmp_directory):
        os.makedirs(tmp_directory)
    logs_directory = os.path.join(current_directory, 'tmp/logs')
    files_directory = os.path.join(current_directory, 'tmp/files')
    if not os.path.exists(tmp_directory) or not os.path.exists(logs_directory) or not os.path.exists(files_directory):
        os.makedirs(logs_directory)
        os.makedirs(files_directory)

    validate_configuration()

    # Logs Configuration
    logging.basicConfig(filename='tmp/logs/debug.log', format='%(levelname)s:%(message)s', level=logging.DEBUG)

    # Testing
    clock = Clockify('MmFhNmZlNDQtNDcwNy00YTdlLWI0MGQtYTM3YzA5YzYzODE2')
    user = clock.get_user()
    projects = clock.get_projects(user['workspace'])
    # clock.add_new_entry(user['workspace'], user['id'])
    # pandas.read_json(json.dumps(projects)).to_excel("tmp/output.xlsx")
    # with open('tmp/files/projects.json', 'w') as outfile:
    #     json.dump(projects, outfile)

    # Export projects to csv
    # rows_projects = [['ID', 'NAME', 'CLIENT']]
    # for element in projects:
    #     rows_projects.append([element, projects[element]['name'], projects[element]['clientName']])
    # create_csv(rows_projects, 'projects')

    # clock.get_entries(user['workspace'], user['id'])

    # Template Test
    template_class = Template()
    template_class.create_template()
