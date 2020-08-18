import csv
import pandas as pd
from sklearn import metrics
import sys
import numpy as np
import os
import argparse

parser = argparse.ArgumentParser(description='Evaluate MACE results')

'''positional (required) arguments'''
parser.add_argument('task', type=str, help='task/dataset name')
parser.add_argument('task_type', type=str, help='task type (e.g. categorical, ordinal, numerical...)')
parser.add_argument('predictions_file', type=str, help='location of file with answer/labels')
parser.add_argument('eval_file', type=str, help='location of file with truths')

'''optional arguments'''
parser.add_argument('--log-results', dest='log_dir', type=str,
                    help='write results to user-specified directory', metavar='RESULTS_DIR', default='results')
parser.add_argument('--semi-supervised', dest='supervision_amt', type=float,
                    help='run task as semi-supervised', metavar='PCT_TRAINING_SET', default=0.0)
parser.add_argument('--fold', dest='fold', type=int, help='which fold?', default=0)
parser.add_argument('--noise', dest='noise', type=str, help='noise level', default='original')


args = parser.parse_args()
task = args.task
task_type = args.task_type
predictions_file = args.predictions_file
eval_file = args.eval_file

log_dir = args.log_dir.strip('/')
supervision_amt = args.supervision_amt
fold = args.fold
noise = args.noise


preds_df = pd.read_csv(predictions_file, header=None, names=['answer'])
preds_df.index.rename('question')
eval_df = pd.read_csv(eval_file).set_index('question')
full_df = preds_df.join(eval_df, how='inner')

if task_type == 'categorical':
	full_df['score'] = (full_df['truth'] == full_df['answer']).astype(int)
	accuracy = metrics.accuracy_score(full_df['truth'], full_df['answer'])
	f1 = metrics.f1_score(full_df['truth'], full_df['answer'], average='weighted')
	assert(accuracy == np.mean(full_df['score']))

	filename = f'{log_dir}/results_{task}.csv'
	with open(filename, 'a') as outfile:
		writer = csv.writer(outfile)
		if (os.stat(filename).st_size == 0):
			header = ['task','task_type','supervision_level','fold','noise_level','accuracy','f1']
			writer.writerow(header)
		writer.writerow([task, task_type, supervision_amt, fold, noise, accuracy, f1])
	print(accuracy)


elif task_type == 'ordinal':
	full_df['score'] = abs(full_df['truth'] - full_df['answer'])
	mae = metrics.mean_absolute_error(full_df['truth'], full_df['answer'])
	mse = metrics.mean_squared_error(full_df['truth'], full_df['answer'])
	assert(mae == np.mean(full_df['score']))

	filename = f'{log_dir}/results_{task}.csv'
	with open(filename, 'a') as outfile:
		writer = csv.writer(outfile)
		if (os.stat(filename).st_size == 0):
			header = ['task','task_type','supervision_level','fold','noise_level','mae','mse']
			writer.writerow(header)
		writer.writerow([task, task_type, supervision_amt, fold, noise, mae, mse])
	print(mae)

else:
	print("invalid task type")