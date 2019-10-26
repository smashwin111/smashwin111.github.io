

name = input("write your name ")
score = input("What is your score? ")

f = open("demofile2.txt", "r")

words = f.read().split()

counter = 0

for i in range(len(words)):
    if name == words[i]:
        if int(score) > int(words[i+1]):
            words[i+1] = score
        counter = counter + 1

if counter == 0:
    words.append(name)
    words.append(score)

names = []
scores = []

for i in range(0,len(words),2):
    names.append(words[i])

for i in range(1,len(words),2):
    scores.append(int(words[i]))

#print(names)
#print(scores)

words = []
while len(scores) > 0:
    topscore = max(scores)
    index = scores.index(topscore)
    #print(index)
    words.append(names[index])
    words.append(topscore)
    scores.pop(index)
    names.pop(index)

f = open("demofile2.txt", "w")
for i in range(0, len(words), 2):
    f.write("\n" + str(words[i]) + " " + str(words[i+1]))
f.close()

f = open("demofile2.txt", "r")
print(f.read())



    
