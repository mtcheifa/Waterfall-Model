import simpy

class SoftwareHouse:
    def __init__(self, env, stage_input, id_input, resources_input):
        self.env = env
        self.stage = stage_input
        self.id = id_input
        self.resources = {resource: simpy.Container(env, init=amount) for resource, amount in resources_input.items()}
