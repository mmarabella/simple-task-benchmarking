import pandas as pd
import numpy as np

tasks = ['temporal', 'movie', 'waterbird', 'face', 'dog', 'weather_ordinal', 'adult_ordinal']
# tasks = ['temporal']
for task in tasks:
	df_answer = pd.read_csv(f'same-index-separate/answer_{task}.csv')
	df_truth = pd.read_csv(f'same-index-separate/truth_{task}.csv').sort_values('question').reset_index()[['question', 'truth']]

	df_answer = df_answer.pivot_table(columns='worker', index='question', values='answer').sort_index()
	df_answer = df_answer.applymap(lambda x: '' if pd.isnull(x) else str(int(x)))
	df_answer.to_csv(f'MACE/answer_{task}.csv', header=False, index=False)

	df_truth = df_truth[['truth']]
	df_truth.index.rename('question', inplace=True)
	df_truth.to_csv(f'MACE/truth_{task}.csv')

