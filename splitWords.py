import os

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

if __name__ == "__main__":
    """     current_dir = os.path.dirname(__file__)
    word_file = os.path.join(current_dir, "Textfiles/word-list.txt")
    output_dir = os.path.join(current_dir, "Textfiles")
    
    split_file(word_file, output_dir) """

    current_dir = os.path.dirname(__file__)
    word_file = os.path.join(current_dir, "Textfiles/T-words.txt")
    
    node = build_tree(word_file)
