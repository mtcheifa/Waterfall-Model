import random

from failure_report import FailureReport
from phases_report import PhasesReport
from resource_report import ResourceReport
from settings import PHASES, PROJECT_TYPES
from phase import Phase
from log_manager import resources_log, phases_log, failures_log


class Project:
    def __init__(self, stage_input, software_house_input, id_input):
        self.software_house_id = software_house_input.id
        self.software_house = software_house_input
        self.id = id_input
        self.stage = stage_input
        self.start_time = 0
        self.end_time = 0
        self.duration = 0
        self.project_scale = ""
        self.compute_project_scale()

    def compute_project_scale(self):
        option = random.uniform(0, 1)
        cumulative_proportion = 0
        for project_type, item in PROJECT_TYPES.items():
            cumulative_proportion += item['proportion']
            if option <= cumulative_proportion:
                self.project_scale = project_type
                break

    def get_failure_probability(self):
        failure_probability = PROJECT_TYPES[self.project_scale]['error_probability']
        return failure_probability

    def log_resource(self, stage: str, resource_type: str, status: str, number_of_resources: int):
        resource = self.software_house.resources[resource_type]
        resources_log.append(ResourceReport(stage, resource_type, self.software_house.id, self.id, resource.level, status, self.software_house.env.now, number_of_resources, self.project_scale))
        return resource

    def project_resource_request(self, stage: str, resource_type: str, number_of_resources: int):
        resource = self.log_resource(stage, resource_type, "request", number_of_resources)
        yield resource.get(number_of_resources)
        self.log_resource(stage, resource_type, "obtain", number_of_resources)

    def project_resource_release(self, stage: str, resource_type: str, number_of_resources: int):
        resource = self.log_resource(stage, resource_type, "release", number_of_resources)
        yield resource.put(number_of_resources)
        self.log_resource(stage, resource_type, "after release", number_of_resources)

    def project_phase(self, stage, phase_name, resource_type):
        current_phase = phase_name
        phase_start = self.software_house.env.now
        phase = Phase(phase_name, resource_type)
        yield from phase.perform_phase_actions(self.software_house.env, self, self.software_house)
        phase_end = self.software_house.env.now
        time_for_phase = phase_end - phase_start
        self.log_phase_info(stage, phase_name, phase_start, phase_end, time_for_phase, phase.wait_time)

        if self.check_for_failure(phase_name):
            previous_phase_name, previous_phase_resource = self.get_previous_phase_info(phase_name)
            failures_log.append(FailureReport(stage, current_phase, previous_phase_name, self.software_house.id, self.id, self.software_house.env.now, self.project_scale))
            yield from self.project_phase(stage, previous_phase_name, previous_phase_resource)
        elif self.is_not_last_phase(phase_name):
            next_phase_name, next_phase_resource = self.get_next_phase_info(phase_name)
            yield from self.project_phase(stage, next_phase_name, next_phase_resource)

    def check_for_failure(self, phase_name: str):
        phase_names = list(PHASES.keys())
        current_phase_index = phase_names.index(phase_name)
        random_number = random.uniform(0, 1)
        if (random_number <= self.get_failure_probability()) and (current_phase_index > 0):
            return True
        return False

    def get_next_phase_info(self, phase_name: str):
        phase_names = list(PHASES.keys())
        next_phase_index = (phase_names.index(phase_name) + 1) % len(phase_names)
        next_phase_name = phase_names[next_phase_index]
        next_phase_resource = PHASES[next_phase_name]['resource']
        return next_phase_name, next_phase_resource

    def get_previous_phase_info(self, phase_name: str):
        phase_names = list(PHASES.keys())
        current_phase_index = phase_names.index(phase_name)
        previous_phase_index = current_phase_index - 1
        previous_phase_name = phase_names[previous_phase_index]
        previous_phase_resource = PHASES.get(previous_phase_name, {}).get('resource')
        return previous_phase_name, previous_phase_resource

    def log_phase_info(self, stage: str, phase_name: str, phase_start: float, phase_end: float, time_for_phase: float, time_to_obtain_resources: float):
        phases_log.append(PhasesReport(stage, phase_name, phase_start, phase_end, time_for_phase, self.software_house_id, self.id, self.project_scale, self.software_house.env.now, time_to_obtain_resources))

    def is_not_last_phase(self, phase_name: str):
        phase_names = list(PHASES.keys())
        current_phase_index = phase_names.index(phase_name)
        return current_phase_index != len(phase_names) - 1

    def start_project(self, stage):
        self.start_time = self.software_house.env.now
        first_phase_name, first_phase_details = next(iter(PHASES.items()))
        first_resource = first_phase_details['resource']
        yield from self.project_phase(stage, first_phase_name, first_resource)
        self.end_time = self.software_house.env.now
        self.duration = self.end_time - self.start_time
