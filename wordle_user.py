from backend.filter import compile_rules, filter_words
from backend.heuristic import evaluate_guess
from backend.engine import WordleEngine
from backend.words import words_likely
from backend.user_input import get_invalid_guess_reason, get_invalid_hint_reason, is_valid_guess, is_valid_hint


if __name__ == '__main__':
	engine = WordleEngine("")
	hints = []
	print("Suggested Opener: trace")
	print("Hints Legend:")
	print("    y - green")
	print("    h - yellow")
	print("    n - gray")
	print("")
	
	while True:
		guess = input("Guess: ").lower()
		if not is_valid_guess(guess):
			print("Invalid guess. %s" % get_invalid_guess_reason(guess))
			continue
		hint = input("Hint:  ").lower()
		if not is_valid_hint(hint):
			print("Invalid hint. %s" % get_invalid_hint_reason(hint))
			continue
		if hint == "yyyyy":
			break
		hints.append((guess, hint))
		rules = compile_rules(hints)
		possible_words = [word for word in filter_words(rules)]
		
		print("")
		if len(possible_words) == 1:
			print("Answer: %s" % possible_words[0])
			break
		elif len(possible_words) <= 10:
			scored_words = [(word, evaluate_guess(possible_words, engine, word)) for word in possible_words]
			print("Possibilities")
			print("-------------")
			for word in scored_words[:5]:
				print("%s" % word[0])
			if len(scored_words) == 0:
				break
		else:
			best_reduction_word = max(words_likely, key=lambda word: evaluate_guess(possible_words, engine, word))
			print("Suggested Word: %s" % best_reduction_word)
		print("")
