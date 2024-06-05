import pandas as pd
from reporting.reporting_manager import ReportingManager

def main():
    phases_df = pd.read_csv('phases_report.csv')
    failures_df = pd.read_csv('failures_report.csv')
    resources_df = pd.read_csv('resources_report.csv')
    project_df = pd.read_csv('project_data.csv')
    optimization_df = pd.read_csv('optimization.csv')

    manager = ReportingManager(phases_df, failures_df, resources_df, project_df, optimization_df)

    # Call all the reporting methods
    manager.table6_figure_2_report_on_convergence()
    manager.table7_count_bottle_neck_pre_optimization()
    manager.table8_optimized_resources_report()
    manager.table9_report_on_project_completion_times()
    manager.table10_report_on_phase_completion_times_by_phase()
    manager.table11_part1_report_on_wait_time()
    manager.table11_part2_report_on_wait_time()
    manager.table11_part3_report_on_wait_time()
    manager.table11_part4_report_on_wait_time()
    manager.table12_part1_failure_report()
    manager.table12_part2_failure_report()
    manager.table12_part3_failure_report()
    manager.table12_part4_failure_report()
    manager.table12_figure4_failure_report()
    manager.figure3()

if __name__ == "__main__":
    main()
