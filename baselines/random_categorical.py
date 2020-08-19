import numpy as np
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
def random_user(s):
    return s.sample(1).values[0]

task_name = sys.argv[1]

annotation_df = pd.read_csv('../data/clean/answer_' + task_name + '.csv')
gold_df_raw = pd.read_csv('../data/clean/truth_' + task_name + '.csv').set_index('question').sort_values(['question'])
full_df = annotation_df.join(gold_df_raw, how='inner', on='question')

random_df = full_df[['question', 'answer']].groupby('question').agg(random_user).sort_values(['question'])
gold_df = full_df[['question', 'truth']].groupby('question').first()

random_df = random_df.join(gold_df, how='inner')
random_df['score'] = (random_df['answer'] == random_df['truth']).astype(int)

random_accuracy = metrics.accuracy_score(random_df['truth'], random_df['answer'])
if len(random_df['answer'].unique()) == 2:
	random_f1 = metrics.f1_score(random_df['truth'], random_df['answer'])
else:
	print('weighted')
	random_f1 = metrics.f1_score(random_df['truth'], random_df['answer'], average='weighted')

print(random_accuracy)
print(np.mean(random_df['score']))
print(random_f1)


with open ('results/RANDOM/results_summary.csv', 'a') as file:
	writer = csv.writer(file)
	writer.writerow([task_name, random_accuracy, random_f1]) 


with open('results/RANDOM/random_scores_' + task_name + '.csv', 'w') as file:
	writer = csv.writer(file)
	for idx, item in random_df['score'].iteritems():
		writer.writerow([item])
