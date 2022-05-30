import pandas as pd


class Files:

    def __init__(self):
        pass

    @staticmethod
    def create_template(path: str = 'tmp/files/Clockify_Example.xlsx', entries: dict = {}, tasks: dict = {},
                        projects: dict = {}):
        # Example
        load = {'PROJECT_ID': [], 'DESCRIPTION': [], 'BILLABLE': [], 'TASK_ID': [], 'START': [],
                'END': [], 'TAGS_IDS': []}

        # Create dataframe
        df_t = pd.DataFrame(tasks)
        df_p = pd.DataFrame(projects)
        df_e = pd.DataFrame(entries)
        df_l = pd.DataFrame(load)

        # Create a Pandas Excel writer using XlsxWriter as the engine.
        writer = pd.ExcelWriter(path, engine='xlsxwriter')

        # Convert the dataframe to an XlsxWriter Excel object.
        df_e.to_excel(writer, sheet_name='ENTRIES', index=False)
        df_p.to_excel(writer, sheet_name='PROJECTS', index=False)
        df_t.to_excel(writer, sheet_name='TASKS', index=False)
        df_l.to_excel(writer, sheet_name='LOAD_ENTRIES', index=False)

        # Close the Pandas Excel writer and output the Excel file.
        writer.save()

    @staticmethod
    def create_dataframe(data: {}):
        df = pd.DataFrame(data)
        return data


if __name__ == '__main__':
    Files.create_template()
