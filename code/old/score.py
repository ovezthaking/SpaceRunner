
with open('score.txt', 'r+') as scorefile:
    scorepart = int(scorefile.read())
with open('totalscore.txt', 'r+') as totalscorefileread:
                    
    totalscore = int(totalscorefileread.read())
                   
with open('totalscore.txt', 'w') as totalscorefile:

    totalscorefile.write(str(totalscore + scorepart))  