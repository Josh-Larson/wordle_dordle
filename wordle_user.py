from backend.filter import compile_rules, filter_words
from backend.heuristic import evaluate_guess
from backend.engine import WordleEngine
from backend.words import words_likely


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
		hint = input("Hint:  ").lower()
		if len(guess) != 5:
			print("Invalid guess. Expected 5 characters")
			continue
		if len(hint) != 5:
			print("Invalid hint. Expected 5 characters")
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
			for word in scored_words[:5]:
				print("%s  [%.2f]" % word)
			if len(scored_words) == 0:
				break
		else:
			best_reduction_word = max(words_likely, key=lambda word: evaluate_guess(possible_words, engine, word))
			print("Suggested Word: %s" % best_reduction_word)
		print("")
