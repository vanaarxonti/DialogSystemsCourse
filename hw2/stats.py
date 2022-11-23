
import numpy as np
import nltk
from nltk.tokenize import word_tokenize, sent_tokenize

file_path = "C:\\Users\\madru\\Downloads\\dialog-babi-task5-full-dialogs-trn.txt"

def processing(file_path):
    path = file_path
    file = open(path, 'r', encoding='utf8') # open the file_path , reading it with encoding 'utf8' for txt files
    content = file.readlines() # reading every line of the file

    userDialogues = []
    allUserSentences = []
    allSystemSentences = []
    systemDialogues = []
    count = 0
    userSentences = [ ]
    systemSentences = [ ]
    # Strips the newline character
    for l in content:
        line = l.strip()  #remove new line

        if (len(line) > 0): #checking if line is not empty
            line = line.split(" ", 1)[1] #removing numbers ID


        if ("<SILENCE>" in line or line.startswith("resto_")): #check if a line stwth resto or it includes Silence , if so, continue

            count += 1
            continue

        if len(line) == 0: #if line is empty --> this is a dialogue
            userDialogues.append(userSentences)
            systemDialogues.append(systemSentences)
            userSentences = []
            systemSentences = []
            continue

        sentences = line.split("\t") #splitting based on tab
        userSentence = sentences[0]  #the first element is the User's Sentence
        systemSentence = sentences[1] #the second element is the System's Sentence

        if ("<SILENCE>" in content[count+1]):
            lineWithOutNumber = content[count+1].split(" ", 1)[1]
            systemSentence = systemSentence + " " + lineWithOutNumber.split("\t")[1]

        userSentences.append(userSentence)
        systemSentences.append(systemSentence)

        allSystemSentences.append(systemSentence)
        allUserSentences.append(userSentence)
        count += 1

    print("Number Of Dialogs Count: " + str(len(userDialogues)))
    print( "Number of user sentences - turns " + str(len(allUserSentences)))
    print("Number of system sentences - turns " + str(len(allSystemSentences)))

    N = ":"
    words_in_allUsersent = [word_tokenize(i) for i in allUserSentences] # creating a list of lists, including the words of every user sentence, using list comprehension
    words_in_allSystemsent = [word_tokenize(i) for i in allSystemSentences] #creating a list of lists, including the words of every system sentence, using list comprehension
    words_in_allSystemsent= [[ele for ele in sub if ele !=N] for sub in words_in_allSystemsent] #creating a list of lists includings words of system's sentences  removing symbol { : }
    total_system_words = sum([len(word) for word in words_in_allSystemsent])  #finding the length of system's words
    total_user_words = sum([len(word) for word in words_in_allUsersent])  #finding the length of user's words


    from itertools import chain
    set_user_words = len(dict.fromkeys(chain.from_iterable(words_in_allUsersent))) # length of  user's unique words
    system = list(dict.fromkeys(chain.from_iterable(words_in_allSystemsent))) # a list with the unique words of system
    system_words = [] # an empty list in which we would add the real unique number of bot
    for word in system:  #for loop in order to substract the resto references and find the real vocabulary size
        if not word.startswith("resto_"):
            system_words.append(word)





    array_system = [len(word) for word in words_in_allSystemsent] #creating a list of lists with the length of words for each system's sentence
    array_user = [len(word) for word in words_in_allUsersent ] #creating a list of list with the length of words for each system's sentence
    array_user_turns = [len(sent) for sent in userDialogues] #creating a list of lists with the length of sentences in all Dialogues
    x = np.array(array_user) #transforming to arrays of length for each one seperately ( user, system, turns) using the numpy library
    y = np.array(array_system)
    z = np.array(array_user_turns)

    standdev_user = x.std() #finding the standard deviation for each one seperately using the std method of np lib
    standdev_system = y.std()
    standdev_turn = z.std()

    print(f"Total number of words in User sentences are:",total_user_words )
    print(f"Total number of words in System sentences are:",total_system_words )
    print(f"Mean number of occurence of  turns in a dialogue is", len(allUserSentences) /len(userDialogues))
    print(f"Mean number of occurence of  user words in a turn is", total_user_words / len(allUserSentences))
    print(f"Mean number of occurence of  system words in a turn is", total_system_words / len(allSystemSentences))
    print(f"The vocabulary size of User sentences are: {set_user_words} words")
    print(f"The vocabulary size of  System sentences are: {len(system_words)} words")
    print(f"Standard deviation of user words in a turn",standdev_user)
    print(f"Standard deviation of system words in a turn", standdev_system)
    print(f"Standard deviation of turns in a dialogue", standdev_turn)

processing(file_path)



