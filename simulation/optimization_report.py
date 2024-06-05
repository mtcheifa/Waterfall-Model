class OptimizationReport:
    def __init__(self, stage_input, phase_input, mean_wait_time_input, iteration_input, original_resource_value_input, resource_value_input):
        self.stage = stage_input
        self.phase = phase_input
        self.mean_wait_time = mean_wait_time_input
        self.iteration = iteration_input
        self.resource_value = resource_value_input
        self.original_resource_value = original_resource_value_input
