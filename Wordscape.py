import random
from english_words import get_english_words_set
from nltk.corpus import words

def find_random_word(dictionary, minimum, maximum):
	word = ""
	copy = dictionary
	#Find random word with length greater than minimum and less than maximum
	while not (len(word) >= minimum and len(word) <= maximum): 
		word = copy.pop(random.randint(0, len(copy)-1))
	return word

def find_words(dictionary, letters):
	#Add initial word
	words = [letters]
	#For every word in dictionary with length greater than one
	for word in dictionary:
		if len(word) > 1:
			#Assume word can be made up from the letters of the letters given
			add = True
			temp = letters
			#Reject word if it contains letters other than the letters given
			for letter in word:
				if add and temp.count(letter) > 0:
					temp = temp.replace(letter, "", 1)
				else:
					add = False
			#Check for duplicates
			if add and words.count(word) == 0:
				words.append(word)
	return words

def create_table(words):
	size = int((len(words[0])+2)*2)
	table = [[' ' for i in range(size)] for j in range(size)]
	#Attempt to insert each word and store
	words_on_table = []
	for word in words:
		word_on_table = insert_word(table, word)
		if word_on_table != None:
			words_on_table.append(word_on_table)
	return table, words_on_table

def insert_word(table, word):
	center = (int(len(table)/2), int(len(table[0])/2))
	position = center
	most_centered = position
	horizontal = True
	direction = horizontal
	possible = True
	if table[position[0]][position[1]] != ' ': #This indicates the first word
		#Assume placement is not possible
		possible = False
		most_centered = (-10000, 10000)
		#Check every element in table
		for i in range(len(table)):
			for j in range(len(table[i])):
				if table[i][j] != ' ': #Ignore blanks
					for char in word: #Compare every non-blank character to every character in the word
						if table[i][j] == char: #Match found
							#Record index of match in word
							match_at = word.find(char) 
							#Check bounds of table
							if (i<len(table)-1 and i>0) and (j<len(table[i])-1 and j>0):
								#Check if characters above and below the match are blanks, if so a vertical word is possible
								if (table[i+1][j] == ' ') and (table[i-1][j] == ' '):
									start_point = i-match_at
									end_point = start_point+len(word)-1
									#Check bounds of table
									if (start_point-1 > 0) and (end_point+1 < len(table)-1):
										#Check that the first character before and after the word are blanks
										if (table[start_point-1][j] == ' ') and (table[end_point+1][j] == ' '):
											#Determine the start position
											position = (start_point,j)
											#Set direction
											horizontal = False
											#All requirements met, assume placement is possible
											possible = True
											#If at any point one of the characters left or right to a character in the word are not blanks,
											#and the current characters do not match, indicate a rule break (placement not possible)
											for x in range(start_point, end_point+1):
												if possible and (table[x][j+1] != ' ' or table[x][j-1] != ' ') and (table[x][j] != word[x-start_point]):
													possible = False
								#Check if characters left and right of the match are blanks, if so a horizontal word is possible
								elif (table[i][j+1] == ' ' and table[i][j-1] == ' '):
									#Check bounds of table
									start_point = j-match_at
									end_point = start_point+len(word)-1
									if (start_point-1 > 0) and (end_point+1 < len(table[i])-1):
										#Check that the first character before and after the word are blanks
										if (table[i][start_point-1] == ' ') and (table[i][end_point+1] == ' '):
											#Determine the start position
											position = (i,start_point)
											#Set direction
											horizontal = True
											#All requirements met, assume placement is possible
											possible = True
											#If at any point one of the characters above or below a character in the word are not blanks, 
											#and the current characters do not match, indicate a rule break (placement not possible)
											for y in range(start_point, end_point+1):
												if possible and (table[i+1][y] != ' ' or table[i-1][y] != ' ') and (table[i][y] != word[y-start_point]):
													possible = False
						#Keep track of the most centered possible placement of the word
						if possible:
							temp = abs(center[0]-position[0]) + abs(center[1]-position[1])
							minimum = abs(center[0]-most_centered[0]) + abs(center[1]-most_centered[1])
							if temp < minimum:
								most_centered = position
								direction = horizontal
	#Update the table with the most centered possible placement of the word
	if possible:
		x, y = most_centered	
		for char in word:
			table[x][y] = char
			if direction:
				y = y + 1
			else:
				x = x + 1
		#Return the word, the most centered possible placement of the word, and direction
		return word, most_centered, direction

