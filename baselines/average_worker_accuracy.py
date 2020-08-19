import pandas as pd
import sys
from sklearn import metrics
import math
import csv
import random

# return mode, randomly break ties

task_name = sys.argv[1]

annotation_df = pd.read_csv('../data/clean/answer_' + task_name + '.csv')
gold_df_raw = pd.read_csv('../data/clean/truth_' + task_name + '.csv').set_index('question').sort_values(['question'])
full_df = annotation_df.join(gold_df_raw, how='inner', on='question')
full_df['correct'] = full_df['answer'] == full_df['truth']

worker_accuracy = full_df[['worker', 'correct']].groupby('worker').agg(lambda x: x.sum()/len(x))


print(worker_accuracy)
# average_accuracy = worker_accuracy['correct'].sum()/len(worker_accuracy['correct'])

# with open('average_worker_mv.csv', 'a') as file:
# 	writer = csv.writer(file)
# 	# writer.writerow(['task', 'average accuracy'])
# 	writer.writerow([task_name, average_accuracy])