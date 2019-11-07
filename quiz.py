import os
import os.path
import random
from copy import deepcopy
from sys import platform as _platform
# -----

# COMPATIBLE WITH WINDOWS
# WORKING ON MAC COMPATIBILITY

ogdir = deepcopy(os.getcwd())

# ===== VALIDITY ===== #
# defining setsDir and dividers
def defineGlobals():
    if _platform == "darwin":  # macOS
        divider = "/"
        setsDir = ogdir + divider + "Sets" + divider  # setsDir is valid
    elif _platform == "win32" or _platform == "win64":  # windows
        divider = "\\"
        setsDir = ogdir + divider + "Sets" + divider
    return divider, setsDir


# Defining first globals
divider, setsDir = defineGlobals()


def ensure_valid(dir):  # adds divider to the end of the directory
    if dir[-1] != divider:
        dir = dir + divider
    return dir
# ===== END VALIDITY ===== #

# ===== DEFINING OTHER GLOBALS ===== #
blankStr = ['', ' ']
letters = ['A', 'B', 'C', 'D', 'E']
tags = ["%F", "%S", "%SS", "A%", "%L", "%Q", "%LO", "%OL", "%A"]
special_chars = [":", ","]  # expand the list!
# ===== END DEFINING GLOBALS ===== #

# ===== STREDIT ===== #
def hyphenateStr(str):
    for i in range(len(str)):
        if str[i] == ' ':
            str = str.replace(' ', '-')
    return str


def hyphenateList(list):
    str = ''
    for i in range(len(list) - 1):
        str += list[i] + '-'
        return str


def rspace(str):
    str = str.rstrip()
    i = 0
    while str[i] == ' ':
        str.pop(i)
    return str


def removeWhitespace(str):
    if type(str) == 'str':
        str = rspace(str)
    elif type(str) == 'list':
        for i in range(len(str)):
            ele = rspace(str[i])
            str[i] = ele
    return str
# =====END STREDIT===== #

# NOTE: if unicode error occurs, replace \ with \\

# ===== EXTRA OS FUNCTIONS ===== #
def extractSetName(setDir):
    if divider in setDir:
         setName = ''
         if setDir[-1] == divider and divider == "\\":
             i = -3
         elif setDir[-1] == divider and divider == "/":
             i = -2
         else:
             i = -1
         while setDir[i] != divider:
             setName = setDir[i] + setName
             i -= 1
    else:
        setName = setDir
    return setName


# =====VECTORIZE===== #
def vectorize_file(fileName, fileDir = ''):
    fileVec = []
    with open(os.path.join(fileDir + fileName), 'r', encoding='windows-1252') as file:
        fileVec = file.readlines()
        for line in enumerate(fileVec):
            fileVec[0] = line[1].rstrip()
    file.close()
    return fileVec


def vectorize_files(qFile, aFile):
     qVec, aVec = vectorize_file(qFile), vectorize_file(aFile)
     return qVec, aVec


def vectorize_set(setDir):
    setDir = ensure_valid(setDir)
    setName = extractSetName(setDir)
    qFile, aFile = os.path.join(setDir + setName + '_qs.txt'), os.path.join(setDir + setName + '_ans.txt')
    qVec, aVec = vectorize_files(qFile, aFile)
    return qVec, aVec
# =====END VECTORIZE===== #


def saveDataFiles(fileList, savePath = divider, closeStatus = True):
    savePath = ensure_valid(savePath)
    for i in range(len(fileList)):
        completeName = os.path.join(savePath + fileList[i] + ".dat")
        file1 = open(completeName, "w")
        if closeStatus == True:
            file1.close()
            

def ensureNotBlank(noteName, noteDir):
    if noteDir == '':
        noteDir = input("Enter the directory of your notes: ")
    elif noteName == '':
        noteName = input("Enter the name of your note file: ")
    return noteName, noteDir


