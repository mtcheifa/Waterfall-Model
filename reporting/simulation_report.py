import pandas as pd

class SimulationReport:
    def __init__(self, projects_log, resources_log, phases_log, failures_log, optimization_log):
        self.projects_log = projects_log
        self.resources_log = resources_log
        self.phases_log = phases_log
        self.failures_log = failures_log
        self.optimization_log = optimization_log

    def generate_report(self):
        project_data = []
        resources_data = []
        phases_data = []
        failures_data = []
        optimization_data = []

        for activity in self.optimization_log:
            optimization_data.append([
                activity.stage, activity.phase, activity.mean_wait_time, activity.iteration, activity.original_resource_value, activity.resource_value
            ])

        for activity in self.projects_log:
            project_completion = "NO" if activity.end_time == 0 else "YES"
            project_data.append([
                activity.stage, activity.software_house_id, activity.id, activity.start_time,
                activity.end_time, activity.duration, activity.project_scale, project_completion
            ])

        for activity in self.resources_log:
            resources_data.append([
                activity.stage, activity.type_of_resource, activity.software_house_id, activity.project_id, activity.resources_available,
                activity.action, activity.timestamp, activity.number_of_resources_request, activity.project_scale
            ])

        for activity in self.phases_log:
            phases_data.append([
                activity.stage, activity.phase, activity.phase_start, activity.phase_end, activity.phase_duration, activity.software_house_id,
                activity.project_id, activity.project_scale, activity.timestamp, activity.resources_obtain_time
            ])

        for activity in self.failures_log:
            failures_data.append([
                activity.stage, activity.current_phase, activity.fail_to_phase, activity.software_house_id, activity.project_id,
                activity.timestamp, activity.project_scale
            ])

        optimization_df = pd.DataFrame(optimization_data, columns=[
            "Stage", "Phase", "Previous Mean Wait Time", "Iteration", "Original Number of Resources", "Number of Resources"
        ])

        project_df = pd.DataFrame(project_data, columns=[
            "Stage", "Iteration", "Project Id", "Project Start Time", "Project End Time", "Duration", "Project Scale", "Project Completion"
        ])

        resources_df = pd.DataFrame(resources_data, columns=[
            "Stage", "Resource Type", "Iteration", "Project Id", "Resources Available", "Action", "Timestamp",
            "Resources Requested", "Project Scale"
        ])

        phases_df = pd.DataFrame(phases_data, columns=[
            "Stage", "Phase", "Phase Start", "Phase End", "Phase Duration", "Iteration", "Project Id", "Project Scale",
            "Timestamp", "Wait Time to Obtain Resources"
        ])

        failures_df = pd.DataFrame(failures_data, columns=[
            "Stage", "Current Phase", "Fail to Phase", "Iteration", "Project Id", "Timestamp", "Project Scale"
        ])

        project_df.to_csv("project_data.csv", index=False, mode='w')
        resources_df.to_csv("resources_report.csv", index=False, mode='w')
        phases_df.to_csv("phases_report.csv", index=False, mode='w')
        failures_df.to_csv("failures_report.csv", index=False, mode='w')
        optimization_df.to_csv("optimization.csv", index=False, mode='w')
