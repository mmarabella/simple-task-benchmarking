from scipy.stats import ttest_rel as ttest
import pandas as pd
import numpy as np


def get_pval(scores1, scores2):
    scores_joined = scores1.join(scores2, how='inner', lsuffix='_1', rsuffix='_2')
    ttest_results = ttest(scores_joined['score_1'], scores_joined['score_2'])
    pval = ttest_results[1]
    if np.isnan(pval):
        pval = 0
    return pval

def read_scores(task, method):
    scores = pd.read_csv(f'results/merge-experiments/scores/{task}_{method.lower()}.csv',
        header=None,
        names=['question', 'score']).set_index('question')
    return scores

def get_formatting_rules(task):
    results_all = pd.read_csv(f'results/merge-experiments/results_{task}.csv')
    results_no_oracle = results_all[results_all['method'].map(lambda x: "ORACLE" not in x)]
    results_no_oracle.set_index('method', inplace=True)

    best_mae = min(results_no_oracle['mae'])
    best_method = results_no_oracle['mae'].idxmin()
    best_scores = read_scores(task, best_method)

    underline = set()
    bold = set()
    for method, row in results_no_oracle.iterrows():
        mae = row['mae']
        scores = read_scores(task, method)
        pval = get_pval(scores, best_scores)
        if pval  > .05:
            bold.add(mae)
        if pval == 0:
            bold.add(mae)
            underline.add(mae)

    return {'underline':underline, 'bold':bold}

def pivot_by_merge(df, method_order):
    df['merge'] = df['method'].map(lambda x: "merge" if "MERGE" in x.upper() else "select")
    df['method'] = df['method'].map(lambda x: "RANDOM" if x == "UNIFORM_MERGE" else x.split('_')[0])
    df['method'] = df['method'].map(lambda x: "MADD" if x == "DEM" else x)
    results_pv = df.pivot_table(columns='merge', values='mae', index='method')
    results_pv.index = pd.Categorical(results_pv.index, method_order)
    results_pv = results_pv.sort_index()
    return results_pv

def format_factory(formatting_rules):
    def format_fn(val):
        if np.isnan(val):
            return "-"
        val_str = str(round(val, 4))
        if val in formatting_rules['bold']:
            val_str = '\\textbf{' + val_str + '}'
        if val in formatting_rules['underline']:
            val_str = '\\underline{' + val_str + '}'
        return val_str

    return format_fn

def print_formatted(results_pv, format_fn, task):
    num_methods = len(results_pv)
    task_pretty = task.split("_")[0].capitalize()
    print('\\midrule')
    print('\\parbox[t]{2mm}{\\multirow{' + str(num_methods) + '}{*}{\\rotatebox[origin=c]{90}{' + task_pretty + '}}} &')
    print('\\parbox[t]{2mm}{\\multirow{' + str(num_methods) + '}{*}{\\rotatebox[origin=c]{90}{Mean}}}')
    first = True
    for idx, row in results_pv.iterrows():
        if first:
            print(f'  & {idx} & {format_fn(row["select"])} & {format_fn(row["merge"])} & - \\\\')
            first = False
        else:
            print(f'& & {idx} & {format_fn(row["select"])} & {format_fn(row["merge"])} & - \\\\')


def main():
    tasks = ['adult_ordinal', 'weather_ordinal', 'similarity', 'emotion']
    method_order = ['RANDOM', 'BAU', 'SAD', 'MAS', 'MADD', 'CATD', 'GPM', 'ORACLE']

    for task in tasks:
        formatting_rules = get_formatting_rules(task)    
        results_all = pd.read_csv(f'results/merge-experiments/results_{task}.csv')
        results_pv = pivot_by_merge(results_all, method_order)
        format_fn = format_factory(formatting_rules)
        print_formatted(results_pv, format_fn, task)


if __name__ == "__main__":
    main()