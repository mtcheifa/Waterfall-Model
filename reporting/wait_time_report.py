import pandas as pd

class WaitTimeReport:
    def __init__(self, phases_df):
        self.phases_df = phases_df

    def table11_part1_report_on_wait_time(self):
        def count_non_zero(x):
            return (x > 0).sum()
        wait_time_stats_by_stage_phase_size = self.phases_df.groupby(['Stage', 'Phase', 'Project Scale'])['Wait Time to Obtain Resources'].agg(['count', 'mean', 'min', 'max', count_non_zero])
        wait_time_stats_by_stage_phase_size = wait_time_stats_by_stage_phase_size.rename(columns={"count_non_zero": "Count > 0"})
        wait_time_stats_by_stage_phase_size = wait_time_stats_by_stage_phase_size.sort_values(by=['Stage', 'mean'], ascending=[True, False])
        report_df = pd.DataFrame({
            'Stage': wait_time_stats_by_stage_phase_size.index.get_level_values(0),
            'Phase': wait_time_stats_by_stage_phase_size.index.get_level_values(1),
            'Project Scale': wait_time_stats_by_stage_phase_size.index.get_level_values(2),
            'Count': wait_time_stats_by_stage_phase_size['count'],
            'Count > 0': wait_time_stats_by_stage_phase_size['Count > 0'],
            'Mean Wait Time': wait_time_stats_by_stage_phase_size['mean'],
            'Min Wait Time': wait_time_stats_by_stage_phase_size['min'],
            'Max Wait Time': wait_time_stats_by_stage_phase_size['max']
        })
        self._display_and_save(report_df, 'table11_part1_report_on_wait_time.csv', 'Wait Time Report Part 1')

    def table11_part2_report_on_wait_time(self):
        def count_non_zero(x):
            return (x > 0).sum()
        wait_time_stats_by_stage_phase = self.phases_df.groupby(['Stage', 'Phase'])['Wait Time to Obtain Resources'].agg(['count', 'mean', 'min', 'max', count_non_zero])
        wait_time_stats_by_stage_phase = wait_time_stats_by_stage_phase.rename(columns={"count_non_zero": "Count > 0"})
        report_df = pd.DataFrame({
            'Stage': wait_time_stats_by_stage_phase.index.get_level_values(0),
            'Phase': wait_time_stats_by_stage_phase.index.get_level_values(1),
            'Count': wait_time_stats_by_stage_phase['count'],
            'Count > 0': wait_time_stats_by_stage_phase['Count > 0'],
            'Mean Wait Time': wait_time_stats_by_stage_phase['mean'],
            'Min Wait Time': wait_time_stats_by_stage_phase['min'],
            'Max Wait Time': wait_time_stats_by_stage_phase['max']
        })
        self._display_and_save(report_df, 'table11_part2_report_on_wait_time.csv', 'Wait Time Report Part 2')

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

    def _display_and_save(self, df, filename, table_name):
        print(f"{table_name}:")
        print(df)
        df.to_csv(filename, index=False)