def print_board(table, correct_words):
	for i in range(len(table)):
		for j in range(len(table[i])):
			char = ' '
			match = False
			for word in correct_words:
				x, y = word[1]
				if word[2]:
					if (j >= y) and (j <= y+len(word[0])) and (i == x):
						match = True
				else:
					if (i >= x) and (i <= x+len(word[0])) and (j == y):
						match = True
			if match:
				char = table[i][j]
			elif table[i][j] != ' ':
				char = '□'
			#char = table[i][j]
			print(char, end=" ")
		print("")

def scramble(letters):
	scrambled = ""
	for x in range(len(letters)):
		rand = random.randint(0, len(letters)-1)
		scrambled = scrambled + letters[rand]
		letters = letters.replace(letters[rand], "", 1)
	return scrambled

def print_letters(letters):
	print("\t", end=" ")
	for char in letters:
		print(char, end=" ")
	print("\n")

def by_length(w):
		return len(w)

def get_difficulty():
	difficulty_text = "Select difficulty:\n\t1) Easy \n\t2) Normal\n\t3) Hard\nOr type 'quit' to exit program.\n"
	user_input = input(difficulty_text).lower()
	incorrect_input = True
	minimum_length, maximum_length = 0, 0
	while incorrect_input:
		incorrect_input = False
		if user_input == "1" or user_input == "easy":
			minimum_length, maximum_length = 5, 6
		elif user_input == "2" or user_input == "normal":
			minimum_length, maximum_length = 7, 9
		elif user_input == "3" or user_input == "hard":
			minimum_length, maximum_length = 10, 20
		elif user_input == "quit":
			minimum_length, maximum_length = 0, 0
		else:
			user_input = input(difficulty_text).lower()
			incorrect_input = True
	return minimum_length, maximum_length

#Driver
#f = open("smallwordlist.txt", "r") #Small dictionary
f = open("wordlist.txt", "r") #Medium dictionary
dictionary = f.read().split(",") 
#dictionary = words.words() #Hard dictionary
#dictionary = list(get_english_words_set(['web2'], lower=False, alpha=True)) #Also too hard
print("Welcome to Pyscape!")
minimum_length, maximum_length = get_difficulty()
while minimum_length != 0 and maximum_length != 0:
	#Setup
	letters = find_random_word(dictionary, minimum_length, maximum_length)
	all_words = find_words(dictionary, letters)
	all_words.sort(reverse=True, key=by_length)
	table, words_on_table = create_table(all_words)
	already_guessed = []
	correct_words = []
	#Begin game
	print_board(table, correct_words)
	print_letters(scramble(letters))
	#for words in words_on_table:
	#	print(words[0], end=", ")
	guess = input("Find all the words on the board using the letters above.\nOr type 'give up' to end game.\n").lower()
	#Loop until all words are guessed
	while words_on_table != [] and guess != "give up":
		#Check for correct guess
		correct_guess = False
		for word in words_on_table:
			#Correct guess found, print table with updated list
			if not correct_guess and word[0] == guess:
				correct_guess = True
				words_on_table.remove(word)
				correct_words.append(word)
				already_guessed.append(guess)
				print_board(table, correct_words)
				print_letters(scramble(letters))
				print(guess + " is correct!")
		#If incorrect guess, print appropriate message
		if not correct_guess:
			if already_guessed.count(guess) != 0:
				print(guess + " has already been guessed.")
			elif all_words.count(guess) != 0:
				all_words.remove(guess)
				already_guessed.append(guess)
				print(guess + " is a bonus word.")
			elif dictionary.count(guess) != 0:
				if len(guess) <= 1:
					print(guess + " is too short.")
				else:
					print(guess + " contains incorrect letters")
			else:
				print(guess + " is not in our dictionary.")
		if words_on_table != []:
			guess = input().lower()
	if words_on_table == []:
		print("Congrats, you finished the Pyscape!")
	minimum_length, maximum_length = get_difficulty()
f.close()