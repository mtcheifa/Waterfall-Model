import pandas as pd

class SimulationReport:
    def __init__(self, projects_log, resources_log, phases_log, failures_log, optimization_log):
        self.projects_log = projects_log
        self.resources_log = resources_log
        self.phases_log = phases_log
        self.failures_log = failures_log
        self.optimization_log = optimization_log

    def table9_report_on_project_completion_times(self):
        pre_optimization_project_df = self.projects_log[self.projects_log['Stage'] == 'pre-optimization']
        pre_optimization_duration_stats_by_scale = pre_optimization_project_df.groupby('Project Scale')['Duration'].agg(['min', 'max', 'mean'])
        print("Pre-Optimization Project Duration Statistics by Project Scale:")
        print(pre_optimization_duration_stats_by_scale)
        pre_optimization_duration_stats_by_scale.to_csv("table9a_report_on_project_completion_times.csv", header=True)

        pre_optimization_duration_stats = pre_optimization_project_df['Duration'].agg(['min', 'max', 'mean'])
        print("Pre-Optimization Project Duration Statistics Across All Project Scales:")
        print(pre_optimization_duration_stats)
        pre_optimization_duration_stats.to_csv("table9b_report_on_project_completion_times.csv", header=True)

        post_optimization_project_df = self.projects_log[self.projects_log['Stage'] == 'post-optimization']
        post_optimization_duration_stats_by_scale = post_optimization_project_df.groupby('Project Scale')['Duration'].agg(['min', 'max', 'mean'])
        print("Post-Optimization Project Duration Statistics by Project Scale:")
        print(post_optimization_duration_stats_by_scale)
        post_optimization_duration_stats_by_scale.to_csv("table9c_report_on_project_completion_times.csv", header=True)

        post_optimization_duration_stats = post_optimization_project_df['Duration'].agg(['min', 'max', 'mean'])
        print("Post-Optimization Project Duration Statistics Across All Project Scales:")
        print(post_optimization_duration_stats)
        post_optimization_duration_stats.to_csv("table9d_report_on_project_completion_times.csv", header=True)

    def table10_report_on_phase_completion_times_by_phase(self):
        pre_optimization_phases = self.phases_log[self.phases_log["Stage"] == "pre-optimization"]
        phase_stats = pre_optimization_phases.groupby(["Project Scale", "Phase"])["Phase Duration"].agg(["min", "max", "mean"])
        print("Phase Duration Statistics (Pre-Optimization):\n")
        print(phase_stats)
        phase_stats.to_csv("table10_report_on_phase_completion_times_by_phase.csv")

        post_optimization_phases = self.phases_log[self.phases_log["Stage"] == "post-optimization"]
        phase_stats2 = post_optimization_phases.groupby(["Project Scale", "Phase"])["Phase Duration"].agg(["min", "max", "mean"])
        print("Phase Duration Statistics (Post-Optimization):\n")
        print(phase_stats2)
        phase_stats2.to_csv("table10_report_on_phase_completion_times_by_phase.csv")

    def _create_and_save_dataframe(self, data, filename, columns):
        df = pd.DataFrame(data, columns=columns)
        print(f"Generated {filename} with columns: {columns}")
        df.to_csv(filename, index=False)
