import pandas as pd
import numpy as np
import scipy.stats


def conf_interval(data, conf_level=0.95):
    n = len(data)
    mu = np.mean(data)
    stderr = scipy.stats.sem(data)
    x = stderr * scipy.stats.t.ppf((1 + conf_level) / 2., n-1)
    # upper = mu + x
    # lower = mu - x
    return mu, x

def plus_minus(data):
    mu, x = conf_interval(data)
    return f'{round(mu, 3)} ({round(x, 3)})'

# def to_latex(data):


def main():
    method_order = ['RANDOM', 'BAU', 'SAD', 'MAS', 'DEM', 'DS', 'MACE', 'MV', 'ORACLE']
    tasks = ['face', 'temporal']
    output_latex = '\\begin{tabular}{clll}\n\\toprule\n'
    output_latex += '\\textbf{Task} & \\textbf{Method} & \\textbf{Unsupervised}  & \\textbf{Supervised} \\\\'

    for task in tasks:
        df = pd.read_csv(f'results/supervision-experiments/results_{task}.csv')
        df = df[df['fold'] != 0]

        df_pv = df[['method', 'supervision_amt', 'acc']].pivot_table(columns='supervision_amt', 
            index='method', 
            values='acc', 
            aggfunc=plus_minus)


        df_pv.reset_index(inplace=True)
        df_pv['method']= pd.Categorical(df_pv['method'], method_order)
        df_pv.sort_values('method', inplace=True)
        df_pv['task'] = task
        df_pv.set_index(['task', 'method'], inplace=True)
        df_pv.rename_axis([None, None], inplace=True)
        df_pv.columns.name = None
        # print(df_pv)
        latex_raw = df_pv.to_latex(header=True, index=True, multirow=True)
        latex_elements = latex_raw.split('\n')
        latex_elements = latex_elements[3:len(latex_elements) - 3]
        latex = "\n".join(latex_elements)
        # print(latex)
        # latex = latex.split('toprule')[1].split('\\bottomrule')[0]
        # output_latex += '\n\\midrule'
        output_latex += '\n'
        output_latex += latex

    output_latex += '\n\\bottomrule\n\\end{tabular}\n'
    print(output_latex)
    with open("testlatex.tex", "w") as file:
        file.write(output_latex)





if __name__ == "__main__":
    main()


# df_grouped = df.groupby(['method', 'supervision_amt']).mean()[['acc', 'f1_weighted', 'f1_macro']]
# df_min_max = df[['method', 'supervision_amt', 'acc']]
# df_min_max['min'] = df['acc']
# df_min_max['max'] = df['acc']
# df_min_max = df_min_max.groupby(['method', 'supervision_amt']).agg({'acc':'mean', 'min':'min', 'max':'max'})
# print(df_min_max)
# print(conf_interval(df['acc']))
# print(plus_minus(df['acc']))