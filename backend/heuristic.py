

def evaluate_guess(possible_words, engine, guess):
	resulting_hints = set()
	for possible in possible_words:
		resulting_hints.add(engine.get_hint(guess, possible))
	
	return len(resulting_hints) / 243
