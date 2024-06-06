from reporting.convergence_report import ConvergenceReport
from reporting.failure_report import FailureReport
from reporting.resource_optimization_report import ResourceOptimizationReport
from reporting.simulation_report import SimulationReport
from reporting.utilization_report import UtilizationReport
from reporting.wait_time_report import WaitTimeReport

class ReportingManager:
    def __init__(self, data):
        """
        Initialize the ReportingManager with the required data.
        
        :param data: Dictionary containing all dataframes
        """
        self.data = data
        self.convergence_report = ConvergenceReport(data['phases_df'])
        self.failure_report = FailureReport(data['phases_df'], data['failures_df'])
        self.resource_optimization_report = ResourceOptimizationReport(data['optimization_df'])
        self.simulation_report = SimulationReport(data['project_df'], data['resources_df'], data['phases_df'], data['failures_df'], data['optimization_df'])
        self.utilization_report = UtilizationReport(data['phases_df'], data['resources_df'])
        self.wait_time_report = WaitTimeReport(data['phases_df'])

    def generate_all_reports(self):
        """
        Generates all reports.
        """
        self.table6_figure_2_report_on_convergence()
        self.table7_count_bottle_neck_pre_optimization()
        self.table8_optimized_resources_report()
        self.table9_report_on_project_completion_times()
        self.table10_report_on_phase_completion_times_by_phase()
        self.table11_part1_report_on_wait_time()
        self.table11_part2_report_on_wait_time()
        self.table11_part3_report_on_wait_time()
        self.table11_part4_report_on_wait_time()
        self.table12_part1_failure_report()
        self.table12_part2_failure_report()
        self.table12_part3_failure_report()
        self.table12_part4_failure_report()
        self.table12_figure4_failure_report()
        self.figure3()

    def table6_figure_2_report_on_convergence(self):
        self.convergence_report.table6_figure_2_report_on_convergence()

    def table7_count_bottle_neck_pre_optimization(self):
        self.utilization_report.table7_count_bottle_neck_pre_optimization()

    def table8_optimized_resources_report(self):
        self.resource_optimization_report.table8_optimized_resources_report()

    def table9_report_on_project_completion_times(self):
        self.simulation_report.table9_report_on_project_completion_times()

    def table10_report_on_phase_completion_times_by_phase(self):
        self.simulation_report.table10_report_on_phase_completion_times_by_phase()

    def table11_part1_report_on_wait_time(self):
        self.wait_time_report.table11_part1_report_on_wait_time()

    def table11_part2_report_on_wait_time(self):
        self.wait_time_report.table11_part2_report_on_wait_time()

    def table11_part3_report_on_wait_time(self):
        self.wait_time_report.table11_part3_report_on_wait_time()

    def table11_part4_report_on_wait_time(self):
        self.wait_time_report.table11_part4_report_on_wait_time()

    def table12_part1_failure_report(self):
        self.failure_report.table12_part1_failure_report()

    def table12_part2_failure_report(self):
        self.failure_report.table12_part2_failure_report()

    def table12_part3_failure_report(self):
        self.failure_report.table12_part3_failure_report()

    def table12_part4_failure_report(self):
        self.failure_report.table12_part4_failure_report()

    def table12_figure4_failure_report(self):
        self.failure_report.table12_figure4_failure_report()

    def figure3(self):
        self.utilization_report.figure3()
