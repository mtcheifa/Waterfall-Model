import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

class ConvergenceReport:
    def __init__(self, phases_df):
        self.phases_df = phases_df

    def table6_figure_2_report_on_convergence(self):
        pre_optimization_df = self.phases_df[self.phases_df['Stage'] == 'pre-optimization']
        mean_durations = pre_optimization_df.groupby(['Iteration', 'Phase'])['Phase Duration'].mean().unstack()
        self._plot_convergence(mean_durations, "Convergence of Phase Durations in pre-optimization stage")

    def _plot_convergence(self, df, title):
        sns.set(style='darkgrid')
        df.plot(kind='line')
        plt.xlabel('Iteration', fontweight='bold')
        plt.ylabel('Mean Duration (in units of time)', fontweight='bold')
        plt.title(title, fontweight='bold')
        plt.legend(title='Phases')
        plt.show()
