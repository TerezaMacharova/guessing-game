import json

filename='animaltree.json'

def save_tree(tree, filename):
    """  """
    with open(filename, 'w') as file:
        json.dump(tree, file, indent=4)


def load_tree(filename):
    try:
        with open(filename, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return (print("File was not found."))


def yes_no_question(question):
    while True: 
        answer = input(question + "(yes/no):" ).strip().lower()
        if answer == 'yes' or answer == 'no':
            return answer
        else:
            print("Ups! Seems like you made a mistake. Please try again!")


def guess_animal(node, parent=None, last_answer=None):
    if isinstance(node, str):
        guess = node
        user_answer = yes_no_question(f"Is your animal {guess}?")
        if user_answer == "yes":
            print("I won, you lost! Haha!")
            return 
        else: 
            return (parent, last_answer, guess) #returnig so i know where to update the tree
    else:
        answer = yes_no_question(node['question'])
        if answer == 'yes':
            return guess_animal(node['yes'], node, 'yes')
        else:
            return guess_animal(node['no'], node, 'no')


def new_animal(parent, last_answer, guess):
    new_animal = input("I give up. What was your animal? ").strip().lower()

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

    update_tree(parent, last_answer, guess, new_animal, question, answer_new_animal)


def update_tree(parent, last_answer, guess, new_animal, question, answer_new_animal):
        
    #if last_answer:
        new_node = {
            "question": question,
            "yes": new_animal if answer_new_animal == 'yes' else guess,
            "no": guess if answer_new_animal == 'yes'else new_animal,
        }
        if last_answer == 'yes':
            parent['yes'] = new_node
        else:
            parent['no'] = new_node
    #else:
    #    # This would be for the root node if necessary
    #    tree['question'] = question
    #    tree['yes'] = new_animal if last_answer == 'yes' else guess
    #    tree['no'] = guess if last_answer == 'yes' else new_animal


def play():
    tree = load_tree(filename)
    if tree is None:
        tree = {
            "question": "Does it fly?",
            "yes": "bird",
            "no": "fish",
        }

    path_info = guess_animal(tree)
    if path_info:  # If the guess was incorrect
        parent, last_answer, guess = path_info
        new_animal(parent, last_answer, guess)
        save_tree(tree, filename)
        print("Thank you! I've learned something new.")

play()