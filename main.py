import pandas as pd
from reporting.reporting_manager import ReportingManager

def main():
    phases_df = pd.read_csv('phases_report.csv')
    failures_df = pd.read_csv('failures_report.csv')
    resources_df = pd.read_csv('resources_report.csv')
    project_df = pd.read_csv('project_data.csv')
    optimization_df = pd.read_csv('optimization.csv')

    data = {
        'phases_df': phases_df,
        'failures_df': failures_df,
        'resources_df': resources_df,
        'project_df': project_df,
        'optimization_df': optimization_df
    }

    manager = ReportingManager(data)

    # Call all the reporting methods
    manager.generate_all_reports()

if __name__ == "__main__":
    main()
