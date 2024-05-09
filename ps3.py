# 6.0001 Problem Set 3
#
# The 6.0001 Word Game
# Created by: Kevin Luu <luuk> and Jenna Wiens <jwiens>
#
# Name          : Sofía Caset
# Collaborators : Chat gpt
# Time spent    : 24 hours

import math
import random
import string

VOWELS = 'aeiou'
CONSONANTS = 'bcdfghjklmnpqrstvwxyz'
HAND_SIZE = 7

SCRABBLE_LETTER_VALUES = {
    'a': 1, 'b': 3, 'c': 3, 'd': 2, 'e': 1, 'f': 4, 'g': 2, 'h': 4, 'i': 1, 'j': 8, 'k': 5, 'l': 1, 'm': 3, 'n': 1, 'o': 1, 'p': 3, 'q': 10, 'r': 1, 's': 1, 't': 1, 'u': 1, 'v': 4, 'w': 4, 'x': 8, 'y': 4, 'z': 10
}

# -----------------------------------
# Helper code
# (you don't need to understand this helper code)

WORDLIST_FILENAME = "words.txt"

def load_words():
    """
    Returns a list of valid words. Words are strings of lowercase letters.
    
    Depending on the size of the word list, this function may
    take a while to finish.
    """
    
    print("Loading word list from file...")
    # inFile: file
    inFile = open(WORDLIST_FILENAME, 'r')
    # wordlist: list of strings
    wordlist = []
    for line in inFile:
        wordlist.append(line.strip().lower())
    print("  ", len(wordlist), "words loaded.")
    return wordlist	

# (end of helper code)
# -----------------------------------


#··········#1: Scoring a word ########

def get_word_score(word, n):
    """
    Returns the score for a word. Assumes the word is a
    valid word.

    You may assume that the input word is always either a string of letters, 
    or the empty string "". You may not assume that the string will only contain 
    lowercase letters, so you will have to handle uppercase and mixed case strings 
    appropriately. 

	The score for a word is the product of two components:

	The first component is the sum of the points for letters in the word.
	The second component is the larger of:
            1, or
            7*wordlen - 3*(n-wordlen), where wordlen is the length of the word
            and n is the hand length when the word was played

	Letters are scored as in Scrabble; A is worth 1, B is
	worth 3, C is worth 3, D is worth 2, E is worth 1, and so on.

    word: string
    n: int >= 0
    returns: int >= 0
    """

    assert type(word) == str or "", "No string entered" #se asegura de que solo entren strings
    word = (word.lower())
    lett_values = []
    

    def score_calculator (word, n): #calcular la multi para el score
        
        product = ((7*(len(word)))- (3*(n-(len(word)))))
        
        if product >= 1:
            return product
        else:
            return 1
    
    for l in word:         #chequear valor de letras
        if l in SCRABBLE_LETTER_VALUES.keys():
            lett_values.append(SCRABBLE_LETTER_VALUES[l])
        else:
            if l == "*":                     #Asignando valor a la wildcard
                lett_values.append(0)
                
    def lett_sum(L): #sumar valor de letras
        total = 0
        for i in L:
            total += i
        return total
        
    
        
    return (lett_sum(lett_values)*score_calculator(word, n))
    
    


def display_hand(hand):
    """
    Displays the letters currently in the hand.

    For example:
       display_hand({'a':1, 'x':2, 'l':3, 'e':1})
    Should print out something like:
       a x x l l l e
    The order of the letters is unimportant.

    hand: dictionary (string -> int)
    """
    
    to_display = []
    
    for letter in hand.keys():
        for j in range(hand[letter]):
            to_display.append(letter)
    
    print()
    return " ".join(to_display)
    

def deal_hand(n):
    """
    Returns a random hand containing n lowercase letters.
    ceil(n/3) letters in the hand should be VOWELS (note,
    ceil(n/3) means the smallest integer not less than n/3).

    Hands are represented as dictionaries. The keys are
    letters and the values are the number of times the
    particular letter is repeated in that hand.

    n: int >= 0
    returns: dictionary (string -> int)
    """

            
    
    hand={}
    num_vowels = int(math.ceil(n / 3))


    for i in range(num_vowels - 1):
      
        x = random.choice(VOWELS)
        hand[x] = hand.get(x, 0) + 1
    
    for i in range(num_vowels, n):    
        x = random.choice(CONSONANTS)
        hand[x] = hand.get(x, 0) + 1
        
    hand ['*'] = 1   #Asignando una wildcard a cada mano

    
    return hand


