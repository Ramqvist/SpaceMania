import pickle

__author__ = 'Erik'

#Class for handling the highscores.
class HighscoreHandler:

    def __init__(self):
        pass

    #Insert one score at the correct position and save it to disk. Returns the inserted position.
    def insertHighscore(self, newScore, playerName):
        scoreList = self.getHighscoreList()
        counter = 1
        for (score, name) in scoreList:
            if int(newScore) > int(score):
                scoreList.insert(counter, ("\n" + str(newScore), playerName + "\n"))
                if len(scoreList) > 10:
                    scoreList.pop(10)
                self.dumpHighscoreList(scoreList)
                return counter
            counter += 1
        if len(scoreList) < 10:
            scoreList.append(("\n" + str(newScore), playerName))
        self.dumpHighscoreList(scoreList)
        return counter

    #Returns true if the score can be in the top 10 best score, otherwise returns false.
    def canScoreBeInserted(self, newScore):
        scoreList = self.getHighscoreList()
        if(len(scoreList) < 10):
            return True
        for (score, name) in scoreList:
            if int(newScore) > int(score):
                return True
        return False

    #Gets the highscore list as a pair of (score, name)
    def getHighscoreList(self):
        resultList = []
        file = open('Highscores.txt', 'r')
        for line in file:
            print line
            splittedList = line.split(":", 1)
            if len(splittedList) == 2:
                resultList.append((splittedList[0], splittedList[1]))
        file.close()
        return resultList

    #Prints the given highscorelist to the disk.
    def dumpHighscoreList(self, highscoreList):
        file = open('Highscores.txt', 'w+')
        for (score, name) in highscoreList:
            file.write(str(score) + ":" + name)
            print "Dumping score name: " + name
        file.close()