def processNotes(noteName = '', noteDir = '', goToQuiz = True):
    if noteName in blankStr or noteDir in blankStr:
        noteName, noteDir = ensureNotBlank(noteName, noteDir)
        return processNotes(noteName, noteDir)

    setName = input("Name your new set: ")
    setName = hyphenateStr(setName)

    if setName not in os.listdir("Sets"):
        os.mkdir(setsDir + setName)
    else:
        string = addNewline("This set already exists.\n \
        To overwrite this set, press C.\n \
        To exit and do neither, press any key")
        editStatus = input(string)
        if editStatus not in ["C", "c"]:
            return None

    # preallocating
    setDir = os.path.join(setsDir + setName)
    fileList = [setName + "_qs", setName + "_ans"]

    # creating new file:
    os.chdir(setDir)
    saveDataFiles(fileList, setDir)
    noteDir = ensure_valid(noteDir)

    # processing notes: writing notes to questions & answers
    with open(os.path.join(noteDir + noteName), "r") as notes:  # opening fine
        with open(os.listdir()[1], "w+") as questions:
            with open(os.listdir()[0], "w+") as answers:
                for line in notes:
                    word = ''
                    defin = ''
                    # definitions
                    if line[0] == "%" and ":" in line:
                        if len(line) > 3 or line[0] + line[1] not in tags:
                            i = 1
                            while line[i] != ":":
                                word += line[i]
                                i += 1
                            if line[i+1] == ' ':
                                i += 2
                            while line[i] != "%":
                                defin += line[i]
                                i += 1
                    if word not in blankStr and defin not in blankStr:
                        questions.write(word + "\n"), answers.write(defin + "\n")
    notes.close(), answers.close(), questions.close()
    os.chdir(ogdir)
    if goToQuiz == True:
        quizStatus = input("Would you like to run this quiz now? [Y/N] ")
        if quizStatus in ["Y", "y"]:
            runShortAnswer(setDir)


def extract_questions(noteDir = '', noteName = ''):
    noteDir = ensure_valid(noteDir)
    unsure_line = []
    question = []
    i = 0
    with open(os.path.join(noteDir + noteName)) as notes:
        for line in notes:
            if line[-1] == '':
                line = line.rstrip()
            if line[-1] == '?':
                unsure_line.append(line)
            if line[0] == "(" and line[1] == "?" and line[2] == ")":
                line = line[4:len(line)-5]
                question.append(line)
            i += 1
    return unsure_line, question


def addNewline(string, end="end"):
    """
    Checks if system is Windows or Mac, adds newline (\n) only if it's Windows.
    This function exists to reconcile some differences between Windows and Mac.
    ALL STRINGS should be passed through this function before printing.
    """
    if _platform == "win32" or _platform == "win64":
        if end == "end":
            string += "\n"
        elif end == "start" or end == "begin":
            string = "\n" + string
    return string


def removeNonDefs(vec):
    i = 0
    for ele in vec:
        if ele[0] == "%" or (ele[0] in ["A", "a"] and ele[1] == "%"):
            vec.remove(ele)
        i += 1
    return vec


def runQuizMC(setDir):
    """
        Runs multiple choice quiz.
    """
    # initializing variables
    setDir = ensure_valid(setDir)
    setName = extractSetName(setDir)
    qVec = vectorize_file(setDir + setName + "_qs.dat")
    qVec = removeNonDefs(qVec)
    og_qVec = deepcopy(qVec)
    totalQs = len(og_qVec)
    score = 0

    # checking run requirements
    if len(qVec) < 5:
         print("ERROR: please add at least 5 questions to this set.")

    # establishing difficulty
    opNum = establishDifficulty()

    # RUNNING QUIZ:
    while len(qVec) > 0:

        # getting random question:
        qInd = random.randint(0, len(qVec)-1)
        question = qVec[qInd]

        # getting correct answer
        aInd = og_qVec.index(question)
        qVec.pop(qInd)
        aVec = vectorize_file(setDir + setName + "_ans.dat")
        aVec = removeNonDefs(aVec)

        # first option: the correct answer
        answers = removeWhitespace(aVec[aInd].split(","))  # this line is complicated, just in case aVec[aInd] is a list.
        officialAns = answers[random.randint(1, len(answers)) - 1]
        options = [officialAns]
        aVec.pop(aInd)     # removing correct answer from aVec

        # getting other potential answers
        for i in range(opNum - 1):
            aInd = random.randint(0, len(aVec)-1) # this is where you need to implement your lists model. right here. 433
            fakeAnswers = removeWhitespace(aVec[aInd].split(","))
            fakeAnswer = answers[random.randint(1, len(fakeAnswers)) - 1]
            options.append(fakeAnswer)
            aVec.pop(aInd)

        # presenting the question:
        qString = addNewline(question + ":")
        j = 0
        while len(options) > 0:
            i = random.randint(0, len(options)-1)
            addString = addNewline(letters[j] + ". " + options[i])
            qString += addString
            if options[i] == officialAns:
                letterAns = letters[j]
            options.pop(i)
            j += 1

        # getting the user answer:
        userAns = input(qString)

        # error check:
        if letterAns not in letters:
            print("**CRITICAL ERROR: letterAns undefined. Revise code @ Sarah. Sorry user :'(**")

        # Keeping score:
        if userAns in [letterAns.lower(), letterAns.upper()] or userAns == officialAns:
            print(addNewline("Correct!"))
            score += 1
        elif userAns in ["-M-", "-m-", "-Q-", "-q-"]:
            return None
        else:
            print(addNewline("Incorrect, try again later."))

    # Result messages
    printScore(score, totalQs)
    return 1


