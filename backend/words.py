import random


with open("resources/words_likely.txt", "r") as file:
	words_likely = [word.strip() for word in file.readlines() if len(word.strip()) == 5]

with open("resources/words_all.txt", "r") as file:
	words = [word.strip() for word in file.readlines() if len(word.strip()) == 5]

random.shuffle(words_likely)
random.shuffle(words)
