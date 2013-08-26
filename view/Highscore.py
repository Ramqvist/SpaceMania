import pickle

__author__ = 'Erik'


class HighscoreHandler:

    def __init__(self):
        pass


    def getHighscoreFile(self):
        return open('Highscores.txt', 'w')


    def getHighscoreList(self):
        resultList = []
        file = self.getHighscoreFile()
        for line in file:
            splittedList = line.split(":", 1)
            resultList.append((splittedList[0], splittedList[1]))
        file.close()
        return resultList

    def dumpHighscoreList(self, highscoreList):
        file = self.getHighscoreFile()
        for (score, name) in highscoreList:
            file.write(score + ":" + name + "\n")
        file.close()
