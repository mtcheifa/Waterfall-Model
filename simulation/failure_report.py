class FailureReport:
    def __init__(self, stage_input, current_phase_input, fail_to_phase_input, software_house_id_input, project_id_input, timestamp_input, project_scale_input):
        self.stage = stage_input
        self.current_phase = current_phase_input
        self.fail_to_phase = fail_to_phase_input
        self.software_house_id = software_house_id_input
        self.project_id = project_id_input
        self.timestamp = timestamp_input
        self.project_scale = project_scale_input
