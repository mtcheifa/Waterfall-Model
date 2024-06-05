class PhasesReport:
    def __init__(self, stage_input, phase_input, phase_start_input, phase_end_input, phase_duration_input, software_house_id_input, project_id_input, project_scale_input, timestamp_input, resources_obtain_time_input):
        self.stage = stage_input
        self.phase = phase_input
        self.phase_start = phase_start_input
        self.phase_end = phase_end_input
        self.phase_duration = phase_duration_input
        self.software_house_id = software_house_id_input
        self.project_id = project_id_input
        self.project_scale = project_scale_input
        self.timestamp = timestamp_input
        self.resources_obtain_time = resources_obtain_time_input
