import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from IPython.display import display

class ReportingManager:
    def __init__(self, phases_df, failures_df, resources_df, project_df, optimization_df):
        self.phases_df = phases_df
        self.failures_df = failures_df
        self.resources_df = resources_df
        self.project_df = project_df
        self.optimization_df = optimization_df

    def table12_part1_failure_report(self):
        failure_counts = self.failures_df.groupby(['Stage', 'Project Scale', 'Current Phase']).size().reset_index(name='Phase Failures')
        total_phases = self.phases_df.groupby(['Stage', 'Project Scale', 'Phase']).size().reset_index(name='Total Phases')
        phase_failure_table = failure_counts.merge(total_phases, left_on=['Stage', 'Project Scale', 'Current Phase'], right_on=['Stage', 'Project Scale', 'Phase'], how='left').fillna(0)
        phase_failure_table = phase_failure_table[phase_failure_table['Stage'] != 'optimizing']
        phase_failure_table['Percentage'] = (phase_failure_table['Phase Failures'] / phase_failure_table['Total Phases']) * 100
        print("Phase Failure Table:")
        display(phase_failure_table)
        phase_failure_table.to_csv("table12_part1_failure_report.csv", index=False)

    def table12_part2_failure_report(self):
        filtered_failures_df = self.failures_df[self.failures_df['Stage'] != 'optimizing']
        filtered_phases_df = self.phases_df[self.phases_df['Stage'] != 'optimizing']
        failure_counts = filtered_failures_df.groupby(['Stage', 'Project Scale']).size().reset_index(name='Phase Failure Count')
        phase_counts = filtered_phases_df.groupby(['Stage', 'Project Scale']).size().reset_index(name='Total Phase Count')
        report_table = pd.merge(failure_counts, phase_counts, on=['Stage', 'Project Scale'], how='outer')
        report_table['Phase Failure Count'].fillna(0, inplace=True)
        report_table['Percentage'] = (report_table['Phase Failure Count'] / report_table['Total Phase Count']) * 100
        display(report_table)
        report_table.to_csv("table12_part2_failure_report.csv", index=False)

    def table12_part3_failure_report(self):
        phase_failures_table = pd.pivot_table(self.failures_df, index=['Stage', 'Current Phase'], values='Iteration', aggfunc='count')
        phase_failures_table.reset_index(inplace=True)
        phase_failures_table.columns = ['Stage', 'Phase', 'Number of Failures']
        total_phases_table = pd.pivot_table(self.phases_df, index=['Stage', 'Phase'], values='Iteration', aggfunc='count')
        total_phases_table.reset_index(inplace=True)
        total_phases_table.columns = ['Stage', 'Phase', 'Total Phases']
        phase_stats_table = pd.merge(phase_failures_table, total_phases_table, on=['Stage', 'Phase'], how='left')
        phase_stats_table['Percentage'] = (phase_stats_table['Number of Failures'] / phase_stats_table['Total Phases']) * 100
        phase_stats_table = phase_stats_table[phase_stats_table['Stage'] != 'optimizing']
        display(phase_stats_table)
        phase_stats_table.to_csv("table12_part3_failure_report.csv", index=False)

    def table12_part4_failure_report(self):
        failures_limited_df = self.failures_df[self.failures_df['Stage'] != 'optimizing']
        stage_failures_table = failures_limited_df.groupby('Stage')['Iteration'].count().reset_index()
        stage_counts = self.phases_df['Stage'].value_counts().reset_index()
        stage_counts.columns = ['Stage', 'Total Phases']
        stage_failures_table = stage_failures_table.merge(stage_counts, on='Stage', how='inner')
        stage_failures_table['Percentage'] = (stage_failures_table['Iteration'] / stage_failures_table['Total Phases']) * 100
        print("Phase Failures Table by Stage:")
        print(stage_failures_table)
        stage_failures_table.to_csv("table12_part4_failure_report.csv", index=False)

    def table12_figure4_failure_report(self):
        filtered_failures_df = self.failures_df[self.failures_df['Stage'] != 'optimizing']
        filtered_phases_df = self.phases_df[self.phases_df['Stage'] != 'optimizing']
        failure_counts = filtered_failures_df.groupby(['Stage', 'Project Scale']).size().reset_index(name='Phase Failure Count')
        phase_counts = filtered_phases_df.groupby(['Stage', 'Project Scale']).size().reset_index(name='Total Phase Count')
        report_table = pd.merge(failure_counts, phase_counts, on=['Stage', 'Project Scale'], how='outer')
        report_table['Phase Failure Count'].fillna(0, inplace=True)
        report_table['Percentage'] = (report_table['Phase Failure Count'] / report_table['Total Phase Count']) * 100
        report_table['Diff'] = report_table['Total Phase Count'] - report_table['Phase Failure Count']
        display(report_table)
        grouped_table = report_table.groupby(['Stage', 'Project Scale']).sum().reset_index()
        plt.figure(figsize=(10, 6))
        sns.set(style='whitegrid')
        unique_scales = grouped_table['Project Scale'].unique()
        bar_width = 0.2
        x = np.arange(len(grouped_table['Stage'].unique()))
        colors = sns.color_palette('colorblind', n_colors=len(unique_scales))
        for i, scale in enumerate(unique_scales):
            scale_data = grouped_table[grouped_table['Project Scale'] == scale]
            phase_failure = scale_data['Phase Failure Count']
            diff = scale_data['Diff']
            plt.bar(x + i * bar_width, phase_failure, width=bar_width, label=f'{scale} - Phase Failure', color=colors[i])
            plt.bar(x + i * bar_width, diff, width=bar_width, label=f'{scale} - Diff', bottom=phase_failure, color=colors[i], alpha=0.7)
        plt.xticks(x + bar_width * len(unique_scales) / 2, grouped_table['Stage'].unique())
        plt.title('Failure Report')
        plt.xlabel('Stage')
        plt.ylabel('Count')
        plt.legend(title='Project Scale')
        plt.show()

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

    def table8_optimized_resources_report(self):
        grouped_data = self.optimization_df.groupby("Phase")
        phase_names = []
        original_resources = []
        final_resources = []
        steps_to_optimum = []
        for phase, group in grouped_data:
            phase_names.append(phase)
            original_resources.append(group["Original Number of Resources"].iloc[0])
            final_resources.append(group["Number of Resources"].iloc[-1])
            steps_to_optimum.append(group.shape[0])
        report_df = pd.DataFrame({
            "Phase": phase_names,
            "Original Resources": original_resources,
            "Final Resources": final_resources,
            "Steps to Optimum": steps_to_optimum
        })
        print(report_df)
        report_df.to_csv('table8_optimized_resources_report.csv', index=False)

    def table9_report_on_project_completion_times(self):
        pre_optimization_project_df = self.project_df[self.project_df['Stage'] == 'pre-optimization']
        pre_optimization_duration_stats_by_scale = pre_optimization_project_df.groupby('Project Scale')['Duration'].agg(['min', 'max', 'mean'])
        print("Pre-Optimization Project Duration Statistics by Project Scale:")
        print(pre_optimization_duration_stats_by_scale)
        pre_optimization_duration_stats_by_scale.to_csv("table9a_report_on_project_completion_times.csv", header=True)

        pre_optimization_duration_stats = pre_optimization_project_df['Duration'].agg(['min', 'max', 'mean'])
        print("Pre-Optimization Project Duration Statistics Across All Project Scales:")
        print(pre_optimization_duration_stats)
        pre_optimization_duration_stats_by_scale.to_csv("table9b_report_on_project_completion_times.csv", header=True)

        post_optimization_project_df = self.project_df[self.project_df['Stage'] == 'post-optimization']
        post_optimization_duration_stats_by_scale = post_optimization_project_df.groupby('Project Scale')['Duration'].agg(['min', 'max', 'mean'])
        print("Post-Optimization Project Duration Statistics by Project Scale:")
        print(post_optimization_duration_stats_by_scale)
        post_optimization_duration_stats_by_scale.to_csv("table9c_report_on_project_completion_times.csv", header=True)

        post_optimization_duration_stats = post_optimization_project_df['Duration'].agg(['min', 'max', 'mean'])
        print("Post-Optimization Project Duration Statistics Across All Project Scales:")
        print(post_optimization_duration_stats)
        post_optimization_duration_stats_by_scale.to_csv("table9d_report_on_project_completion_times.csv", header=True)

    def table10_report_on_phase_completion_times_by_phase(self):
        pre_optimization_phases = self.phases_df[self.phases_df["Stage"] == "pre-optimization"]
        phase_stats = pre_optimization_phases.groupby(["Project Scale", "Phase"])["Phase Duration"].agg(["min", "max", "mean"])
        print("Phase Duration Statistics (Pre-Optimization):\n")
        print(phase_stats)
        phase_stats.to_csv("table10_report_on_phase_completion_times_by_phase.csv")

        post_optimization_phases = self.phases_df[self.phases_df["Stage"] == "post-optimization"]
        phase_stats2 = post_optimization_phases.groupby(["Project Scale", "Phase"])["Phase Duration"].agg(["min", "max", "mean"])
        print("Phase Duration Statistics (Post-Optimization):\n")
        print(phase_stats2)
        phase_stats2.to_csv("table10_report_on_phase_completion_times_by_phase.csv")

    def table11_part1_report_on_wait_time(self):
        wait_time_stats_by_stage_phase_size = self.phases_df.groupby(['Stage', 'Phase', 'Project Scale'])['Wait Time to Obtain Resources'].agg(
            count='count', 
            mean='mean', 
            min='min', 
            max='max', 
            count_gt_0=lambda x: (x > 0).sum()
        ).sort_values(by=['Stage', 'mean'], ascending=[True, False])

        report_df = pd.DataFrame({
            'Stage': wait_time_stats_by_stage_phase_size.index.get_level_values(0), 
            'Phase': wait_time_stats_by_stage_phase_size.index.get_level_values(1), 
            'Project Scale': wait_time_stats_by_stage_phase_size.index.get_level_values(2), 
            'Count': wait_time_stats_by_stage_phase_size['count'], 
            'Count > 0': wait_time_stats_by_stage_phase_size['count_gt_0'], 
            'Mean Wait Time': wait_time_stats_by_stage_phase_size['mean'], 
            'Min Wait Time': wait_time_stats_by_stage_phase_size['min'], 
            'Max Wait Time': wait_time_stats_by_stage_phase_size['max']
        })

        print(report_df)
        report_df.to_csv('table11_part1_report_on_wait_time.csv', index=False)

    def table11_part2_report_on_wait_time(self):
        wait_time_stats_by_stage_phase = self.phases_df.groupby(['Stage', 'Phase'])['Wait Time to Obtain Resources'].agg(
            count='count', 
            mean='mean', 
            min='min', 
            max='max', 
            count_gt_0=lambda x: (x > 0).sum()
        ).sort_values(by=['Stage', 'mean'], ascending=[True, False])

        report_df = pd.DataFrame({
            'Stage': wait_time_stats_by_stage_phase.index.get_level_values(0), 
            'Phase': wait_time_stats_by_stage_phase.index.get_level_values(1), 
            'Count': wait_time_stats_by_stage_phase['count'], 
            'Count > 0': wait_time_stats_by_stage_phase['count_gt_0'], 
            'Mean Wait Time': wait_time_stats_by_stage_phase['mean'], 
            'Min Wait Time': wait_time_stats_by_stage_phase['min'], 
            'Max Wait Time': wait_time_stats_by_stage_phase['max']
        })

        print(report_df)
        report_df.to_csv('table11_part2_report_on_wait_time.csv', index=False)

    def table11_part3_report_on_wait_time(self):
        wait_time_stats_by_stage_size = self.phases_df.groupby(['Stage', 'Project Scale'])['Wait Time to Obtain Resources'].agg(
            count='count', 
            mean='mean', 
            min='min', 
            max='max', 
            count_gt_0=lambda x: (x > 0).sum()
        ).sort_values(by=['Stage', 'Project Scale', 'mean'], ascending=[True, True, False])

        report_df = pd.DataFrame({
            'Stage': wait_time_stats_by_stage_size.index.get_level_values(0), 
            'Project Scale': wait_time_stats_by_stage_size.index.get_level_values(1), 
            'Count': wait_time_stats_by_stage_size['count'], 
            'Count > 0': wait_time_stats_by_stage_size['count_gt_0'], 
            'Mean Wait Time': wait_time_stats_by_stage_size['mean'], 
            'Min Wait Time': wait_time_stats_by_stage_size['min'], 
            'Max Wait Time': wait_time_stats_by_stage_size['max']
        })

        print(report_df)
        report_df.to_csv('table11_part3_report_on_wait_time.csv', index=False)

    def table11_part4_report_on_wait_time(self):
        wait_time_stats_by_stage = self.phases_df.groupby(['Stage'])['Wait Time to Obtain Resources'].agg(
            count='count', 
            mean='mean', 
            min='min', 
            max='max', 
            count_gt_0=lambda x: (x > 0).sum()
        ).sort_values(by=['Stage', 'mean'], ascending=[True, False])

        report_df = pd.DataFrame({
            'Stage': wait_time_stats_by_stage.index, 
            'Count': wait_time_stats_by_stage['count'], 
            'Count > 0': wait_time_stats_by_stage['count_gt_0'], 
            'Mean Wait Time': wait_time_stats_by_stage['mean'], 
            'Min Wait Time': wait_time_stats_by_stage['min'], 
            'Max Wait Time': wait_time_stats_by_stage['max']
        })

        print(report_df)
        report_df.to_csv('table11_part4_report_on_wait_time.csv', index=False)

    def table6_figure_2_report_on_convergence(self):
        # Set the pandas options to display all rows and columns
        pd.set_option('display.max_rows', None)
        pd.set_option('display.max_columns', None)

        # Filter the DataFrame for the "pre-optimization" stage
        pre_optimization_df = self.phases_df[self.phases_df['Stage'] == 'pre-optimization']

        # Group the data by iteration and phase, and calculate the mean duration
        mean_durations = pre_optimization_df.groupby(['Iteration', 'Phase'])['Phase Duration'].mean().unstack()

        # Print the mean durations for each phase across iterations
        print(mean_durations)

        # Visualize mean durations as a line graph
        sns.set(style='darkgrid')
        line_colors = {'Design': sns.color_palette('colorblind')[0], 'Implementation': sns.color_palette('colorblind')[9], 'Maintenance': sns.color_palette('colorblind')[7], 'Requirements': sns.color_palette('colorblind')[1], 'Testing': sns.color_palette('colorblind')[7]} # Replace with your custom labels
        mean_durations.plot(kind='line', color=line_colors.values())
        plt.xlabel('Iteration', fontweight='bold')
        plt.ylabel('Mean Duration (in units of time)', fontweight='bold')
        plt.title('Convergence of Phase Durations in pre-optimization stage', fontweight='bold')
        line_labels = ['Design', 'Implementation', 'Maintenance', 'Requirements', 'Testing']  # Replace with your custom labels
        legend_title = 'Phases'  # Replace with your desired title
        legend = plt.legend(line_labels, loc='best')
        legend.set_title(legend_title)
        legend.get_title().set_fontweight('bold')
        plt.show()