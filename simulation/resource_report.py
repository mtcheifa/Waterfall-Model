class ResourceReport:
    def __init__(self, stage_input, type_of_resource_input, software_house_id_input, project_id_input, resources_available_input, action_input, timestamp_input, number_of_resources_request_input, project_scale_input):
        self.stage = stage_input
        self.type_of_resource = type_of_resource_input
        self.software_house_id = software_house_id_input
        self.project_id = project_id_input
        self.resources_available = resources_available_input
        self.action = action_input
        self.timestamp = timestamp_input
        self.number_of_resources_request = number_of_resources_request_input
        self.project_scale = project_scale_input
