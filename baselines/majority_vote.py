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

task_name = sys.argv[1]
task_type = sys.argv[2]

annotation_df = pd.read_csv('../data/clean/answer_' + task_name + '.csv')
gold_df_raw = pd.read_csv('../data/clean/truth_' + task_name + '.csv').set_index('question').sort_values(['question'])

# annotation_df = pd.read_csv('../hate-speech/answer.csv')
# gold_df_raw = pd.read_csv('../hate-speech/truth.csv').set_index('question').sort_values(['question'])

full_df = annotation_df.join(gold_df_raw, how='inner', on='question')

mv_df = full_df[['question', 'answer']].groupby('question').agg(mode_ties).sort_values(['question'])
gold_df = full_df[['question', 'truth']].groupby('question').first()

mv_df = mv_df.join(gold_df, how='inner')


if task_type == 'categorical':
	mv_df['score'] = (mv_df['answer'] == mv_df['truth']).astype(int)

	mv_accuracy = metrics.accuracy_score(mv_df['truth'], mv_df['answer'])
	if len(mv_df['answer'].unique()) == 2:
		mv_f1 = metrics.f1_score(mv_df['truth'], mv_df['answer'])
	else:
		print('weighted')
		# mv_f1 = metrics.f1_score(mv_df['truth'], mv_df['answer'], average='weighted')
		# mapping = {'neither': 1, 'sexism': 2, 'racism': 3, 'both': 4, 'link': 5, \
		# 	1: 'neither', 2: 'sexism', 3: 'racism', 4: 'both', 5: 'link'}
		mv_df['truth'] = mv_df['truth'].map(lambda x: mapping[x])
		mv_df['answer'] = mv_df['answer'].map(lambda x: mapping[x])
		mv_f1 = metrics.f1_score(mv_df['truth'], mv_df['answer'], average=None)
		conf_matrix = metrics.confusion_matrix(mv_df['truth'], mv_df['answer'])
		report = metrics.classification_report(mv_df['truth'], mv_df['answer'], output_dict = True)
		print(conf_matrix)

	print(mv_accuracy)
	print(np.mean(mv_df['score']))
	print(mv_f1)
	print(report['1'])
	print(report['accuracy'])

	# with open ('../hate-speech/results2.csv', 'a') as file:
		writer = csv.writer(file)
		header = [
			'method', 
			'accuracy', 
			'macro f1', 
			'weighted f1', 
			'neither f1', 
			'sexism f1', 
			'racism f1', 
			'both f1', 
			'link f1'
		]
		row = [
			'MV', 
			report['accuracy'],
			report['macro avg']['f1-score'],
			report['weighted avg']['f1-score'],
			report[str(mapping['neither'])]['f1-score'],
			report[str(mapping['sexism'])]['f1-score'],
			report[str(mapping['racism'])]['f1-score'],
			report[str(mapping['both'])]['f1-score'],
			report[str(mapping['link'])]['f1-score']
		]
		writer.writerow(header)
		writer.writerow(row)

	# with open ('../hate-speech/conf_matrices.csv', 'a') as file:
		writer = csv.writer(file)
		writer.writerow(['MV'])
		writer.writerow(['', 'neither', 'sexism', 'racism', 'both', 'link'])
		counter = 1
		for row in conf_matrix:
			writer.writerow([mapping[counter]] + list(row))
			counter += 1

elif task_type == 'ordinal':
	mv_df['score'] = abs(mv_df['answer'] - mv_df['truth'])
	mae = metrics.mean_absolute_error(mv_df['truth'], mv_df['answer'])
	mse = metrics.mean_squared_error(mv_df['truth'], mv_df['answer'])
	print(mae)
	print(np.mean(mv_df['score']))
	print(mse)
	with open('results/MV/results_ordinal.csv', 'a') as file:
		writer = csv.writer(file)
		writer.writerow([task_name, mae, mse])

# with open('results/MV/mv_scores_' + task_name + '.csv', 'w') as file:
# 	writer = csv.writer(file)
# 	for idx, item in mv_df['score'].iteritems():
# 		writer.writerow([item])
