import pandas as pd

class DataLoader:
    def __init__(self):
        """
        Initialize the DataLoader by loading data from CSV files.
        """
        self.project_df = pd.read_csv('project_data.csv')
        self.resources_df = pd.read_csv('resources_report.csv')
        self.phases_df = pd.read_csv('phases_report.csv')
        self.failures_df = pd.read_csv('failures_report.csv')
        self.optimization_df = pd.read_csv('optimization.csv')
        
        pd.set_option('display.max_rows', None)
        pd.set_option('display.max_columns', None)

    def get_data(self):
        """
        Get all loaded data as a dictionary.
        
        :return: Dictionary containing all dataframes
        """
        return {
            'project_df': self.project_df,
            'resources_df': self.resources_df,
            'phases_df': self.phases_df,
            'failures_df': self.failures_df,
            'optimization_df': self.optimization_df
        }
