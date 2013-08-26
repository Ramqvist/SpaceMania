import pickle

__author__ = 'Erik'


class HighscoreHandler:

    def __init__(self):
        pass

    

    def canScoreBeInserted(self, newScore):
        scoreList = self.getHighscoreList()
        if(len(scoreList) < 10):
            return True
        for (score, name) in scoreList:
            if newScore > score:
                return True
        return False


    def getHighscoreList(self):
        resultList = []
        file = open('Highscores.txt', 'r')
        for line in file:
            print line
            splittedList = line.split(":", 1)
            resultList.append((splittedList[0], splittedList[1]))
        file.close()
        return resultList

    def dumpHighscoreList(self, highscoreList):
        file = open('Highscores.txt', 'w+')
        for (score, name) in highscoreList:
            file.write(score + ":" + name)
        file.close()
