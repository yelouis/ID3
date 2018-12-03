import math
import random

global example_list
example_list = []
global all_answers
all_answers = []
global headers
headers = []
global headers_without_question
headers_without_question = []
global answer_set
answer_set = set([])

class Node:
    '''
    This class will create Nodes for the Decision Tree
    '''
    def __init__(self, name):
        '''
        Creates variable associated with class

        :type name: String
        :param name: The name of the node
        '''
        self.children = {}
        self.label = str(name)

    def getChildren(self):
        '''
        Function for getting the children for a node

        :return: The nodes that are the children for the current node
        '''
        return self.children

    def addChild(self, key, value):
        '''
        Adds a child to the current node

        :type key: String
        :param key: The key of the child node being added
        :type value: String
        :param value: The value of the child node being added
        :return: The child node that was added in the list of children where the key is the index and the value is the value
        '''
        self.children[key] = value

    def getLabel(self):
        '''
        Function that gets the label of the current node

        :return: The label of the current node
        '''
        return self.label


def reader_and_packager(textFile):
    '''
    Reads the file with the data. It first finds the headers and stores them. Then it splits by line on the rest of the text file and stores them.

    :type textFile: String
    :param textFile: The name of the text file that is being read.
    :return: Returns a list of tuples.
    The first value is the catagory and the second value is the dictionary of all of the catagory's attributes where the key in the dictionary is the label.
    '''

    file = open(textFile, "r")

    global headers
    headers = file.readline().strip().split(",")
    global headers_without_question
    headers_without_question = list(headers)
    headers_without_question.pop(0)

    for line in file:
        all_answers.append(line[0])
        example_list.append(line.strip().split(","))

    global answer_set
    answer_set = set(all_answers)

    return

def entropy_calculator(examples):
    '''
    This function calculates the entropy of the data set to see the amount fo variation there is between answers.

    :type examples: Dictionary
    :param examples: A dictionary of all of the catagory's attributes where the key in the dictionary is the label
    :return: The overall entropy of the data set
    '''

    answers = []
    for example in examples:
        answers.append(example[0])

    answerSet = set(answers)

    overallEntropy = 0
    for answer in answerSet:
        pVal = float(answers.count(answer) / len(answers))
        subVal = float(pVal) * math.log(float(pVal), 2)
        overallEntropy -= subVal

    return overallEntropy

def information_gain(examples, header):
    '''
    This function calculates the potential entropy drop by splitting a tree by a specific header and its values

    :type examples: Dictionary
    :param examples: A dictionary of all of the catagory's attributes where the key in the dictionary is the label
    :type header: List
    :param header: A list of all the headers
    :return: The overall entropy after subtracting the highest entropy drop
    '''

    all_possible_values = []
    header_index = headers.index(header)
    overall_entropy = entropy_calculator(examples)
    valueDict = {}
    temp_list = []

    for example in examples:
        possible_value = example[header_index]
        all_possible_values.append(possible_value)
    values_set = set(all_possible_values)

    for value_option in values_set:
        for example in examples:
            possible_value = example[header_index]
            if possible_value == value_option:
                temp_list.append(example)
        valueDict[value_option] = list(temp_list)
        temp_list.clear()

    for value in values_set:
        subEntropy = (all_possible_values.count(value) / len(all_possible_values)) * entropy_calculator(valueDict[value])
        overall_entropy -= subEntropy

    return overall_entropy

def id3(examples, remaining_headers):
    '''
    This function organizes the data into a tree using the information it collected from entropy and information gain.
    It finds the best attribute to split on and makes a node with that attribute as the label.
    Then it runs recursively until there are no more attributes or if all the possible answers are of one option.
    Example: All options return yes. In which case, ID3 will return a leaf node with that label

    :type examples: Dictionary
    :param examples: A dictionary of all of the catagory's attributes where the key in the dictionary is the label
    :type remaining_headers: List
    :param remaining_headers: A list of the remaining headers that haven't been used because information gain was too low
    :return: A labeled node with or without children nodes. The root node is what will be returned overall and the root ndoe is the tree
    '''

    temp_answer_list = []
    for example in examples:
        temp_answer_list.append(example[0])
    if len(set(temp_answer_list)) == 1:
        return Node(temp_answer_list[0])

    if len(remaining_headers) == 0:
        biggest_ans = str
        biggest_num = 0
        for answer in answer_set:
            if all_answers.count(answer) > biggest_num:
                biggest_num = all_answers.count(answer)
                biggest_ans = all_answers.pop(all_answers.index(answer))

        return Node(biggest_ans)

    best_header = None
    best_info_gain = 0
    for header in remaining_headers:
        gain = information_gain(examples, header)
        if gain >= best_info_gain:
            best_info_gain = gain
            best_header = header

    node = Node(best_header)

    all_possible_values = []
    for example in examples:
        possible_value = example[headers.index(best_header)]
        all_possible_values.append(possible_value)
    value_set = set(all_possible_values)

    temp_header_list = list(remaining_headers)
    temp_header_list.remove(best_header)

    for value in value_set:
        temp_list = []
        for example in examples:
            if example[headers.index(best_header)] == value:
                temp_list.append(example)
        child = id3(temp_list, temp_header_list)
        node.addChild(value, child)

    return node

def display(node, level):
    '''
    This function displays the tree made in id3 by printing the nodes in terminal recursively

    :type node: Node
    :param node: Node with label
    :type level: Integer
    :param level: The level that the node is on which is used to determine the spacing the in the printed statement
    :return: A printed statement of the tree in the terminal
    '''

    spacing = ""
    for num in range(level):
        spacing += " - "

    if len(node.getChildren().values()) == 0:
        print(spacing + node.getLabel())
    else:
        print(spacing + node.getLabel() + "?")

        for element in node.getChildren().keys():
            print(spacing + " - " + element + ":")
            display(node.getChildren()[element], level + 2)

    return

def tester(proportion):
    '''
    A function for testing the accuracy of the tree by splitting the dataset into a training dataset and a testing data set

    :type proportion: Float
    :param proportion: The percentage of the dataset used for training
    :return: A printed statement of the accuracy of the ID3 and the percentage of the data that was used for training
    '''
    count = 0

    random.shuffle(example_list)
    split_num = int(proportion * len(example_list))
    training_data = example_list[:split_num]
    test_data = example_list[split_num:]

    root = id3(training_data, headers_without_question)

    for example in test_data:
        node = root
        while len(node.getChildren().values()) != 0:
            header_index = headers.index(node.getLabel())
            if node.getChildren().__contains__(example[header_index]):
                child = node.getChildren()[example[header_index]]
                node = child
            else:
                print("Catch: Key Error")
                break

        if node.getLabel() == example[0]:
            count += 1

    print("id3 was " + str(count/len(test_data)) + " accurate, trained on " + str(proportion * 100) + "%")
    return


if __name__ == '__main__':
    # RUNNING EVERYTHING
    reader_and_packager("GeneralizedDataPizza.txt")
    # Change the text file here
    entropy_calculator(example_list)
    root_node = id3(example_list, headers_without_question)
    display(root_node, 0)
    # Change the amount of training data here!
    tester(0.95)