def printAnswers(answers, correct):
    """

    """
    # RETURNS A STRING, WHICH YOU MUST PRINT IN ANOTHER FUNCTION
    if len(answers) == 0:
        print(addNewline("**ERROR: No answers to print.**"))
    if not correct:
        if len(answers) == 1:
            print(addNewline("Incorrect. The correct answer is " + answers[0]))
        else:
            string = "Incorrect. The correct answers are: "
            for i in range(len(answers)):
                string += answers[i] + ", "
                if i == len(answers) - 1:
                    string += "or " + answers[i]
            print(string)
    if correct:
        if len(answers) == 1:
            print(addNewline("Correct!\nThe correct answer is " + answers[0]))
        else:
            string = 'Correct!\nThe correct answers are: '
            for i in range(len(answers)):
                if i == len(answers) - 1:
                   string += "or " + answers[i]
                else:
                    string += answers[i] + ", "
            print(addNewline(string))


def runShortAnswer(setDir):
    """
    Runs quiz
    """
    # initializing variables
    setDir = ensure_valid(setDir)
    os.chdir(setDir)
    qVec, aVec = vectorize_files(os.listdir()[1], os.listdir()[0])  #files are in alphabetical order
    og_qVec = deepcopy(qVec)
    score = 0
    totalQs = len(og_qVec)

    while len(qVec) > 0:
        # selecting a random Question
        ind = random.randint(0, len(qVec)-1)
        question = aVec[ind]

        # finding its correct answer
        answers = qVec[ind].split(",")
        answers = removeWhitespace(answers)

        # getting userinput
        userAns = input(addNewline(question))

        # checking if userAns is right or wrong
        for i in range(len(answers)):
            if hyphenateStr(userAns.rstrip()).lower() == hyphenateStr(answers[i].rstrip()).lower():  # correct answer
                printAnswers(answers, True)
                score += 1
            # elif keywords in userAns:
                # print("Somewhat correct. The correct answer is " + answer)
                # score += 0.5
            elif userAns in ["-Q-", "-q-", "M", "-m-"]:  # return to menu.
                return None
            else:  # wrong answer
                printAnswers(answers, False)
        qVec.pop(ind)
        aVec.pop(ind)
    printScore(score, totalQs)
    return 1


def establishDifficulty():
    opNum = 0
    while opNum == 0:
        difficulty = input("Choose your difficulty: Easy (E), Medium (M) or Hard (H) ")
        if difficulty in ["E", "e"]:
            opNum = 3
        elif difficulty in ["M", "m"]:
            opNum = 4
        elif difficulty in ["H", "h"]:
            opNum = 5
        elif difficulty in ["-Q-", "-q-", "-m-", "-M-"]:
            return None
        else:
            print("Invalid. Please enter a valid option next time.")
    return opNum


def combine_sets(setList):
    master_qVec = []
    master_aVec = []
    for i in range(len(setList)):
        qFile = os.path.join(setsDir + setList[i] + divider + setList[i] + "_qs.dat")
        aFile = os.path.join(setsDir + setList[i] + divider + setList[i] + "_ans.dat")
        questions, answers = vectorize_files(qFile, aFile)
        master_qVec += questions
        master_aVec += answers
    os.chdir(ogdir)
    return master_qVec, master_aVec


def printScore(score, totalQs):
    percent = round(score / totalQs * 100, 2)
    print("Your score is " + str(score) + " out of " + str(totalQs) + ".\n" + str(percent) + "%.")
    if percent == 100:
        print("Perfect!")
    if 100 > percent > 80:
        print("Almost there, keep practising!")
    if 80 > percent > 70:
        print("Not bad, but still some work to be done.")
    if 70 > percent > 50:
        print("You need to revise your notes!")
    if percent < 50:
        print("You are struggling with this topic.")


