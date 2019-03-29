import os
import pickle
import string

class Node(object):
    def __init__(self, char, parent):
        self.character = char
        self.parent = parent
        self.children = []
        self.is_word = False

    def add_child(self, new_node):
        self.children.append(new_node)

    def get_word(self):
        reversed_word = []
        reversed_word.append(self.character)

        current_node = self
        while (current_node.parent != None):
            current_node = current_node.parent
            reversed_word.append(current_node.character)
        
        return ''.join(reversed(reversed_word))

def serialize_to_file(node, file_path):
    with open(file_path, 'wb+') as file:
        pickle.dump(node, file)

def deserialize_from_file(file_path):
    with open(file_path, 'rb') as file:
        return pickle.load(file)

# TODO: Add DOC String
def build_tree(file_path):
    words = [line.strip() for line in open(file_path)]
    root_letter = words[0][0]
    root_node = Node(root_letter, None)

    for word in words:
        current_node = root_node
        for index, char in enumerate(word):
            if (index == 0 and char != root_letter):
                raise ValueError("Word does not belong in this word list: " + str(word))

            if (index != 0):
                child_node = next((node for node in current_node.children if node.character == char), None)
                if child_node != None:
                    current_node = child_node
                else:
                    new_child = Node(char, current_node)
                    current_node.add_child(new_child)
                    current_node = new_child

            if (index == len(word) - 1): # end of word
                current_node.is_word = True
    
    return root_node

# TODO: Add DOC String
def get_words_in_tree(root_node: Node, words=[]):
    if (root_node.is_word):
        words.append(root_node.get_word())

    for child_node in root_node.children:
        get_words_in_tree(child_node, words)

# TODO: Add DOC String
def split_file(file_name, output_dir):
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

# TODO: Add DOC String
def get_tree_for_letter(starting_letter):
    if ((len(starting_letter) != 1) or (starting_letter.upper() not in string.ascii_uppercase)):
        raise ValueError("Input must be a single letter from [A-Z]")

    base_directory = os.path.dirname(__file__)

    # If data file exists, return it
    expected_data_file_name = "DataFiles/" + str(starting_letter) + "-data.node.bin"
    expected_data_file_path = os.path.join(base_directory, expected_data_file_name)
    if os.path.isfile(expected_data_file_path):
        return deserialize_from_file(expected_data_file_path)

    # If word list exists for letter, build the data file and return node
    expected_word_list_name = "TextFiles/" + str(starting_letter) + "-words.txt"
    expected_word_list_path = os.path.join(base_directory, expected_word_list_name)
    if os.path.isfile(expected_word_list_path):
        node = build_tree(expected_word_list_path)
        serialize_to_file(node, expected_data_file_path)
        return node

    # If the master list does not exist, cannot continue
    expected_master_word_list_name = "TextFiles/master-list.txt"
    expected_master_word_list_path = os.path.join(base_directory, expected_master_word_list_name)
    if not os.path.isfile(expected_master_word_list_path):
        raise FileNotFoundError("Expected to find 'masterlist.txt' in local 'TextFiles' directory!")

    # If the master list does exist, split it into individual word lists
    output_dir = os.path.join(base_directory, "TextFiles")
    split_file(expected_master_word_list_path, output_dir)
    return get_tree_for_letter(starting_letter)

if __name__ == "__main__":
    tree = get_tree_for_letter("W")
    words_in_tree = []
    get_words_in_tree(tree, words_in_tree)
    print(words_in_tree[:10]) # print first 10 words
    print(len(words_in_tree))