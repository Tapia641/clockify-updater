import json
from Classes.clockify import Clockify
import Configuration.configuration as configuration
import logging
import os
import csv
import argparse

from Classes.template import Template


def create_csv(rows: list, name: str):
    with open(f'tmp/files/{name}.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(rows)


def validate_configuration():
    config = configuration.load_config()
    if config is not None:
        return config
    else:
        logging.ERROR("We don't have the API_KEY in Configuration/config.yaml")
        return None


def create_folders():
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


if __name__ == '__main__':
    # Logs Configuration
    create_folders()
    logging.basicConfig(filename='tmp/logs/debug.log', format='%(levelname)s:%(message)s', level=logging.DEBUG)

    # API KEY
    config = validate_configuration()

    if config is not None:
        parser = argparse.ArgumentParser()
        parser.add_argument('--start', type=str, help='Fecha inicial')
        parser.add_argument('--end', type=str, help='Fecha final')
        parser.add_argument('--load_entries', type=str, help='Carga las entradas desde un archivo CSV a Clockify.')
        parser.add_argument('--delete_all_entries', help='Borra todas tus entradas de clockify.',
                            action='store_true')
        parser.add_argument('--generate_example', help='Genera un archivo CSV ejemplo para Clockify.',
                            action='store_true')
        parser.add_argument('--generate_entries', help='Genera un archivo CSV con todas tus horas.',
                            action='store_true')
        args = parser.parse_args()

        # Testing
        clock = Clockify(config['API_KEY'])
        template = Template(config['API_KEY'])

        if args.generate_example:
            template.generate_example()
            logging.info('The example was generated in Examples/Example.csv')

        if args.generate_entries:
            template.generate_entries()
            logging.info('The example was generated in Examples/MyEntries.csv')

        if args.delete_all_entries:
            user = clock.get_user()
            entries = clock.get_entries(user['workspace_id'], user['user_id'])
            for entry in entries:
                # print(entry['id'], entry['workspaceId'])
                response = clock.delete_time_entry(entry['id'], user['workspace_id'])
                logging.info(response)

        if args.load_entries:
            entries = template.load_template(args.load_entries)
            workspace = clock.get_user()['workspace_id']
            user = clock.get_user()['user_id']
            for entry in entries:
                # print(entry)
                response = clock.add_new_entry(workspace_id=workspace, user_id=user, start=entry['start'],
                                               end=entry['end'], billable=entry['billable'],
                                               description=entry['description'], project_id=entry['projectId'],
                                               task_id=entry['taskId'], tag_ids=entry['tagIds'])
                if 'id' in response:
                    logging.info(f'The following entry was created: {entry["description"]}')
                else:
                    logging.error(f'The following entry was not created: {entry["description"]}')
            # user = clock.get_user()
        # projects = clock.get_projects(user['workspace'])
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
        # template_class = Template()
        # template_class.create_template()