def runMenu(mode = "", askForMode = True):
    print("~~~~~~~~~~MAIN MENU~~~~~~~~~~")
    print(addNewline("Welcome to AutoQuiz!\nType -m- at any time to return to the main menu.\n\
    Type -q- at any time to quit."))

    # initializing
    set_list = os.listdir(setsDir)
    if set_list[0] == "init.txt":
        set_list = set_list.pop(0)

    if len(set_list) == 0:
        mode = "B"
    elif askForMode:
        mode = input(addNewline("Select: \n(A) Quiz\n(B) Process Notes"))
        print(addNewline("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"))
    elif not askForMode and mode == "":     # default mode: quiz.
        mode = "A"

    if mode in ["a", "A"]:  # QUIZ MODE
        print(addNewline("~~~QUIZ YOURSELF~~~"))
        game_type = input(addNewline("Select Game Mode: \
                  \n(A) Short Answer \n(B) Multiple Choice \nMenu (-m-) \nQuit (-q-)")).strip(' ')
        # (C) Fill in the blanks\n True or False (D)\n(N/A yet) Match the words (E)\n(N/A yet) Tick the Boxes (F)\n \
        # (N/A yet) Custom (G)

        # checking for exit
        if game_type in ["-m-", "-M-"]:
            return runMenu()
        elif game_type in ["-q-", "-Q-"]:
            return None

        print(addNewline("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"))

        # listing the sets you can quiz on:
        sets = os.listdir(setsDir)
        num = 1
        for i in range(len(sets)):
            if sets[i] != '.DS_Store':
                print(str(i+num) + ": " + sets[i])
            else:
                num -= 1

        # asking user to choose sets.
        user_sets = input("Number the sets you'd like to quiz yourself on (seperated by commas): ")
        print(addNewline("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"))

        # checking for exit or return:
        if user_sets.strip(' ') in ["-m-", "-M-"]:
            return runMenu()
        elif user_sets.strip(' ') in ["-q-", "-Q-"]:
            return None

        # preparing the chosen sets:
        user_sets = user_sets.rstrip()
        user_sets = user_sets.split(",")
        setList = []
        for i in range(len(user_sets)):
            setList.append(sets[int(user_sets[i]) - 1])

        # running the chosen game mode:
        if game_type in ["A", "a"]:
            for i in range(len(user_sets)):
                runStatus = runShortAnswer(setsDir + sets[int(user_sets[i]) - 1])
                if runStatus == None:
                    return None  # menu not working.
        elif game_type in ["B", "b"]:
            for i in range(len(user_sets)):
                runStatus = runQuizMC(setsDir + sets[int(user_sets[i]) - 1])
                if runStatus == None:
                    return None
        # elif type in ["C", "c"]:
            # runFillInBlanks(sets)
        # elif type in ["D", "d"]:
            # runTrueFalse(sets)
        # elif type in ["E", "e"]:
            # runMatchWords(sets)
        # elif type in ["F", "f"]:
            # runTickBoxes(sets)
        # elif type in ["G", "g"]:
            # runCustom(sets)
        os.chdir(ogdir)

    elif mode in ["b", "B"]:    # PROCESS MODE
        print("~~~PROCESS YOUR NOTES~~~")
        if len(set_list) == 0:
            print("You have no sets yet!")
        noteDir = input("Please enter the directory of your notes: ")

        # Listing the processable files that exist in given directory
        notes = os.listdir(noteDir)
        j = 1
        for file in notes:
            if ".txt" in file or ".dat" in file:
                print(str(j) + ": " + file)
                j += 1

        # Getting user to select which notes to process
        user_notes = input("Number the notes you'd like to process (seperated by commas): ")

        # exit or return check
        if user_notes in ["-M-", "-m-"]:
            return runMenu()
        elif user_notes in ["-q-", "-Q-"]:
            return None

        # preparing the chosen notes
        user_notes = user_notes.split(", ")
        goToQuiz = False

        # processing all their chosen files:
        for i in range(len(user_notes)):
            processNotes(notes[int(user_notes[i]) - 1], noteDir, goToQuiz)
        # Implement option:
            # | Run this quiz now | Choose a different quiz to run |
        mode = "a"
        askForMode = False
        return runMenu(mode, askForMode)

    # checking for exit
    elif mode in ["-M-", "-m-"]:
        return runMenu()
    elif mode in ["-q-", "-Q-"]:
        return None
    else:
        mode = input(addNewline("Please enter a valid option.\nSelect: \n(A) Quiz\n(N/A yet) (B) Process Notes."))
        return runMenu(mode)
    return runMenu()


runMenu()
