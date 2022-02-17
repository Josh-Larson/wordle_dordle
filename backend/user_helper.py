def print_results(application, hints):
	max_hints = max(len(hint) for hint in hints)
	guesses = [[g[0].upper() for g in hint] for hint in hints if len(hint) == max_hints][0]
	print("%s Bot: %s" % (application, " ".join([str(len(hint)) for hint in hints])))
	print("")
	columns = 1 if len(hints) == 1 else (2 if len(hints) <= 6 else 3)
	for hint_index in range(0, len(hints), columns):
		for hint_row in range(max_hints):
			for col in range(columns):
				if hint_index + col < len(hints) and hint_row < len(hints[hint_index+col]):
					hint = hints[hint_index+col][hint_row]
					print(hint[1].replace("y", "\U0001F7E9").replace("h", "\U0001F7E8").replace("n", "\u2B1B"), end="")
				else:
					print("%s" % ("\u2B1B" * 5), end="")
				if col + 1 == columns:
					print(" ||%s||" % guesses[hint_row])
				else:
					print("    ", end="")
		print("")
