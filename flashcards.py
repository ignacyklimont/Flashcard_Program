# Importing argparse to take arguments from the command line
import argparse


# Defining main class
class FlashCards:
	def __init__(self):
		self.cards = {}
		self.mistakes = {}
		self.cards_added = 0
		self.question = 0
		self.log = []
		self.file_name_export = ''

	# Parser that takes arguments from CLI
	# For "import" calls function immediately, for "export" waits until user types "exit" in the main menu
	def parser_func(self):
		parser = argparse.ArgumentParser()
		parser.add_argument("--export_to")
		parser.add_argument("--import_from")
		args = parser.parse_args()
		if args.export_to:
			self.file_name_export = args.export_to
		if args.import_from:
			file_name_imp = args.import_from
			FlashCards.import_cards(self, file_name_imp)

	# Records and appends every output statement in the program (used instead of print to track interaction with program)
	def print(self, message = "", end = '\n'):
		self.log.append(message + end)
		print(message, end=end)

	# Records and appends every input statement in the program (used instead of input to track interaction with program)
	def input(self):
		term = input()
		self.log.append(term + '\n')
		return term

	# Main menu that allows user to choose different options for interacting with the program
	# Add cards, remove cards, import or export, ask to choose number of cards and start practicing
	# Log to save logs generated with input and output method, the hardest card option to see card with most wrong answers
	# Reset stats to erase statistics for wrong answers
	def prompt_main_actions(self):
		self.print('Input the action (add, remove, import, export, ask, exit, log, hardest card, reset stats):')
		action = self.input()
		# Going over different possible answers
		while action == '':
			FlashCards.prompt_main_actions(self)
		if action not in ['add', 'remove', 'import', 'export', 'ask', 'exit', 'log', 'hardest card', 'reset stats']:
			self.print(f'{action} is not an option')
			FlashCards.prompt_main_actions(self)
		elif action == 'add':
			FlashCards.add_cards(self)
		elif action == 'remove':
			FlashCards.remove_card(self)
		elif action == 'import':
			self.print('File name: \n')
			file_name_imp = self.input()
			FlashCards.import_cards(self, file_name_imp)
		elif action == 'export':
			self.print('File name: ')
			file_name_exp = self.input()
			FlashCards.export_cards(self, file_name_exp)
		elif action == 'ask':
			self.print("How many times to ask?")
			n = int(self.input())
			self.question = n
			FlashCards.practice_menu(self)
		elif action == 'log':
			FlashCards.log_cards(self)
		elif action == 'hardest card':
			FlashCards.hardest_card(self)
		elif action == 'reset stats':
			self.mistakes.clear()
			self.print('Card statistics have been reset.')
			FlashCards.prompt_main_actions(self)
		elif action == 'exit':
			print('Bye bye!')
			if self.file_name_export != '':
				FlashCards.export_cards(self, self.file_name_export)
			exit()
		else:
			FlashCards.prompt_main_actions(self)

	# Adds cards if the term and definition does not exist yet
	def add_cards(self):
		self.print(f'The card: ')
		term = self.input()
		while term in self.cards.keys():
			self.print(f'The card "{term}" already exists. Try again: ')
			term = self.input()
		self.print(f'The definition of  the card: ')
		definition = self.input()
		while definition in self.cards.values():
			self.print(f'The definition "{definition}" already exists. Try again: ')
			definition = self.input()
		if term not in self.cards.keys() and definition not in self.cards.values():
			self.cards[term] = definition
			self.print(f'The pair ("{term}":"{definition}") has been added.')
		FlashCards.prompt_main_actions(self)

	# Method to interactively practice the cards, number of questions depends on number passed to "ask" option
	def practice_menu(self):
		while self.question > 0:
			for key, value in self.cards.items():
				self.print(f'Print the definition of "{key}": ')
				answer = self.input()
				if answer == value:
					print('Correct!')
				elif answer != value and answer in self.cards.values():
					other_key = str({i for i in self.cards if self.cards[i] == answer})
					other_key = other_key.strip("{}").strip("''")
					self.print(
						f'Wrong. The right answer is "{value}", but your definition is correct for "{other_key}".')
					FlashCards.update_mistakes(self, key)
				else:
					self.print(f'Wrong. The right answer is "{value}".')
					FlashCards.update_mistakes(self, key)
				self.question -= 1
				if self.question == 0:
					FlashCards.prompt_main_actions(self)

	# Removes chosen card
	def remove_card(self):
		self.print('Which card? ')
		card_to_rem = self.input()
		if card_to_rem in self.cards.keys():
			del self.cards[card_to_rem]
			self.print('The card has been removed.')
		else:
			self.print(f'Can\'t remove "{card_to_rem}": there is no such card.')
		FlashCards.prompt_main_actions(self)

	# Imports cards from a file
	def import_cards(self, file_name):
		try:
			file_txt = open(file_name, 'r')
			for line in file_txt:
				line = line.strip().replace('\n', '')
				line_split = line.split(':')
				if line_split[0] in self.cards.keys():
					del self.cards[line_split[0]]
				self.cards[line_split[0]] = line_split[1]
				self.cards_added += 1
			self.print(f'{self.cards_added} cards have been loaded.\n')
			file_txt.close()
			self.cards_added = 0
			FlashCards.prompt_main_actions(self)
		except FileNotFoundError:
			self.print('File not found.')
			FlashCards.prompt_main_actions(self)

	# Exports cards to a file
	def export_cards(self, file_name):
		with open(f'{file_name}', 'a', newline='') as file:
			for key, value in self.cards.items():
				file.write('%s:%s\n' % (key, value))
		self.print(f'{len(self.cards)} cards have been saved.')
		if self.file_name_export != '':
			exit()
		else:
			FlashCards.prompt_main_actions(self)

	# Keeps tracks of mistakes for different cards
	def update_mistakes(self, term):
		if term in self.mistakes.keys():
			self.mistakes[term] += 1
		else:
			self.mistakes[term] = 1

	# Generates information about the hardest card
	def hardest_card(self):
		try:
			max_val = max(self.mistakes.values())
			h_card = [f'"{t}"' for t, v in self.mistakes.items() if v == max_val]
			h_card_str = ', '.join(x for x in h_card)
			if len(h_card) > 1:
				self.print('The hardest cards are', end='')
				self.print(h_card_str, end='')
				self.print(f'. You have {max_val} errors answering them.')
			else:
				self.print(f'The hardest card is {h_card_str}. You have {max_val} errors answering it.')
		except ValueError:
			self.print('There are no cards with errors.')
		FlashCards.prompt_main_actions(self)

	# Produces file with logs
	def log_cards(self):
		self.print('File name: \n')
		log_file = self.input()
		with open(f'{log_file}', 'w', newline='') as file_write:
			file_write.writelines(self.log)
		self.print('The log has been saved.', end='\n\n')
		FlashCards.prompt_main_actions(self)


# Initiates the game
if __name__ == '__main__':
	game = FlashCards()
	game.parser_func()
	game.prompt_main_actions()
