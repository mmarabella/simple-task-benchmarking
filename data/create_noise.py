import random
import numpy as np
from scipy.stats import norm
import pandas as pd
from sklearn.metrics import accuracy_score
import argparse
from dataset_diagnostics import read_df, get_worker_quality_distr


def generate_dist_csv(df_new, task, noise_level, directory, new_sigma=None):
	if new_sigma:
		df_new.to_csv(f'{directory}/DIST/answer_{task}_noise{noise_level}_var{new_sigma}.csv', index=False)
	else:
		df_new.to_csv(f'{directory}/DIST/answer_{task}_noise{noise_level}.csv', index=False)

def generate_ds_csv(df_new, task, noise_level, directory, new_sigma=None):
	df_ds = df_new[['worker', 'question', 'answer']]
	if new_sigma:
		df_ds.to_csv(f'{directory}/DS/answer_{task}_noise{noise_level}_var{new_sigma}.csv', index=False, sep='\t', header=None)
	else:
		df_ds.to_csv(f'{directory}/DS/answer_{task}_noise{noise_level}.csv', index=False, sep='\t', header=None)

def generate_mace_csv(df_new, df_truth, task, noise_level, directory, new_sigma=None):
	df_mace = df_new.pivot_table(columns='worker', index='question', values='answer').sort_index()
	df_mace = df_mace.applymap(lambda x: '' if pd.isnull(x) else str(int(x)))
	if new_sigma:
		df_mace.to_csv(f'{directory}/MACE/answer_{task}_noise{noise_level}_var{new_sigma}.csv', header=False, index=False)
	else:
		df_mace.to_csv(f'{directory}/MACE/answer_{task}_noise{noise_level}.csv', header=False, index=False)

	mace_idx = df_mace.index
	df_truth_mace = pd.DataFrame(index=mace_idx)
	df_truth_mace = df_truth_mace.join(df_truth, how='inner').sort_index()
	df_truth_mace = df_truth_mace.reset_index()[['truth']]
	df_truth_mace.index.rename('question', inplace=True)
	if new_sigma:
		df_truth_mace.to_csv(f'{directory}/MACE/truth_{task}_noise{noise_level}_var{new_sigma}.csv')
	else:
		df_truth_mace.to_csv(f'{directory}/MACE/truth_{task}_noise{noise_level}.csv')

def create_noisey_df(df_full, mu, sigma):
	possible_answers = list(df_full['answer'].unique())
	new_answers = {}
	for worker in df_full['worker'].unique():
		worker_answers = {}
		df_worker = df_full[df_full['worker'] == worker]
		accuracy = np.random.normal(mu, sigma)
		df_worker = df_worker.sample(frac=1).reset_index(drop=True)
		partition = round(accuracy * len(df_worker))
		df_right = df_worker[:partition]
		df_wrong = df_worker[partition:]

		for idx, row in df_right.iterrows():
			truth_val = row['truth']
			question = row['question']
			worker_answers[question] = truth_val
		for idx, row in df_wrong.iterrows():
			truth_val = row['truth']
			question = row['question']
			remaining_answers = possible_answers[:]
			remaining_answers.pop(remaining_answers.index(truth_val))
			worker_answers[question] = random.choice(remaining_answers)
				
		new_answers[worker] = worker_answers

	df = pd.DataFrame(new_answers)
	df = df.stack().to_frame()
	df = df.reset_index()
	df.columns = ['question', 'worker', 'answer']
	df['answer'] = df['answer'].astype(int)
	return(df)


def main():
	parser = argparse.ArgumentParser(description='Generate noisey datasets')

	parser.add_argument('output_dir', type=str, help='folder for output files')
	parser.add_argument('--sigma', dest='sigma', type=float, help='set worker acc variance')

	args = parser.parse_args()
	output_dir = args.output_dir
	new_sigma = args.sigma


	# tasks = ['temporal', 'waterbird', 'movie', 'face', 'dog', 'adult_ordinal', 'weather_ordinal']
	tasks = ['face']
	noise = [0.55, 0.65, 0.75, 0.85]

	for task in tasks:
		print(task)
		df_full, df_answer, df_truth = read_df(task)
		labels_per_item = len(df_full) / df_full['question'].nunique() 
		for noise_level in noise:
			if new_sigma:
				sigma = new_sigma
			else:
				_, sigma = get_worker_quality_distr(df_full)


			mu2 = 0
			sigma2 = 0
			attempts = 0
			while abs(mu2 - noise_level) > .02 or abs(sigma2 - sigma) > .02:
				print("attempt:", attempts)
				df_new = create_noisey_df(df_full, noise_level, sigma)
				mu2, sigma2 = get_worker_quality_distr(df_new.join(df_truth, on='question', how='inner'))
				if attempts > 5:
					print(mu2, sigma2)
				attempts += 1

			print("MEAN:", noise_level, "->", mu2)
			print("VAR: ", sigma, "->", sigma2)


			generate_dist_csv(df_new, task, noise_level, output_dir, new_sigma)
			generate_ds_csv(df_new, task, noise_level, output_dir, new_sigma)
			generate_mace_csv(df_new, df_truth, task, noise_level, output_dir, new_sigma)


if __name__ == "__main__":
	main()