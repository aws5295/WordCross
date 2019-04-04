import os
import pickle
import string
from timeit import default_timer as timer

class Node(object):
    """ Represent a node of a tree or graph.

    Each Node optionally has one parent (or none if it is a root node) Node and 
    a list of child Nodes. Each Node has a character associated with it. Each Node
    also has a bool property stating if it is a word.  If this property is True, it 
    means that starting at the root Node of a tree and traversing to that Node will 
    spell out a legal English word.  An example is depicted below using a '*' character
    to represent a Node where the word property is True.

    Examples:
        Given the following tree composed of Nodes:
            T
            |_A
            |_B*
            | |_B
            |   |_Y*
            |_L
              |_E*
              |_L*
              |_E
                |_R*
                |_S
                  |_T*
        We can traverse the tree to find the following words:
            TAB
            TABBY
            TALE
            TALL
            TALLER
            TALLEST

    Attributes:
        character (str): The character [A-Z] the Node represents.
        parent (Node): The parent Node in a tree. None if Node has no parent (root).
        children (list): A list of child Nodes. Empty list if Node has no children.
        is_word (boolean): A flag indicating if the path from the root Node to this Node spells a word.
    """
    def __init__(self, char, parent):
        """Construct a new Node object.

        Args:
            char (str): The character the Node represents. Legal values [A-Z].
            parent (Node): The Parent Node that this is a child of. None if this is root node.
        """
        self.character = char
        self.parent = parent
        self.children = []
        self.is_word = False

    def add_child(self, new_node):
        """Add an existing Node to the current Node's children."""
        self.children.append(new_node)

    def get_word(self):
        """Gets the word associated with the current Node's position in a tree.

        Note:
            The word will only be a legal English word if the `is_word` property of the Node is `True`.

        Returns:
            A string representing the path traversed from the root to the current node.
        """
        reversed_word = []
        reversed_word.append(self.character)

        current_node = self
        while (current_node.parent != None):
            current_node = current_node.parent
            reversed_word.append(current_node.character)
        
        return ''.join(reversed(reversed_word))

def serialize_to_file(node, file_path):
    """Serialize a Node to a file on disk.
    
    Args:
        node (Node): The node to be serialized.
        file_path (str): The path on disk to create the file.
    
    Note:
        The file, if it exists, will be overwritten.
    """
    with open(file_path, 'wb+') as file:
        pickle.dump(node, file)

def deserialize_from_file(file_path):
    """Deserialize a Node from a file on disk.

    Args:
        file_path (str): The path on disk to read the file from.
    """
    with open(file_path, 'rb') as file:
        return pickle.load(file)

def build_tree(file_path):
    """Builds a tree based on a list of English words in a text file.

    Args:
        file_path (str): The path on disk of a text file containing words all starting with the same letter.

    Returns:
        A `Node` that provides a complete representation of every word contained in the file.
    """
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

def solve(possible_letters):
    """Finds all English words that can be composed using only the input letters.

    Args:
        possible_letters (list): A list of letters [A-Z].  Duplicates are allowed.

    Returns:
        A list of all English words that can be composed using only the possible letters.
        The list is first sorted by word length (shortest first), then alphabetically.
    """
    result = []
    # Load all Trees from disk so we can time the speed of the implementation
    trees = [get_tree_for_letter(letter) for letter in set(possible_letters)]

    # Time this
    start = timer()
    for tree in trees:
        get_possible_words(tree, possible_letters, result)
    end = timer()
    print(end - start)

    return sorted(result, key=lambda r: (len(r), r.upper()))

def get_possible_words(root: Node, possible_letters, word_list=set()):
    """Gets all possible words from a single tree that can be composed using specified letters.

    This is a recursive function. Callers should supply a `word_list`. Iterations of this function
    will add new words they find to that list.

    Args:
        root (Node): A node representing the root of a tree.
        possible_letters (list): A list of characters [A-Z]. Duplicates are allowed.
        word_list (set): A set of words found while traversing the tree.
    """
    if (root.is_word):
        word_list.append(root.get_word())

    letters = possible_letters[:]
    letters.remove(root.character)
    valid_children = [c for c in root.children if c.character in letters]
    for child in valid_children:
        get_possible_words(child, letters, word_list)

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

def get_tree_for_letter(starting_letter):
    """Returns the Node representing all possible English words starting with a specified letter

    Args:
        starting_letter (str): A character [A-Z].

    Raises:
        ValueError: If `starting_letter` is not a character from [A-Z].
        FileNotFoundError: If `.\TextFiles\master-list.txt` is not present on disk.  This file
            is in the Master branch of this repository and must always be present.
    """
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
    letters = []
    while True:
        letter = input("Enter a letter (Press <ENTER> to stop): ").upper()
        if letter == "":
            print("Computing possible word compinations...")
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
