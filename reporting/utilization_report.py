import matplotlib.pyplot as plt
import seaborn as sns

class UtilizationReport:
    def __init__(self, phases_df, resources_df):
        self.phases_df = phases_df
        self.resources_df = resources_df

    def report_on_resource_utilization(self):
        utilization_df = self.phases_df[self.phases_df['Stage'] == 'utilization']
        mean_utilization = utilization_df.groupby(['Iteration', 'Resource'])['Utilization'].mean().unstack()
        print("Mean Resource Utilization:")
        print(mean_utilization)

    def figure3(self):
        filtered_resources = self.resources_df[(self.resources_df['Stage'] == 'pre-optimization') & (self.resources_df['Iteration'] == 1)]
        resource_types = filtered_resources['Resource Type'].unique()
        for resource_type in resource_types:
            resource_data = filtered_resources[filtered_resources['Resource Type'] == resource_type]
            plt.figure(figsize=(10, 6))
            plt.step(resource_data['Timestamp'], resource_data['Resources Available'], where='post')
            plt.xlabel('Time')
            plt.ylabel('Resources Available')
            plt.title(f'Resources Available for {resource_type.capitalize()} (Pre-Optimization, Iteration 1)')
            plt.xticks(rotation=45)
            plt.xlim(0, 400)
            plt.show()
