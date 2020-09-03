import pandas as pd
import numpy as np
from scipy.stats import norm
import pandas as pd
from sklearn.metrics import accuracy_score

def read_df(task):
	df_answer = pd.read_csv(f'clean/answer_{task}.csv')
	df_truth = pd.read_csv(f'clean/truth_{task}.csv').set_index('question')
	df_full = df_answer.join(df_truth, how='inner', on='question')
	return df_full, df_answer, df_truth

def get_labels_per_worker(df_full):
	nlabels = len(df_full)
	nworkers = df_full['worker'].nunique()
	return int(round(nlabels/nworkers, 0))

def get_labels_per_question(df_full):
	nlabels = len(df_full)
	nquestions = df_full['question'].nunique()
	return int(round(nlabels/nquestions, 0))

def get_worker_quality_distr(df_full):
	accs = []
	for worker in df_full['worker'].unique():
		rows = df_full[df_full['worker'] == worker]
		acc = accuracy_score(rows['truth'], rows['answer'])
		accs.append(acc)

	mu, sigma = norm.fit(accs)
	return mu, sigma

def get_totals(df_full):
	totals = {}
	totals['workers'] = df_full['worker'].nunique()
	totals['questions'] = df_full['question'].nunique()
	totals['labels'] = len(df_full)
	return totals

def get_truth_variance(df_truth):
	counts = df_truth['truth'].value_counts().values
	pcts = counts/np.sum(counts)*100
	var = np.var(pcts)
	return var

def get_error_variance(df_full):
	df = df_full.copy()
	df['score'] = abs(df['answer'] - df['truth'])
	only_misses = df[df['score'] != 0]
	counts = only_misses['score'].value_counts().values
	pcts = counts/np.sum(counts)*100
	var = np.var(pcts)
	return var


def main():
	tasks = ['face', 'adult_ordinal', 'waterbird', 'dog', 'weather_ordinal', 'movie', 'temporal']
	results_dict = {}
	for task in tasks:
		task_dict = {}

		df_full, df_answer, df_truth = read_df(task)
		worker_acc_mean, worker_acc_var = get_worker_quality_distr(df_full)
		l_per_q = get_labels_per_question(df_full)
		l_per_w = get_labels_per_worker(df_full)
		truth_var = get_truth_variance(df_truth)
		error_var = get_error_variance(df_full)
		totals = get_totals(df_full)


		task_dict['worker_acc_mean'] = worker_acc_mean
		task_dict['worker_acc_var'] = worker_acc_var
		task_dict['l_per_q'] = l_per_q
		task_dict['l_per_w'] = l_per_w
		task_dict['truth_var'] = truth_var
		task_dict['error_var'] = error_var
		task_dict['total_workers'] = totals['workers']
		task_dict['total_questions'] = totals['questions']
		task_dict['total_labels'] = totals['labels']

		results_dict[task] = task_dict

	results_df = pd.DataFrame.from_dict(results_dict, orient='index')
	# results_df.to_csv('dataset_diagnostics.csv')
	print(results_df)

if __name__ == "__main__":
	main()