#
#··········#2: Update a hand by removing letters
#
def update_hand(hand, word):
    """
    Does NOT assume that hand contains every letter in word at least as
    many times as the letter appears in word. Letters in word that don't
    appear in hand should be ignored. Letters that appear in word more times
    than in hand should never result in a negative count; instead, set the
    count in the returned hand to 0 (or remove the letter from the
    dictionary, depending on how your code is structured). 

    Updates the hand: uses up the letters in the given word
    and returns the new hand, without those letters in it.

    Has no side effects: does not modify hand.

    word: string
    hand: dictionary (string -> int)    
    returns: dictionary (string -> int)
    """

    hand_update = hand.copy()
    word = word.lower()
    
    for e in word:
        if e in hand:
            hand_update[e] -= 1
            if hand_update[e] <= 0:
                del hand_update [e]

    return hand_update

    



#··········#3: Test word validity and Wildcards
#
def is_valid_word(word, hand, word_list):
    """
    Returns True if word is in the word_list and is entirely
    composed of letters in the hand. Otherwise, returns False.
    Does not mutate hand or word_list.
   
    word: string
    hand: dictionary (string -> int)
    word_list: list of lowercase strings
    returns: boolean
    """

    # is_valid=0
    in_hand = 0
    word_copy = word.lower()
    hand_copy = hand.copy()
    # wildcard_checked = True
    
    
    for e in word_copy:
        if e in hand and hand_copy[e] >= 1:
            in_hand += 1
            hand_copy [e] -= 1
    
    if in_hand == len(word_copy):
        if '*' in word_copy:
            for v in VOWELS:
                prob_word = word_copy.replace('*', v) #Asignando identidad a la wildcard.
                if prob_word in word_list:
                    return True
        else: 
            if word_copy in word_list:
                return True
    else:
        return False
    




#··········#4: Playing a hand
#
def calculate_handlen(hand):
    """ 
    Returns the length (number of letters) in the current hand.
    
    hand: dictionary (string-> int)
    returns: integer
    """
    
    return sum(hand.values())

    

def play_hand(hand, word_list):

    """
    Allows the user to play the given hand, as follows:

    * The hand is displayed.
    
    * The user may input a word.

    * When any word is entered (valid or invalid), it uses up letters
      from the hand.

    * An invalid word is rejected, and a message is displayed asking
      the user to choose another word.

    * After every valid word: the score for that word is displayed,
      the remaining letters in the hand are displayed, and the user
      is asked to input another word.

    * The sum of the word scores is displayed when the hand finishes.

    * The hand finishes when there are no more unused letters.
      The user can also finish playing the hand by inputing two 
      exclamation points (the string '!!') instead of a word.

      hand: dictionary (string -> int)
      word_list: list of lowercase strings
      returns: the total score for the hand
      
    """
    

    total_score = []
    
    def the_total_score(L):
        total = 0
        for i in L:
            total += i
        return total
    
    hand_len = calculate_handlen(hand)
    
    while hand_len >= 1:
        print ()
        hand_len = calculate_handlen(hand)
        displayed_hand = display_hand(hand)
        print ("Current hand:", displayed_hand)
        guess = input('Enter word, or "!!" to indicate that you are finished:' )
        
        
        if guess == '!!':
            print("Total score for this hand:", the_total_score(total_score), 'points')
            return the_total_score(total_score)
            break
        else:
            if is_valid_word(guess, hand, word_list):
                
                total_score.append(get_word_score(guess, hand_len))
                
                print(guess, 'earned' , get_word_score(guess, hand_len) , 'points. Total:', the_total_score(total_score), 'points')
                hand = update_hand(hand, guess)
                hand_len = calculate_handlen(hand)
            else: 
                print("Not a valid word mate...")
                
    return the_total_score(total_score)

#
#··········#5: Playing a game


