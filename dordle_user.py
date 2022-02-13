from backend.filter import compile_rules, filter_words
from backend.engine import WordleEngine
from backend.heuristic import evaluate_guess
from backend.words import words_likely
from backend.user_input import get_invalid_guess_reason, get_invalid_hint_reason, is_valid_guess, is_valid_hint


if __name__ == '__main__':
	print("Suggested Opener: trace")
	print("Hints Legend:")
	print("    y - green")
	print("    h - yellow")
	print("    n - gray")
	print("")
	
	engine = WordleEngine("")
	hints1 = []
	hints2 = []
	game_running = True, True
	hint1, hint2 = "", ""
	
	while game_running[0] or game_running[1]:
		guess = input("Guess: ").lower()
		if not is_valid_guess(guess):
			print("Invalid guess. %s" % get_invalid_guess_reason(guess))
			continue
		if game_running[0]:
			hint1 = input("Hint Left:  ").lower()
			if not is_valid_hint(hint1):
				print("Invalid left hint. %s" % get_invalid_hint_reason(hint1))
				continue
			hints1.append((guess, hint1))
		if game_running[1]:
			hint2 = input("Hint Right: ").lower()
			if not is_valid_hint(hint2):
				print("Invalid right hint. %s" % get_invalid_hint_reason(hint2))
				continue
			hints2.append((guess, hint2))
		game_running = (game_running[0] and hint1 != "yyyyy"),\
					   (game_running[1] and hint2 != "yyyyy")
		
		guesses_left = []
		guesses_right = []
		if game_running[0]:
			rules1 = compile_rules(hints1)
			guesses_left = [word for word in filter_words(rules1)]
		if game_running[1]:
			rules2 = compile_rules(hints2)
			guesses_right = [word for word in filter_words(rules2)]
		
		guesses_best = [(guess, evaluate_guess(guesses_left, engine, guess) + evaluate_guess(guesses_right, engine, guess)) for guess in words_likely]
		guesses_left = [(guess, evaluate_guess(guesses_left, engine, guess)) for guess in guesses_left]
		guesses_right = [(guess, evaluate_guess(guesses_right, engine, guess)) for guess in guesses_right]
		guesses_left.sort(key=lambda g: g[1], reverse=True)
		guesses_right.sort(key=lambda g: g[1], reverse=True)
		guesses_best.sort(key=lambda g: g[1], reverse=True)
		
		print("")
		if len(guesses_left) == 1:
			print("Suggested: %-5s [%.2f]" % (guesses_left[0]))
		elif len(guesses_right) == 1:
			print("Suggested: %-5s [%.2f]" % (guesses_right[0]))
		elif len(guesses_best) > 0 and (len(guesses_left) + len(guesses_right)) > 2 and (len(guesses_left) > 0 or len(guesses_right) > 0):
			print("Suggested: %-5s [%.2f]" % (guesses_best[0]))
		print("")
		
		print("%-12s    %-12s" % ("    Left    ", "   Right    "))
		print("%-12s    %-12s" % ("------------", "------------"))
		for i in range(min(5, max(len(guesses_left), len(guesses_right)))):
			guess_left, guess_right = "", ""
			if i < len(guesses_left):
				guess_left = "%-5s [%.2f]" % guesses_left[i]
			if i < len(guesses_right):
				guess_right = "%-5s [%.2f]" % guesses_right[i]
			
			print("%-12s    %-12s" % (guess_left, guess_right))
		
		print("")
		print("")
		
		if len(guesses_left) <= 1 and len(guesses_right) <= 1:
			break
