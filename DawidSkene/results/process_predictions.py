import csv
import pandas as pd
from sklearn import metrics
import numpy as np
import sys
import os
import argparse

parser = argparse.ArgumentParser(description='Evaluate MACE results')

'''positional (required) arguments'''
parser.add_argument('task', type=str, help='task/dataset name')
# parser.add_argument('eval_file', type=str, help='location of file with truths')

'''optional arguments'''
parser.add_argument('--semi-supervised', dest='supervision_amt', type=float,
                    help='amount of supervision. Does not affect how program runs and is just for logging', metavar='PCT_TRAINING_SET', default=0.0)
parser.add_argument('--fold', dest='fold', type=int, help='which fold? Does not affect how program runs and is just for logging', default=0)
parser.add_argument('--noise', dest='noise', type=str, help='noise level. Does not affect how program runs and is just for logging', default='original')


args = parser.parse_args()
task = args.task
# eval_file = args.eval_file
supervision_amt = args.supervision_amt
fold = args.fold
noise = args.noise

df = pd.read_csv('results/object-probabilities.txt', sep='\t').sort_values(['Object']).reset_index()
df = df[['Object', 'Correct_Category', 'DS_MaxLikelihood_Category', 'MV_MaxLikelihood_Category']]
df = df.dropna()

methods = ['DS', 'MV']
for method in methods:
	col_name = method + '_MaxLikelihood_Category'
	accuracy = metrics.accuracy_score(df['Correct_Category'], df[col_name])
	print(df[['Object', 'Correct_Category', col_name]])
	f1 = metrics.f1_score(df['Correct_Category'], df[col_name], average='weighted')

	score_col_name = 'score' + method
	df[score_col_name] = (df[col_name] == df['Correct_Category']).astype(int)

	print(method, accuracy, f1)

	conf_matrix = metrics.confusion_matrix(df['Correct_Category'], df[col_name])
	print(conf_matrix)


	filename = f'results/{method}/results_{task}.csv'
	with open (filename, 'a') as file:
		writer = csv.writer(file)
		if (os.stat(filename).st_size == 0):
			writer.writerow(['task','supervision_level','fold','noise_level','accuracy','f1'])
		writer.writerow([task, supervision_amt, fold, noise, accuracy, f1]) 
	print([task, supervision_amt, fold, noise, accuracy, f1]) 

