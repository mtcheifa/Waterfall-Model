import pandas as pd

class ResourceOptimizationReport:
    def __init__(self, optimization_df):
        self.optimization_df = optimization_df

    def table8_optimized_resources_report(self):
        grouped_data = self.optimization_df.groupby("Phase")
        phase_names, original_resources, final_resources, steps_to_optimum = [], [], [], []
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
        self._display_and_save(report_df, "table8_optimized_resources_report.csv", "Optimized Resources Report")

    def _display_and_save(self, df, filename, report_name):
        print(f"{report_name}:")
        print(df)
        df.to_csv(filename, index=False)
