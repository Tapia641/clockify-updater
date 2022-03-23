from classes.clockify import Clockify
import configuration.configuration as configuration
import logging
import os
import csv
import argparse

from classes.files import Files
from classes.template import Template


def create_csv(rows: list, name: str):
    with open(f'tmp/files/{name}.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(rows)


def validate_configuration():
    config = configuration.load_config()
    if config is not None:
        return config
    else:
        logging.ERROR("We don't have the API_KEY in configuration/config.yaml")
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
    # Logs configuration
    create_folders()
    logging.basicConfig(filename='tmp/logs/debug.log', format='%(levelname)s:%(message)s', level=logging.DEBUG)

    # API KEY
    config = validate_configuration()

    if config is not None:
        parser = argparse.ArgumentParser()
        parser.add_argument('--load_entries', type=str, help='Carga las entradas desde un archivo CSV a Clockify.')
        parser.add_argument('--delete_all_entries', help='Borra todas tus entradas de clockify.',
                            action='store_true')
        parser.add_argument('--generate_example', help='Genera un archivo CSV ejemplo para Clockify.',
                            action='store_true')
        args = parser.parse_args()

        # Testing
        clock = Clockify(config['API_KEY'])
        template = Template(config['API_KEY'])

        if args.generate_example:
            n = 50
            template.generate_example(n)
            logging.info('The example was generated in tmp/files/Example.csv')

        if args.delete_all_entries: #BE CAREFUL
            user = clock.get_user()
            entries = clock.get_entries(user['workspace_id'], user['user_id'])
            for entry in entries:
                response = clock.delete_time_entry(entry['id'], user['workspace_id'])
                logging.info(response)
            logging.info('All entries were deleted')

        if args.load_entries:
            entries = template.load_template(args.load_entries)
            workspace = clock.get_user()['workspace_id']
            user = clock.get_user()['user_id']
            for entry in entries:
                response = clock.add_new_entry(workspace_id=workspace, user_id=user, start=entry['start'],
                                               end=entry['end'], billable=entry['billable'],
                                               description=entry['description'], project_id=entry['projectId'],
                                               task_id=entry['taskId'], tag_ids=entry['tagIds'])
                if response:
                    logging.info(f'The following entry was created: {entry["description"]}')
                else:
                    logging.error(f'The following entry was not created: {entry["description"]}')
