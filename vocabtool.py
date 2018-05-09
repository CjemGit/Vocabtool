#TO DO
#make it so you have to have done it english to italian and italian to english for the score to be boosted
#make it a score rather than a last correct

import pandas as pd
import numpy as np
import datetime
import random


invalid = 'Invalid Option, try again '

articles = ['il', 'la', 'lo', 'le', 'l\'', 'i', 'gli']

targetlang = 'Italian'

vocab = pd.read_csv('itvocab.csv', index_col=0)

mode = input("Choose a mode: \n a : ADD, \n c : CORRECT, \n r : REVISE or \n t : TEST \n")

if mode == 'a':

    no = int(input("How many lines are you going to add? \n"))

    for i in range(no):
        line = []
        ID = len(vocab) + 1
        English = input("What is the English word?")
        Target = input("What is the " + targetlang + ' word?')
        while True:
            Type = input('Is the word a noun or a verb? (Can be \n n: noun \n v: verb \n o: other)')
            if Type == 'n' or \
               Type == 'v' or \
               Type == 'o':
               break
            else: print(invalid)
        if Type == 'n':
            Regular = 'n/a'
            while True:
                Article = input("What is the article? (Determinative, Can be " + str(articles))
                if Article in articles:
                    break
                else: print(invalid)

        elif Type =='v':
            Article = 'n/a'
            while True:
                Regular = input("Is the verb regular? (Can be r, i or na)")
                if Regular == 'r' or \
                   Regular == 'i' or \
                   Regular == 'n/a':
                    break
                else: print(invalid)

        elif Type =='o':
            Article = 'n/a'
            Regular = 'n/a'

        line.append(ID)
        line.append(English)
        line.append(Target)
        line.append(Article)
        line.append(Regular)
        line.append(Type)
        line.append(0)
        line = pd.DataFrame([line], columns=vocab.columns)
        vocab = vocab.append(line, ignore_index=True)
        print('Added ')
        print(line)

    vocab.to_csv('itvocab.csv')

elif mode == 'c':
    while True:
        try:
            cor2 = int(input('What would you like to correct? Give the index '))
            break
        except ValueError:
            print(invalid)
    print(vocab.iloc[cor2-1])

    while True:
        cor = input("What would you like to correct? \n e : English, \n i : " + targetlang + ', \n a : Article ,\n or r : Regular')

        if cor == 'e':

            English = input("What is the English word?")

            vocab.iloc[cor2-1,1] = English

        elif cor =='i':

            Target = input("What is the " + targetlang + "word? ")

            vocab.iloc[cor2-1,2] = Target

        elif cor =='a':

            while True:
                Article = input("What is the article? (Determinative, Can be " + str(articles))
                if Article in articles:
                    break
                else: print(invalid)

            vocab.iloc[cor2-1,3] = Article

            Regular = vocab.iloc[cor2-1,4]

            if Article in articles:
                Type = "Noun"
            elif Regular == 'r' or \
                 Regular == 'i':
                Type = "Verb"
            else:
                 Type = "Other"

            vocab.iloc[cor2-1,5] = Type

        elif cor =='r':

            while True:
                Regular = input("Is the verb regular? (Can be r, i or na)")
                if Regular == 'r' or \
                   Regular == 'i' or \
                   Regular == 'na':
                    break
                else: print(invalid)

            vocab.iloc[cor2-1,4] = Regular

            Article = vocab.iloc[cor2-1,3]

            if Article in articles:
                Type = "Noun"
            elif Regular == 'r' or \
                 Regular == 'i':
                Type = "Verb"
            else:
                 Type = "Other"

            vocab.iloc[cor2-1,5] = Type

        else:
            print(invalid)

        print("Here is your new correct line")
        print(vocab.iloc[cor2-1])
        yn = input("are you happy with this? (Can be y or n) ")
        if yn == 'n':
            print("You made no changes")
            break
        elif yn == 'y':
            vocab.to_csv('itvocab.csv')
            break
        else: print(invalid)


elif mode =='r':

#orders based on LastCorrect and gives 5 lines

    sortedvocab = vocab.sort_values('LastCorrect')
    for i in range(5):
        print(sortedvocab.iloc[i])
        input("Press any key")


elif mode == 't':

    sortedvocab = vocab.sort_values('LastCorrect', ascending=True)

    nocor = 0

    for i in range(5):
        a = random.randint(0,1)
        #1 asks for italian
        if a == 1:
            print(sortedvocab.iloc[i,1])

            test = input("Give the " + targetlang + " ")
            if test == sortedvocab.iloc[i,2]:
                print('CORRECT!!!')
                if sortedvocab.iloc[i,-2] == 'n':
                    article = input("Now give the article ")
                    if article == sortedvocab.iloc[i,3]:
                        print('Also Correct!')
                        nocor = nocor + 1
                        print(nocor)
                        sortedvocab.iloc[i,-1] = datetime.datetime.now().timestamp()

                elif sortedvocab.iloc[i,-2] == 'v':
                    regular = input("Is the verb regular? ")
                    if regular == sortedvocab.iloc[i,-3]:
                        print('Also Correct!')
                        nocor = nocor + 1
                        print(nocor)
                        sortedvocab.iloc[i,-1] = datetime.datetime.now().timestamp()

                if sortedvocab.iloc[i,-2] == 'o':
                    nocor = nocor + 1
                    sortedvocab.iloc[i,-1] = datetime.datetime.now().timestamp()


            else:
                print('Sorry Pal, you need to revise')


        if a == 0:
            print(sortedvocab.iloc[i,2])
            test = input("Give the English ")
            if test == sortedvocab.iloc[i,1]:
                print('CORRECT!!!')
                nocor = nocor + 1
                print(nocor)
                sortedvocab.iloc[i,-1] = datetime.datetime.now().timestamp()
            else:
                print('Sorry Pal')
    print("You scored " + str(float(nocor/5)*100) + '%')

    sortedvocab.to_csv('itvocab.csv')

else:
    print(invalid)
