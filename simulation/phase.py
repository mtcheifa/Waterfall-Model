import random

from settings import PHASES, PROJECT_TYPES

class Phase:
    def __init__(self, name, resource_type):
        self.name = name
        self.resource_type = resource_type
        self.start_time = 0
        self.end_time = 0
        self.duration = 0
        self.wait_time = 0

    def perform_phase_actions(self, env, project, software_house):
        resource_type = self.resource_type
        resource_request_time = env.now
        yield from project.project_resource_request(software_house.stage, resource_type,
                                                    PROJECT_TYPES[project.project_scale]['requirements'][resource_type])
        self.start_time = env.now
        duration = round(random.uniform(*PHASES[self.name]['duration_range']))
        yield env.timeout(duration)
        self.end_time = env.now
        yield from project.project_resource_release(software_house.stage, resource_type,
                                                    PROJECT_TYPES[project.project_scale]['requirements'][resource_type])
        self.duration = self.end_time - self.start_time
        self.wait_time = self.start_time - resource_request_time
