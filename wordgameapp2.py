from flask import Flask, render_template, url_for, request, redirect,flash,session
import random,time,datetime,pickle
import sys
import logging


app=Flask(__name__)

if __name__ == "__main__":
    app.run(debug=True)

    
app.logger.addHandler(logging.StreamHandler(sys.stdout))
app.logger.setLevel(logging.ERROR)
def displayWords():  #get the words with seven or more letters
    
    allWords="macList.txt"
    testcount=0
    with open (allWords) as words:
        lines=words.readlines()
        with open('displayWords.txt','a') as log:  #open the file as a log
            for x in lines:
                if len(x)>8:                        #if the length of the word is 7 chars or greater
                     x2 = x.replace("\n", "")
                     print(x2.lower(),file=log)     #print it to the text file
                     testcount=testcount+1
            print("7 letters count was ",testcount)
            #validWords()
            print("end of displayWords")
            return(lines)
            
def validWords():#create a list of words with over 3 characters

    allWords='macList.txt'

    testcount=0
    with open (allWords) as words:
        lines=words.readlines()
        lines = [l.strip() for l in lines]
        with open('validWords.txt','a') as log:
            for x in lines:
                if len(x)>=3 :                  #create a text file that has words with over 3 letters
                 print(x.lower(),file=log)
                 testcount=testcount+1
        print('number of valid words ', testcount)
           

@app.route("/")
def display_home():     #home page
    return render_template("home.html",
                           title="The word game",
                           game_url=url_for("display_game"),
                           leaderBoard_url=url_for("display_score")
                           )

@app.route('/game')
def display_game():
    #generate random word
     session['start']=datetime.datetime.utcnow()#start the timer
     lines=displayWords()
     lines = [l.strip() for l in lines]
     print("game1")
     session['randWord']=random.choice(lines)

     return render_template('game.html', 
                           title='The word game',
                           word=session['randWord'],
                           time=session['start'],
                           home_url=url_for('display_home'),
                           leaderBoard_url=url_for('display_score'),
                           save_words=url_for('saveForm')
                           )
def score(user): # create a log with the time to finish the game + the users name
    with open('score.txt', 'a') as log:
         print(session['endtime'],'|',user,file=log)       
                   

@app.route('/save', methods=['POST'])
def saveForm():
    name= True
    print("save 1")
    if request.form['user_name'] == '':
        name= False
        flash("Sorry. You must tell me your name. Try again")  #ensure that the user has entered a name
    print('save2')
    session['endtime']=str(datetime.datetime.utcnow() - session['start']) #work out the time taken
    inputList=[]
    inputList.append(request.form['word0'])
    inputList.append(request.form['word1'])
    inputList.append(request.form['word2'])
    inputList.append(request.form['word3'])
    inputList.append(request.form['word4'])
    inputList.append(request.form['word5'])
    inputList.append(request.form['word6']) #get each of the words from the text boxes
    #validate words
    print("save3")
    allWords='validWords.txt'
    with open (allWords) as words:
        print("save4")
        lines=words.readlines()
        lines = [l.strip() for l in lines]
        print("save5")
        invalList=[]
        allgood='true'
        
        print("save form 1")
        for userwords in inputList:
            print("save form loop")
            if allgood:
                if userwords in lines:  #check if word is in dictionary  
                    if inputList.count(userwords) >1: #count the number of times the user word appears in the wordlist
                        print("word already entered")
                        allgood='false'
                        invalList.append(userwords)
                        if session['randWord'] == userwords:  # check if word is the source word 
                               print("same word")
                               allgood='false'
                               invalList.append(userwords)
                    else:
                         length=len(userwords)
                         tempList=[]
                         for y in session['randWord']:
                               tempList.append(y)
                        
                         for y in userwords:
                             for z in tempList:
                                   if y == z:
                                       tempList.remove(z)
                                       length-=1
                                       break
                                    
                         if length == 0: 
                             print("Your word is valid")
                             allgood='true'
                else:
                     print("Not Valid")
                     allgood='false'
                     invalList.append(userwords)
    
    if name == True: #if the name was entered
        if allgood=='true':
            score(request.form['user_name'])
            x=0
            tempL=[]
            with open ('score.txt') as words:   #open the score text file
                lines=words.readlines()
                tempL=sorted(lines,key=getKey)  #sort the text file
                #print(tempL)
            while x <=9:
                flash(tempL[x]) #display the first 10
                x+=1
            return render_template('valid.html',
                                   
                                   theWords=inputList,
                                   title='Congratulations, ',
                                   gametime=session['endtime'],
                                   game_url=url_for('display_game'),
                                   home_url=url_for('display_home')
                                   
                                   )
        else:
            return render_template('gameOver.html',
                                   theWords=invalList,
                                   title='unlucky',
                                   gametime=session['endtime'],
                                   game_url=url_for('display_game'),
                                   home_url=url_for('display_home')
                                   )
    else:
        return redirect(url_for("display_game"))    

@app.route('/score')
def display_score():
    #leaderboard page, display the first ten
       
    x=0
    tempL=[]
    with open ('score.txt') as words:   
        lines=words.readlines()
        tempL=sorted(lines,key=getKey)
        print(tempL)
    while x <=9:
        flash(tempL[x])
        x+=1
    return render_template('score.html',
                           title='the high scores',
                           home_url=url_for('display_home')
                           )

def getKey(item): # used to sort on the first item
    return item[0]

app.config['SECRET_KEY'] = 'thisismyultimatesecretkeyofdoinvalListom'

