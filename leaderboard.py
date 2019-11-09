
def leaderboard(name, score, fileName):

    f = open(fileName, "r")

    #read and split the current txt file into its constituent words
    words = f.read().split()

    #check if name inputted by user is already in the txt file
    i = 0
    found = False
    while i < len(words) and found==False:
        if name == words[i]:
            #if so, update his/her high score if it is higher than previous high score
            if int(score) > int(words[i+1]):
                words[i+1] = score
                found = True
        i = i + 1

    #otherwise, add name to list along with score
    if found==False:
        words.append(name)
        words.append(score)

    #separate names and scores so we can sort scores and order names accordingly
    names = []
    scores = []

    for i in range(0,len(words),2):
        names.append(words[i])

    for i in range(1,len(words),2):
        scores.append(int(words[i]))

    #print(names)
    #print(scores)

    #repopulating the words list with the names/scores in order from greatest to least
    words = []
    while len(scores) > 0:
        topscore = max(scores)
        index = scores.index(topscore)
        #print(index)
        words.append(names[index])
        words.append(topscore)
        scores.pop(index)
        names.pop(index)

    #rewrite the txt file with the now sorted words list
    f = open(fileName, "w")
    for i in range(0, len(words), 2):
        f.write("\n" + str(words[i]) + " " + str(words[i+1]))
    f.close()

    #read out the new txt file
    f = open(fileName, "r")
    print(f.read())






    
