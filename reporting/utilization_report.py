import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

class UtilizationReport:
    def __init__(self, phases_df, resources_df):
        self.phases_df = phases_df
        self.resources_df = resources_df

    def table7_count_bottle_neck_pre_optimization(self):
        # Filter the data for the "pre-optimization" stage
        pre_optimization_data = self.phases_df[self.phases_df['Stage'] == 'pre-optimization']

        # Filter the data for wait times greater than zero
        wait_times_greater_than_zero = pre_optimization_data[pre_optimization_data['Wait Time to Obtain Resources'] > 0]

        # Group the data by phase, iteration, and project scale and count the number of wait times
        wait_times_count = wait_times_greater_than_zero.groupby(['Phase', 'Iteration', 'Project Scale'])[
            'Wait Time to Obtain Resources'].count()

        # Convert the result to a DataFrame and reset the index
        wait_times_count_df = wait_times_count.reset_index()

        # Compute the mean across all iterations
        mean_wait_time = wait_times_count_df['Wait Time to Obtain Resources'].mean()

        # Group the data by phase and calculate the total wait time
        total_wait_time_by_phase = wait_times_count_df.groupby('Phase')['Wait Time to Obtain Resources'].sum()

        pd.set_option('display.max_columns', None)
        pd.set_option('display.max_rows', None)

        # Print the total wait time by phase
        print("Total Wait Time by Phase:")
        print(total_wait_time_by_phase)

        total_wait_time_by_phase.to_csv('table7a_count_bottle_neck_pre_optimization.csv', index=False)

        # Filter the DataFrame to include only the "pre-optimization" stage
        pre_optimization_df = self.phases_df[self.phases_df['Stage'] == 'pre-optimization']

        # Group the DataFrame by phase and project scale, and count the number of occurrences
        wait_time_counts = pre_optimization_df[pre_optimization_df['Wait Time to Obtain Resources'] > 0].groupby(
            ['Phase', 'Project Scale']).size()

        # Print the report
        print("Wait Time Report - Pre-Optimization (Grouped by Project Size)")
        print("------------------------------------------------------------")
        print(wait_time_counts)

        wait_time_counts.to_csv('table7b_count_bottle_neck_pre_optimization.csv', index=False)

        # Filter the DataFrame by stage and select the relevant columns
        pre_optimization_phases_df = self.phases_df[self.phases_df['Stage'] == 'pre-optimization']
        pre_optimization_phases_df = pre_optimization_phases_df[['Phase', 'Wait Time to Obtain Resources']]

        # Group the data by phase and calculate the sum, mean, and count
        wait_time_summary = pre_optimization_phases_df.groupby('Phase')['Wait Time to Obtain Resources'].agg(
            ['sum', 'mean', 'count'])

        # Display the report
        print(wait_time_summary)
        wait_time_summary.to_csv('table7c_count_bottle_neck_pre_optimization.csv', index=False)

        # Filter the DataFrame by stage and select the relevant columns
        pre_optimization_phases_by_size_df = self.phases_df[self.phases_df['Stage'] == 'pre-optimization']
        pre_optimization_phases_by_size_df = pre_optimization_phases_by_size_df[
            ['Phase', 'Project Scale', 'Wait Time to Obtain Resources']]

        # Group the data by phase and project size and calculate the sum, mean, and count
        wait_time_summary_by_size = pre_optimization_phases_by_size_df.groupby(['Phase', 'Project Scale'])[
            'Wait Time to Obtain Resources'].agg(['sum', 'mean', 'count'])

        # Display the report
        print(wait_time_summary_by_size)
        wait_time_summary_by_size.to_csv('table7d_count_bottle_neck_pre_optimization.csv', index=False)

    def figure3(self):
        filtered_resources = self.resources_df[(self.resources_df['Stage'] == 'pre-optimization') & (self.resources_df['Iteration'] == 1)]
        resource_types = filtered_resources['Resource Type'].unique()
        for resource_type in resource_types:
            resource_data = filtered_resources[filtered_resources['Resource Type'] == resource_type]
            self._plot_resources_available(resource_data, resource_type)

    def _plot_resources_available(self, df, resource_type):
        plt.figure(figsize=(10, 6))
        plt.step(df['Timestamp'], df['Resources Available'], where='post')
        plt.xlabel('Time')
        plt.ylabel('Resources Available')
        plt.title(f'Resources Available for {resource_type.capitalize()} (Pre-Optimization, Iteration 1)')
        plt.xticks(rotation=45)
        plt.xlim(0, 400)
        plt.show()
