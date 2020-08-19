import pandas as pd
import sys
from sklearn import metrics
import math
import csv
import random

# return mode, randomly break ties
def mode_ties(s):
	m = s.mode()
	if len(m) > 1:
		random.shuffle(m)
		return(m[0])
	return m

task_name = sys.argv[1]
metric = sys.argv[2]

annotation_df = pd.read_csv('../data/clean/answer_' + task_name + '.csv')
gold_df_raw = pd.read_csv('../data/clean/truth_' + task_name + '.csv').set_index('question').sort_values(['question'])
full_df = annotation_df.join(gold_df_raw, how='inner', on='question')
if metric == 'mae':
	full_df['err'] = abs(full_df['answer'] - full_df['truth'])
	filename = 'average_worker_mae.csv'
elif metric == 'mse':
	full_df['err'] = (full_df['answer'] - full_df['truth']).pow(2)
	filename = 'average_worker_mse.csv'

worker_mse = full_df[['worker', 'err']].groupby('worker').agg(lambda x: x.sum()/len(x))
average_mse = worker_mse['err'].sum()/len(worker_mse['err'])

print(worker_mse)
print(average_mse)

with open(filename, 'a') as file:
	writer = csv.writer(file)
	# writer.writerow(['task', 'average mse'])
	writer.writerow([task_name, average_mse])