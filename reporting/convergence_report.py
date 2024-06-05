import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

class ConvergenceReport:
    def __init__(self, phases_df):
        self.phases_df = phases_df

    def report_on_convergence_by_difference(self):
        pre_optimization_df = self.phases_df[self.phases_df['Stage'] == 'pre-optimization']
        mean_durations = pre_optimization_df.groupby(['Iteration', 'Phase'])['Phase Duration'].mean().unstack()
        diff_of_means = mean_durations.diff(axis=0)
        print("Mean Durations:")
        print(mean_durations)
        print("\nDifferences of Means between Iterations:")
        print(diff_of_means)

    def table6_figure_2_report_on_convergence(self):
        pre_optimization_df = self.phases_df[self.phases_df['Stage'] == 'pre-optimization']
        mean_durations = pre_optimization_df.groupby(['Iteration', 'Phase'])['Phase Duration'].mean().unstack()
        print(mean_durations)
        sns.set(style='darkgrid')
        mean_durations.plot(kind='line')
        plt.xlabel('Iteration', fontweight='bold')
        plt.ylabel('Mean Duration (in units of time)', fontweight='bold')
        plt.title('Convergence of Phase Durations in pre-optimization stage', fontweight='bold')
        plt.legend(title='Phases')
        plt.show()
