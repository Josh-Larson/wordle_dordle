import re


guess_regex = re.compile("[a-zA-Z]{5}")
hint_regex = re.compile("[yhnYHN]{5}")


def get_invalid_guess_reason(guess):
	if len(guess) != 5:
		return "Expected 5 characters"
	if not guess_regex.match(guess):
		return "Invalid word"
	return None


def is_valid_guess(guess):
	return guess_regex.match(guess) is not None


def get_invalid_hint_reason(hint):
	if len(hint) != 5:
		return "Expected 5 characters"
	if not hint_regex.match(hint):
		return "Invalid hint (expected only characters: yhn)"
	return None


def is_valid_hint(hint):
	return hint_regex.match(hint) is not None
