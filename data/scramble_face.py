import pandas as pd
import random


def generate_mapping():
	orig = [0, 1, 2, 3]
	new = [0, 1, 2, 3]
	random.shuffle(new)
	for i in range(10):
		if new[0] != 1:
			random.shuffle(new)
	mapping = dict(zip(orig, new))
	return mapping

df_answer = pd.read_csv('data/same-index-separate/answer_dog.csv')
df_truth = pd.read_csv('data/same-index-separate/truth_dog.csv')

# print(df_answer.join(df_truth.set_index('question'), on='question', how='inner'))
print(df_answer['answer'].value_counts())
print(df_truth['truth'].value_counts())

for idx, row in df_truth.iterrows():
	question = row['question']
	truth = row['truth']
	mapping = generate_mapping()

	#change answers
	answers = df_answer[df_answer['question'] == question]
	idxs = answers.index
	answers_new = answers['answer'].map(lambda x: mapping[x])
	df_answer['answer'].loc[idxs] = answers_new
	#change truth
	df_truth['truth'].loc[idx] = mapping[truth]


print(df_answer.join(df_truth.set_index('question'), on='question', how='inner'))
df_answer.to_csv('answer_dog_scrambled.csv', index=False)
df_truth.to_csv('truth_dog_scrambled.csv', index=False)

print(df_answer['answer'].value_counts())
print(df_truth['truth'].value_counts())
