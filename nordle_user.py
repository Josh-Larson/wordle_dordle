from backend.filter import compile_rules, filter_words
from backend.engine import WordleEngine
from backend.heuristic import evaluate_guess
from backend.words import words_likely
from backend.user_input import get_invalid_guess_reason, get_invalid_hint_reason, is_valid_guess, is_valid_hint

from typing import List, Tuple
import sys


def get_inputs(n: int, hints: List[List[Tuple[str, str]]], game_running: List[bool]):
	guess = input("Guess:  ").lower()
	if not is_valid_guess(guess):
		print("Invalid guess. %s" % get_invalid_guess_reason(guess))
		return None
	
	hint_buffer = [("", "")] * n
	game_running_buffer = game_running.copy()
	for i in range(n):
		if game_running[i]:
			hint = input("Hint %d: " % (i+1)).lower()
			if not is_valid_hint(hint):
				print("Invalid hint %d. %s" % (i+1, get_invalid_hint_reason(hint)))
				return None
			hint_buffer[i] = (guess, hint)
			game_running_buffer[i] = game_running_buffer[i] and hint != "yyyyy"
	
	for i in range(n):
		hints[i].append(hint_buffer[i])
		game_running[i] = game_running_buffer[i]

	return guess


def get_solution_guesses(n: int, engine, hints: List[List[Tuple[str, str]]], game_running: List[bool]):
	guesses = [[] for _ in range(n)]
	for i in range(n):
		if game_running[i]:
			rules = compile_rules(hints[i])
			guesses[i] = [word for word in filter_words(rules)]
	
	best_guesses = [(guess, sum(evaluate_guess(guesses[i], engine, guess) for i in range(n) if game_running[i])) for guess in words_likely]
	best_guesses.sort(key=lambda g: g[1], reverse=True)
	for i in range(n):
		guesses[i] = [(guess, evaluate_guess(guesses[i], engine, guess)) for guess in guesses[i]]
		guesses[i].sort(key=lambda g: g[1], reverse=True)
	return best_guesses, guesses


def print_guesses(n: int, best_guesses: List[Tuple[str, float]], guesses: List[List[Tuple[str, float]]]):
	format_output = "    ".join(["%-12s"] * n)
	print("")
	if any([len(g) == 1 for g in guesses]):
		for g in guesses:
			if len(g) == 1:
				print("Suggested: %-5s" % (g[0][0]))
				break
	elif len(best_guesses) > 0 and sum(len(g) for g in guesses) > 2 and any(len(g) > 0 for g in guesses):
		print("Suggested: %-5s" % (best_guesses[0][0]))
	print("")
	
	print(format_output % tuple(["     % 2d     " % (i + 1) for i in range(n)]))
	print(format_output % tuple(["------------"] * n))
	for i in range(min(5, max(len(g) for g in guesses))):
		guess_format = []
		for g in guesses:
			if i < len(g):
				guess_format.append(g[i][0])
			else:
				guess_format.append("")
		
		print(format_output % tuple(guess_format))


def main():
	if len(sys.argv) < 2:
		print("Expected argument for number of wordles")
		exit(-1)
	
	try:
		n = int(sys.argv[1])
	except ValueError:
		n = 0
		print("Invalid argument for number of wordles: '%s'" % sys.argv[1])
		exit(-2)
	
	print("Suggested Opener: trace")
	print("Hints Legend:")
	print("    y - green")
	print("    h - yellow")
	print("    n - gray")
	print("")
	
	engine = WordleEngine("")
	hints = [[] for _ in range(n)]
	game_running = [True] * n
	
	while any(game_running):
		guess = get_inputs(n, hints, game_running)
		if guess is None:
			continue
		if not any(game_running):
			break
		best_guesses, guesses = get_solution_guesses(n, engine, hints, game_running)
		print_guesses(n, best_guesses, guesses)
		
		print("")
		print("")
		
		if all(len(g) <= 1 for g in guesses):
			break


if __name__ == '__main__':
	main()
