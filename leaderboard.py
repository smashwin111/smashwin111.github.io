

name = input("write your name ")
score = input("What is your score? ")

f = open("demofile2.txt", "r")

#read and split the current txt into its constituent words
words = f.read().split()

counter = 0
#counter will go up if any name already in the list matches the input name
for i in range(len(words)):
    if name == words[i]:
        #if score of existing name beats old score, it is added
        if int(score) > int(words[i+1]):
            words[i+1] = score
        counter = counter + 1

#otherwise the name that was input is appended to the list along with its score
if counter == 0:
    words.append(name)
    words.append(score)

#separating names and scores so we can sort scores and sort names with corresponding indices
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

#rewrite the txt files with the now sorted words list
f = open("demofile2.txt", "w")
for i in range(0, len(words), 2):
    f.write("\n" + str(words[i]) + " " + str(words[i+1]))
f.close()

#read out the new txt file
f = open("demofile2.txt", "r")
print(f.read())



    
