# simulation_manager.py

import random
import simpy
import pandas as pd
import numpy as np
from optimization_report import OptimizationReport
from settings import PROJECT_TYPES, PHASES, RESOURCES, STAGE, TOTAL_PROJECTS, NEW_PROJECT_ARRIVAL_INTERVAL
from log_manager import (
    projects_log,
    failures_log,
    resources_wait_time_log,
    resources_log,
    phases_log,
    failure_log,
    optimization_log,
    history_phases_log,
    history_failure_log,
    history_resources_log,
    history_resources_wait_time_log,
    history_failures_log,
    history_projects_log
)
from project import Project
from software_house import SoftwareHouse

class SimulationManager:
    def __init__(self):
        self.STAGE = STAGE

    def reset_simulation_data(self):
        history_phases_log.extend(phases_log)
        history_failure_log.extend(failure_log)
        history_resources_log.extend(resources_log)
        history_resources_wait_time_log.extend(resources_wait_time_log)
        history_failures_log.extend(failures_log)
        history_projects_log.extend(projects_log)
        phases_log.clear()
        projects_log.clear()
        failures_log.clear()
        resources_wait_time_log.clear()
        resources_log.clear()
        failure_log.clear()
        optimization_log.clear()

    def optimize_resource(self, stage, phase, resource_name, min_value, max_value, initial_step_size):
        iterations = 0
        step_size = initial_step_size
        best_mean = self.get_mean_wait_time(phase)
        starting_resource_value = RESOURCES[resource_name]

        min_step_size = 1
        no_improvements = 0
        max_no_improvements = 10

        while step_size >= min_step_size:
            for direction in [1, -1]:
                iterations += 1
                old_resource_value = RESOURCES[resource_name]
                RESOURCES[resource_name] += direction * step_size
                RESOURCES[resource_name] = min(max(RESOURCES[resource_name], min_value), max_value)

                self.reset_simulation_data()
                self.simulate(stage)
                new_mean = self.get_mean_wait_time(phase)

                if new_mean >= best_mean:
                    RESOURCES[resource_name] = old_resource_value
                    no_improvements += 1
                else:
                    best_mean = new_mean
                    no_improvements = 0
                    step_size = max(min_step_size, int(abs(new_mean - best_mean) * step_size))

                if no_improvements >= max_no_improvements:
                    RESOURCES[resource_name] = random.randint(min_value, max_value)
                    no_improvements = 0

                optimization_log.append(
                    OptimizationReport(stage, phase, new_mean, iterations, starting_resource_value, RESOURCES[resource_name])
                )

            if RESOURCES[resource_name] == old_resource_value:
                step_size //= 2

        print(f"Optimal Number of {resource_name}:", RESOURCES[resource_name])
        return best_mean

    def optimize_resources(self, stage):
        resource_info = {
            'business_analysts': {
                'phase': 'requirements_analysis',
                'min_value': PROJECT_TYPES['large']['requirements']['business_analysts'],
                'max_value': 200,
                'step_size': 1
            },
            'designers': {
                'phase': 'design',
                'min_value': PROJECT_TYPES['large']['requirements']['designers'],
                'max_value': 200,
                'step_size': 1
            },
            'programmers': {
                'phase': 'implementation',
                'min_value': PROJECT_TYPES['large']['requirements']['programmers'],
                'max_value': 200,
                'step_size': 1
            },
            'testers': {
                'phase': 'testing',
                'min_value': PROJECT_TYPES['large']['requirements']['testers'],
                'max_value': 200,
                'step_size': 1
            },
            'maintenance_people': {
                'phase': 'maintenance',
                'min_value': PROJECT_TYPES['large']['requirements']['maintenance_people'],
                'max_value': 200,
                'step_size': 1
            }
        }

        for resource_name, resource_data in resource_info.items():
            phase = resource_data['phase']
            min_value = resource_data['min_value']
            max_value = resource_data['max_value']
            initial_step_size = resource_data['step_size']
            self.optimize_resource(stage, phase, resource_name, min_value, max_value, initial_step_size)

    def simulate(self, stage):
        RATE_OF_CHANGE_THRESHOLD = 0.01
        MAX_ITERATIONS = 100
        NUM_OF_PHASES = 5
        CONVERGENCE_STREAK_THRESHOLD = 3

        def is_converged(means, prev_means):
            return all(abs((mean - prev_mean) / (prev_mean if prev_mean != 0 else 1)) < RATE_OF_CHANGE_THRESHOLD for mean, prev_mean in zip(means, prev_means))

        output_data = [[] for _ in range(NUM_OF_PHASES)]
        prev_means = [0] * NUM_OF_PHASES
        consecutive_non_improvements = 0
        phases = ['requirements_analysis', 'design', 'implementation', 'testing', 'maintenance']

        for num_iterations in range(1, MAX_ITERATIONS + 1):
            self.reset_simulation_data()
            random.seed(random.random())
            env = simpy.Environment()
            env.process(self.run_software_house(env, stage, num_iterations, RESOURCES))
            env.run(until=num_iterations * 7000)

            for i, phase in enumerate(phases):
                output_data[i].append(self.get_mean_completion_time(phase, num_iterations))

            means = [np.mean(variable_data) for variable_data in output_data]

            if is_converged(means, prev_means):
                consecutive_non_improvements += 1
                if consecutive_non_improvements >= CONVERGENCE_STREAK_THRESHOLD:
                    return
            else:
                consecutive_non_improvements = 0

            prev_means = means

    def run_software_house(self, env, stage, id_input, resources_input):
        software_house = SoftwareHouse(env, stage, id_input, resources_input)
        project_number = 0
        while True:
            new_project_wait_time = random.triangular(*NEW_PROJECT_ARRIVAL_INTERVAL)
            yield env.timeout(new_project_wait_time)
            if project_number < TOTAL_PROJECTS:
                project_number += 1
                project = Project(stage, software_house, project_number)
                projects_log.append(project)
                env.process(project.start_project(stage))

    def get_mean_completion_time(self, phase_name, iteration):
        phases_data_mean_completion_time_with_iteration = []
        for activity in phases_log:
            phases_data_mean_completion_time_with_iteration.append([
                activity.phase, activity.phase_start, activity.phase_end, activity.phase_duration,
                activity.software_house_id,
                activity.project_id, activity.project_scale, activity.timestamp, activity.resources_obtain_time
            ])
        phases_data_mean_completion_time_with_iteration_df = pd.DataFrame(phases_data_mean_completion_time_with_iteration, columns=[
            "Phase", "Phase Start", "Phase End", "Phase Duration", "Iteration", "Project Id", "Project Scale",
            "Timestamp", "Wait Time to Obtain Resources"
        ])
        filtered_data = phases_data_mean_completion_time_with_iteration_df[
            (phases_data_mean_completion_time_with_iteration_df['Phase'] == phase_name) &
            (phases_data_mean_completion_time_with_iteration_df['Iteration'] == iteration)]
        completion_times = filtered_data['Phase Duration']
        if not completion_times.empty:
            mean_completion_time = completion_times.mean()
        else:
            mean_completion_time = 0
        phases_data_mean_completion_time_with_iteration.clear()
        return mean_completion_time

    def get_mean_wait_time(self, phase_name):
        phases_data_mean_wait_time = []
        for activity in phases_log:
            phases_data_mean_wait_time.append([
                activity.phase, activity.phase_start, activity.phase_end, activity.phase_duration, activity.software_house_id,
                activity.project_id, activity.project_scale, activity.timestamp, activity.resources_obtain_time
            ])
        phases_data_mean_wait_time_df = pd.DataFrame(phases_data_mean_wait_time, columns=[
            "Phase", "Phase Start", "Phase End", "Phase Duration", "Iteration", "Project Id", "Project Scale",
            "Timestamp", "Wait Time to Obtain Resources"
        ])
        phase_data_mean_wait_time = phases_data_mean_wait_time_df[phases_data_mean_wait_time_df['Phase'] == phase_name]
        wait_times = phase_data_mean_wait_time['Wait Time to Obtain Resources']
        if not wait_times.empty:
            mean_wait_time = wait_times.mean()
        else:
            mean_wait_time = 0
        phases_data_mean_wait_time.clear()
        return mean_wait_time

    def report(self):
        project_data = []
        resources_data = []
        phases_data = []
        failures_data = []
        optimization_data = []

        for activity in optimization_log:
            optimization_data.append([
                activity.stage, activity.phase, activity.mean_wait_time, activity.iteration, activity.original_resource_value, activity.resource_value
            ])

        for activity in history_projects_log:
            project_completion = "NO" if activity.end_time == 0 else "YES"
            project_data.append([
                activity.stage, activity.software_house_id, activity.id, activity.start_time,
                activity.end_time, activity.duration, activity.project_scale, project_completion
            ])

        for activity in history_resources_log:
            resources_data.append([
                activity.stage, activity.type_of_resource, activity.software_house_id, activity.project_id, activity.resources_available,
                activity.action, activity.timestamp, activity.number_of_resources_request, activity.project_scale
            ])

        for activity in history_phases_log:
            phases_data.append([
                activity.stage, activity.phase, activity.phase_start, activity.phase_end, activity.phase_duration, activity.software_house_id,
                activity.project_id, activity.project_scale, activity.timestamp, activity.resources_obtain_time
            ])

        for activity in history_failures_log:
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

