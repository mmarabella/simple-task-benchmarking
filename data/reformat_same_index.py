import pandas as pd
import csv as csv

task_name = input("task name: ")
separate = input("separate files (y/n)? ")

if separate == 'y':
	annotation_df = pd.read_csv(task_name + '-data-raw/answer.csv')
	gold_df = pd.read_csv(task_name + '-data-raw/truth.csv')

elif separate == 'n':
	full_df = pd.read_csv(task_name + '-data-raw/' + task_name + '.csv')
	annotation_df = full_df[['question', 'worker', 'answer']]
	gold_df = full_df[['question', 'truth']].groupby('question').first().reset_index()
	print(gold_df)


with open('same-index-separate/answer_' + task_name + '.csv', 'w') as answerfile:     
	writer = csv.writer(answerfile)
	writer.writerow(['question', 'worker', 'answer'])
	for index, data in annotation_df.iterrows():
		row = []
		question = data['question']
		worker = data['worker']
		answer = data['answer']
		row += [question, worker, answer]
		writer.writerow(row)

with open('same-index-separate/truth_' + task_name + '.csv', 'w') as truthfile:
	writer = csv.writer(truthfile)
	writer.writerow(['question','truth'])
	for index, data in gold_df.iterrows():
		row = []
		question = data['question']
		truth = data['truth']
		row += [question, truth]
		writer.writerow(row)
