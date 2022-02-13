from .words import words_likely
import random


class WordleEngine:
	def __init__(self, word):
		self.word = word
		self.win = False
	
	def get_hint(self, guess, evaluation_word=None):
		if self.word == guess and evaluation_word is None:
			self.win = True
			return "yyyyy"
		
		evaluation_word = evaluation_word or self.word
		
		correct = set()
		hint = ""
		for i in range(5):
			if evaluation_word[i] == guess[i]:
				correct.add(evaluation_word[i])
		for i in range(5):
			if evaluation_word[i] == guess[i]:
				hint += "y"
			elif (guess[i] in correct) or guess[i] not in evaluation_word:
				hint += "n"
			else:
				hint += "h"
		return hint
	
	def is_win(self):
		return self.win


class WordleEngineRandom(WordleEngine):
	def __init__(self):
		super().__init__(random.choice(words_likely))


class DordleEngineRandom:
	def __init__(self):
		self.word1 = WordleEngineRandom()
		self.word2 = WordleEngineRandom()
	
	def get_hint(self, guess):
		return "     " if self.word1.is_win() else self.word1.get_hint(guess),\
			   "     " if self.word2.is_win() else self.word2.get_hint(guess)
	
	def is_win(self):
		return self.word1.is_win(), self.word2.is_win()
