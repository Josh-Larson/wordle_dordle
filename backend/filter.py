from .words import words_likely
import re


def compile_rules(hints):
	letters_exist = set()
	letters_not_exist = set()
	for rule_word, rule_output in hints:
		for i, out in enumerate(rule_output):
			if out == "y" or out == "h":
				letters_exist.add(rule_word[i])
			elif out == "n":
				letters_not_exist.add(rule_word[i])
	
	regex = ""
	for i in range(5):
		exact_match = False
		range_splits = []
		for rule_word, rule_output in hints:
			l, o = ord(rule_word[i]), rule_output[i]
			if o == "y":
				regex += rule_word[i]
				exact_match = True
				break
			elif len(range_splits) == 0 or range_splits[-1] != l:
				range_splits.append(l)
		if not exact_match:
			range_splits.sort()
			prev_split = ord("a")
			regex += "["
			for range_index, range_split in enumerate(range_splits):
				if prev_split < range_split:
					if prev_split + 1 == range_split:
						regex += chr(prev_split)
					else:
						regex += chr(prev_split) + "-" + chr(range_split - 1)
				prev_split = range_split + 1
			if prev_split <= ord("z"):
				regex += chr(prev_split) + "-z"
			regex += "]"
	
	for not_exists in letters_not_exist.copy():
		if not_exists in letters_exist:
			letters_not_exist.remove(not_exists)
	
	return letters_exist, letters_not_exist, re.compile(regex)


def filter_words(filters):
	for word in words_likely:
		match = True
		for not_exists in filters[1]:
			if not_exists in word:
				match = False
				break
		if not match:
			continue
		for exists in filters[0]:
			if exists not in word:
				match = False
				break
		if not match:
			continue
		if not filters[2].match(word):
			continue
		yield word
