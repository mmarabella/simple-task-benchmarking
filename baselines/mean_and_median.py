import pandas as pd
import sys
from sklearn import metrics
import math
import csv
import numpy as np

# rmse = lambda x, y: math.sqrt(metrics.mean_squared_error(x, y))

task_name = sys.argv[1]

annotation_df = pd.read_csv('../data/clean/answer_' + task_name + '.csv')
gold_df_raw = pd.read_csv('../data/clean/truth_' + task_name + '.csv').set_index('question').sort_values(['question'])
full_df = annotation_df.join(gold_df_raw, how='inner', on='question')

mean_df = full_df[['question', 'answer']].groupby('question').agg('mean').sort_values(['question'])
median_df = full_df[['question', 'answer']].groupby('question').agg('median').sort_values(['question'])
gold_df = full_df[['question', 'truth']].set_index('question').groupby('question').first()

mean_df = mean_df.join(gold_df, on='question', how='inner')
mean_df['score'] = abs(mean_df['answer'] - mean_df['truth'])

median_df = median_df.join(gold_df, on='question', how='inner')
median_df['score'] = abs(median_df['answer'] - median_df['truth'])
print(mean_df)
print(median_df)

mean_mae = metrics.mean_absolute_error(mean_df['truth'], mean_df['answer'])
mean_mse = metrics.mean_squared_error(mean_df['truth'], mean_df['answer'])
median_mae = metrics.mean_absolute_error(median_df['truth'], median_df['answer'])
median_mse = metrics.mean_squared_error(median_df['truth'], median_df['answer'])

print(mean_mae)
print(np.mean(mean_df['score']))
print(mean_mse)
print(median_mae)
print(np.mean(median_df['score']))
print(median_mse)


with open ('results/MEAN/results_summary.csv', 'a') as file:
	writer = csv.writer(file)
	writer.writerow([task_name, mean_mae, mean_mse]) 

with open ('results/MEDIAN/results_summary.csv', 'a') as file:
	writer = csv.writer(file)
	writer.writerow([task_name, median_mae, median_mse]) 

with open('results/MEAN/mean_scores_' + task_name + '.csv', 'w') as file:
	writer = csv.writer(file)
	for idx, item in mean_df['score'].iteritems():
		writer.writerow([item])

with open('results/MEDIAN/median_scores_' + task_name + '.csv', 'w') as file:
	writer = csv.writer(file)
	for idx, item in median_df['score'].iteritems():
		writer.writerow([item])