def substitute_hand(hand, letter):
    """ 
    Allow the user to replace all copies of one letter in the hand (chosen by user)
    with a new letter chosen from the VOWELS and CONSONANTS at random. The new letter
    should be different from user's choice, and should not be any of the letters
    already in the hand.

    If user provide a letter not in the hand, the hand should be the same.

    Has no side effects: does not mutate hand.

    For example:
        substitute_hand({'h':1, 'e':1, 'l':2, 'o':1}, 'l')
    might return:
        {'h':1, 'e':1, 'o':1, 'x':2} -> if the new letter is 'x'
    The new letter should not be 'h', 'e', 'l', or 'o' since those letters were
    already in the hand.
    
    hand: dictionary (string -> int)
    letter: string
    returns: dictionary (string -> int)
    """
    
    abc = list('abcdefghijklmnopqrstuvwxyz')
    # abc = list(abce)

    
    new_hand = hand.copy()
    old_letter = letter
    new_letter = random.choice(abc)
    
    if old_letter in hand:
        new_hand [new_letter] = new_hand.pop(old_letter) #Asigna a una nueva key el valor de otra
        return new_hand                                  #Que a la vez se elimina.

       
    
def play_game(word_list):
    """
    Allow the user to play a series of hands

    * Asks the user to input a total number of hands

    * Accumulates the score for each hand into a total score for the 
      entire series
 
    * For each hand, before playing, ask the user if they want to substitute
      one letter for another. If the user inputs 'yes', prompt them for their
      desired letter. This can only be done once during the game. Once the
      substitue option is used, the user should not be asked if they want to
      substitute letters in the future.

    * For each hand, ask the user if they would like to replay the hand.
      If the user inputs 'yes', they will replay the hand and keep 
      the better of the two scores for that hand.  This can only be done once 
      during the game. Once the replay option is used, the user should not
      be asked if they want to replay future hands. Replaying the hand does
      not count as one of the total number of hands the user initially
      wanted to play.

            * Note: if you replay a hand, you do not get the option to substitute
                    a letter - you must play whatever hand you just had.
      
    * Returns the total score for the series of hands

    word_list: list of lowercase strings
    """
    subs_used = False
    replay_used = False
    key = 0
    hand_names = ["Round 1", "Round 2","Round 3","Round 4","Round 5","Round 6","Round 7","Round 8","Round 9","Round 10",]
    hand_index = 0
    
    
    print("Welcome to scrabble game!")
    num_hands = int(input("Enter how many hands you would like to play: "))    
    TOTAL_SCORE = {}    
    
    for i in range(num_hands):
        
        hand = deal_hand(HAND_SIZE)
       
        if subs_used is False: #Offers to subtitute a letter 
            print("Current hand: ", display_hand(hand))
            
            subs = input("Would you like to subtitute a letter?: ")
            subs = subs.lower()
        
            
            if subs == 'yes':
                while subs_used == False:
                    letter = input("What letter would you like to change?: ")
                    if letter in hand:                        
                        hand = substitute_hand(hand, letter)
                        subs_used = True
                    else:
                            print("That letter ain't there! \n", )

                
        round_score = play_hand(hand, word_list)
        hand_name = hand_names[hand_index] #se le da un nombre a la mano                                                                        
        TOTAL_SCORE[hand_name] = round_score  #se usa ese nombre como key para almacenar el puntaje
        
        if replay_used == False:
            ask_replay = input('Would you like to replay the hand?').lower()
            if ask_replay == 'yes':               
                                
                replay_score = play_hand(hand, word_list)
                TOTAL_SCORE[hand_name]= max(round_score, replay_score) #Si se rejuega la misma mano
                                                                       #Se almacena el puntaje más alto
                replay_used = True
                

        hand_index += 1 #Pasamos a la siguiente mano → siguiente key del dict.
        
    print ("\n Now let's see the scores you got!.......\n")       
    for key, value in TOTAL_SCORE.items():
        print (f'{key}:{value}')
    
    print("\n Calculating total score...........\n" )
    
    final_score = sum(TOTAL_SCORE.values())
    
    if final_score <= 100:
        print("Well, at least it was fun!")
    elif final_score > 100 and final_score <= 200:
        print("Not bad at all huh")
    elif final_score > 200 and final_score <= 270:
        print("Impressive!")
    elif final_score > 270 and final_score <= 350:
        print("Way to go, cowboy/girl.")
    elif final_score > 350:
        print ("Absolute champion.")
    
    print("✶ ✶ ✶ " + str(final_score) + ' ✶ ✶ ✶')
    
    return 
    


if __name__ == '__main__':
    word_list = load_words()
    play_game(word_list)


 