import pandas as pd

class DataLoader:
    def __init__(self):
        self.project_df = pd.read_csv('project_data.csv')
        self.resources_df = pd.read_csv('resources_report.csv')
        self.phases_df = pd.read_csv('phases_report.csv')
        self.failures_df = pd.read_csv('failures_report.csv')
        self.optimization_df = pd.read_csv('optimization.csv')
        pd.set_option('display.max_rows', None)
        pd.set_option('display.max_columns', None)

    def get_project_data(self):
        return self.project_df

    def get_resources_data(self):
        return self.resources_df

    def get_phases_data(self):
        return self.phases_df

    def get_failures_data(self):
        return self.failures_df

    def get_optimization_data(self):
        return self.optimization_df
