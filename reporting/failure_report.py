import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from IPython.display import display


class FailureReport:
    def __init__(self, phases_df, failures_df):
        self.phases_df = phases_df
        self.failures_df = failures_df

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
