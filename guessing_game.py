import json
from tkinter import LAST
from spellchecker import SpellChecker
#import  tkinter as tk
#from tkinter import messagebox

filename = 'animaltree.json'

class GuessingGame:
    def __init__(self, filename):
        self.filename = filename
        self.tree = self.load_tree()
        self.current_node = None


    def save_tree(self):
        """ save the tree to a file """
        with open(self.filename, 'w') as file:
            json.dump(self.tree, file, indent=4)


    def load_tree(self):
        """ load or initialze the tree if it doesn't exit """
        try:
            with open(self.filename, 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            return { #so the game can start with the default
                "question": "Does it havr feathers?",
                "yes": "parrot",
                "no": "cat"
                }


    def yes_no_question(self, question):
        while True: 
            answer = input(question + "(yes/no):" ).strip().lower()
            if answer == 'yes' or answer == 'no':
                return answer
            else:
                print("Ups! Seems like you made a mistake. Please try again!")


    def guess_animal(self, node, parent=None, last_answer=None):
        if isinstance(node, str):
            guess = node
            user_answer = self.yes_no_question(f"Is your animal {guess}?")
            if user_answer == "yes":
                print("I won, you lost! Haha!")
                return True
            else: 
                if parent is not None:
                    self.new_animal(parent, last_answer, guess)
                return False
        else:
            self.current_node = node
            answer = self.yes_no_question(node['question'])
            if answer == 'yes':
                return self.guess_animal(node['yes'], node, 'yes')
            else:
                return self.guess_animal(node['no'], node, 'no')



    def spell_check(self, prompt):
        spell = SpellChecker()

        while True:
            user_input = input(prompt).strip().capitalize()
            # Check if the word is misspelled
            misspelled = spell.unknown([user_input])
            if misspelled:
                # Suggest the most likely correction
                suggestion = spell.correction(user_input)
                confirmation = self.yes_no_question(f"Did you mean '{suggestion}'?")
                if confirmation == 'yes':
                    return suggestion
                else:
                    print("Please enter the animal name again.")
            else:
                # If the word is not misspelled, return it as is
                return user_input


    def new_animal(self, parent, last_answer, guess):
        new_animal = self.spell_check("I give up. What was your animal? ").strip().lower()

        question = input(f"Please enter a question that distinguishes a {new_animal} from a {guess}: ").strip()
        question = question[0].upper() + question[1:].lower()
        if not question.endswith('?'):
            question += '?'

        while True:
            answer_new_animal = input(f"For the {new_animal}, is the answer to your question 'yes' or 'no'? ").strip().lower()
            if answer_new_animal in ['yes', 'no']:
                break
            else:
                print("Please enter 'yes' or 'no'.")

        self.update_tree(parent, last_answer, guess, new_animal, question, answer_new_animal)
        self.save_tree()


    def update_tree(self, parent, last_answer, guess, new_animal, question, answer_new_animal):
        new_node = {        
           "question": question,
            "yes": new_animal if answer_new_animal == 'yes' else guess,
            "no": guess if answer_new_animal == 'yes'else new_animal,
            }

        if last_answer == 'yes':
            parent['yes'] = new_node
        else:
            parent['no'] = new_node
    

    def play(self):
         while True:

            self.current_node = self.tree  # Reset the current node to the start of the tree
            guessed_correctly = self.guess_animal(self.current_node)
            if not guessed_correctly:
                # If the game did not guess correctly, it already went through learning new animal.
                print("Ready for a new round or learn a new animal.")

            play_again = self.yes_no_question("Do you want to play again?")
            if play_again == 'no':
                print("Thanks for playing! See you next time.")
                break

print("Hello! Let's start the game!")
if __name__ == "__main__":
    game = GuessingGame(filename)
    game.play()