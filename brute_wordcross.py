import os
from timeit import default_timer as timer
import string

def print_solution(words):
    """Prints a word list to the stdout.

    Args:
        words (list): A list of strings.
    """
    curr_len = 0
    for word in words:
        if curr_len != len(word):
            print(str(len(word)) + "-Letter Words:")
            curr_len = len(word)
        print(word)

def split_file(file_name, output_dir):
    """Splits a file of English words into separate files based on the starting letter of the word.

    The resulting file name is deterministic: `<Starting Letter>-words.txt`.
    Where <Starting Letter> is the first letter of all words contained in that file.

    Example:
        If the following words were in the input file:
            ABLE
            ARE
            BARE
            CAR
        The following output files would be produced:
            A-words.txt (Containing: ABLE, ARE)
            B-words.txt (Containing: BARE)
            C-words.txt (Containing: CAR)
    
    Args:
        file_name (str): The path on disk to a list of line-delimited English words.
        output_dir (str): The path to a directory where the deterministic output files will be generated.
    """
    words = [line.strip() for line in open(file_name)]

    # Process the words into a dictionary where the key is the first letter, value is the list of words
    grouped_words = {}
    for word in words:
        grouped_words.setdefault(word[0].upper(), []).append(word.upper())

    # Loop through each letter and write an output file for all the words starting with that letter
    for letter in grouped_words:
        output_file_name = str(letter) + "-words.txt"
        output_file_path = os.path.join(output_dir, output_file_name)
        
        with open(output_file_path, 'w+') as file:
            file.writelines("%s\n" % word for word in grouped_words[letter])

def get_word_list_for_letter(letter):
    if ((len(letter) != 1) or (letter.upper() not in string.ascii_uppercase)):
        raise ValueError("Input must be a single letter from [A-Z]")

    base_directory = os.path.dirname(__file__)

    # If word list exists for letter, build the data file and return node
    expected_word_list_name = "TextFiles/" + str(letter) + "-words.txt"
    expected_word_list_path = os.path.join(base_directory, expected_word_list_name)
    if os.path.isfile(expected_word_list_path):
        return [line.strip() for line in open(expected_word_list_path)]

    # If the master list does not exist, cannot continue
    expected_master_word_list_name = "TextFiles/master-list.txt"
    expected_master_word_list_path = os.path.join(base_directory, expected_master_word_list_name)
    if not os.path.isfile(expected_master_word_list_path):
        raise FileNotFoundError("Expected to find 'masterlist.txt' in local 'TextFiles' directory!")

    # If the master list does exist, split it into individual word lists
    output_dir = os.path.join(base_directory, "TextFiles")
    split_file(expected_master_word_list_path, output_dir)
    return get_word_list_for_letter(letter)

def solve(possible_letters):
    result = []
    # Load all Trees from disk so we can time the speed of the implementation
    word_lists = [get_word_list_for_letter(letter) for letter in set(possible_letters)]

    # Time this
    start = timer()
    for word_list in word_lists:
        get_possible_words(word_list, possible_letters, result)
    end = timer()
    print(end - start)

    return sorted(result, key=lambda r: (len(r), r.upper()))

def get_possible_words(word_list: list, possible_letters, result):
    for word in word_list:
        if len(word) > len(possible_letters):
            pass
        else:
            valid = True
            letters = possible_letters[:]
            for letter in word:
                if letter in letters:
                    letters.remove(letter)
                else:
                    valid = False
            if valid:
                result.append(word)

if __name__ == "__main__":
    letters = []
    while True:
        letter = input("Enter a letter (Press <ENTER> to stop): ").upper()
        if letter == "":
            print("Computing possible word combinations...")
            break
        if letter not in string.ascii_uppercase:
            print("Invalid input - must be a letter [A-Z]!")
        else:
            letters.append(letter)
        
        output = "Current letters: "
        for letter in letters:
            output += letter + " " 
        print(output)

    answers = solve(letters)
    #print_solution(answers)
    print(len(answers))