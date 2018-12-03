import math
import random

# global fields
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

# node class (used in id3, display, tester, etc.)
class Node:
    def __init__(self, name):
        self.children = {}
        self.label = str(name)

    def getChildren(self):
        return self.children

    def addChild(self, key, value):
        self.children[key] = value

    def getLabel(self):
        return self.label


def reader_and_packager():
    # reads files with data. Returns a list of tuples - the first value being a decision, the second value being a dictionary of an example

    file = open("GeneralizedDataPizza.txt", "r") # change the file here!

    # finding headers and storing them
    global headers
    headers = file.readline().strip().split(",")
    global headers_without_question
    headers_without_question = list(headers)
    headers_without_question.pop(0)

    # splitting on lines and storing them
    for line in file:
        all_answers.append(line[0])
        example_list.append(line.strip().split(","))

    global answer_set
    answer_set = set(all_answers)

    return

def entropy_calculator(examples):
    # calculates the "entropy" of a certain data set: how much variation there is between answers

    answers = []
    for example in examples:
        answers.append(example[0])

    # making a set
    answerSet = set(answers)

    # calculating entropy
    overallEntropy = 0
    for answer in answerSet:
        pVal = float(answers.count(answer) / len(answers))
        subVal = float(pVal) * math.log(float(pVal), 2)
        overallEntropy -= subVal

    return overallEntropy

def information_gain(examples, header):
    # calculates the potential entropy drop by splitting a tree on a specific header and its values
    # example: splitting a tree on the header "outlook," and its values sunny, overcast, and rainy

    # fields
    all_possible_values = []  # all possible values for a given attribute (example: given "wind," it'd contain *every* weak and strong
    header_index = headers.index(header)  # index of that attribute (header)
    overall_entropy = entropy_calculator(examples)  # overall entropy to reference later without calling the function -- makes the math cleaner
    valueDict = {}  # a dictionary whose key is an attribute value (weak) that results in all of the examples where that att value exists
    temp_list = []

    # getting all of the possible values of an attribute w/o duplicates
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

    # info gain math
    for value in values_set:
        subEntropy = (all_possible_values.count(value) / len(all_possible_values)) * entropy_calculator(valueDict[value])
        overall_entropy -= subEntropy

    return overall_entropy

def id3(examples, remaining_headers):
    # organizing data into a tree using nodes, entropy and info_gain

    # if all of the possible answers are of one option (example: all yes) -- id3 will return a leaf node with that label
    temp_answer_list = []
    for example in examples:
        temp_answer_list.append(example[0])
    if len(set(temp_answer_list)) == 1:
        return Node(temp_answer_list[0])

    # if there are no more attributes -- calculating the most common answer and making a leaf node with that answer (example: most common is yes so a leaf node with yes is made!)
    if len(remaining_headers) == 0:
        biggest_ans = str
        biggest_num = 0
        for answer in answer_set:
            if all_answers.count(answer) > biggest_num:
                biggest_num = all_answers.count(answer)
                biggest_ans = all_answers.pop(all_answers.index(answer))

        return Node(biggest_ans)

    # OTHERWISE:
    # finding the best attribute to split on
    best_header = None
    best_info_gain = 0
    for header in remaining_headers:
        gain = information_gain(examples, header)
        if gain >= best_info_gain:
            best_info_gain = gain
            best_header = header

    # making a node with that attribute as the label
    node = Node(best_header)

    # getting all of the possible values of an attribute w/o duplicates
    all_possible_values = []
    for example in examples:
        possible_value = example[headers.index(best_header)]
        all_possible_values.append(possible_value)
    value_set = set(all_possible_values)

    # getting ready to run id3 recursively
    temp_header_list = list(remaining_headers)
    temp_header_list.remove(best_header)

    # populating the children dictionary and running id3 recursively
    for value in value_set:
        temp_list = []
        for example in examples:
            if example[headers.index(best_header)] == value:
                temp_list.append(example)
        child = id3(temp_list, temp_header_list)
        node.addChild(value, child)

    return node

def display(node, level):
    # displaying the tree made in id3

    # spacing
    spacing = ""
    for num in range(level):
        spacing += " - "

    # printing the label at the current level
    if len(node.getChildren().values()) == 0:
        print(spacing + node.getLabel())
    else:
        print(spacing + node.getLabel() + "?")

        # printing recursively!
        for element in node.getChildren().keys():
            print(spacing + " - " + element + ":")
            display(node.getChildren()[element], level + 2)

    return

def tester(proportion):
    # fields
    count = 0

    # parsing data
    random.shuffle(example_list)
    split_num = int(proportion * len(example_list))
    training_data = example_list[:split_num]
    test_data = example_list[split_num:]

    # running id3 on the training_data
    root = id3(training_data, headers_without_question)



    # figuring out how accurate id3 was by "tracing" test data
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

        if node.getLabel() == example[0]:  # id3 result being compared to the actual
            count += 1

    # printing the accuracy of my id3 and its proportion
    print("id3 was " + str(count/len(test_data)) + " accurate, trained on " + str(proportion * 100) + "%")

    return

# RUNNING EVERYTHING Type something random
reader_and_packager()
entropy_calculator(example_list)
root_node = id3(example_list, headers_without_question)
display(root_node, 0)
tester(0.95) # change the amount of training data here!

#No Test Line