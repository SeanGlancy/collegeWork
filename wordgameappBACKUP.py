from flask import Flask, render_template, url_for, request, redirect,flash,session
import random,time,datetime



app=Flask(__name__)



def displayWords():#get the words with seven or more letters
    
    allWords="macList.txt"
    testcount=0
    with open (allWords) as words:
        lines=words.readlines()
        with open('displayWords.txt','a') as log:
            for x in lines:
                if len(x)>7:
                     x2 = x.replace("\n", "")
                     print(x2.lower(),file=log)
                     testcount=testcount+1
            print("7 letters+ count was ",testcount)
            validWords()
            return(lines)
            
def validWords():#create a list of words with between 3 and 7 characters

    allWords='macList.txt'

    testcount=0
    with open (allWords) as words:
        lines=words.readlines()
        lines = [l.strip() for l in lines]
        with open('validWords.txt','a') as log:
            for x in lines:
                if len(x)>=3 and len(x)<7:
                 print(x.lower(),file=log)
                 testcount=testcount+1
        print('number of valid words ', testcount)
           

@app.route("/")
def display_home():
    return render_template("home.html",
                           title="The word game",
                           game_url=url_for("display_game"),
                           leaderBoard_url=url_for("display_score")
                           )

@app.route('/game')
def display_game():
    #generate random word
     session['start']=datetime.datetime.utcnow()
     lines=displayWords()
     lines = [l.strip() for l in lines]
     session['randWord']=random.choice(lines)
     start=time.strftime('%X ')

     return render_template('game.html', 
                           title='The word game',
                           word=session['randWord'],
                           time=start,
                           home_url=url_for('display_home'),
                           leaderBoard_url=url_for('display_score'),
                           save_words=url_for('saveForm')
                           )

@app.route('/save', methods=['POST'])
def saveForm():
    
    session['endtime']=str(datetime.datetime.utcnow() - session['start'])
    inputList=[]
    inputList.append(request.form['word0'])
    inputList.append(request.form['word1'])
    inputList.append(request.form['word2'])
    inputList.append(request.form['word3'])
    inputList.append(request.form['word4'])
    inputList.append(request.form['word5'])
    inputList.append(request.form['word6'])
    
    valid(inputList)
    #print(inputList)

    # call vaild function
    return render_template('valid.html',
                           theWords=wordList,
                           title='Yours words were',
                           gametime=session['endtime'],
                           game_url=url_for('display_game'),
                           home_url=url_for('display_home')
                           )

@app.route('/score')
def display_score():
    return render_template('score.html',
                           title='the high scores',
                           game_url=url_for('display_game'),
                           home_url=url_for('display_home')
                           )

def valid(inputList):

    allWords='validWords.txt'
    with open (allWords) as words:
        lines=words.readlines()
        lines = [l.strip() for l in lines]
        #set dictionary
      
        allgood='true'
        random= session['randWord']
        
        while userwords in inputList and allgood =='true':
            
            if userwords in lines:  #check if word is in dictionary  
                if inputList.count(userwords) >1: #count the number of times the user word appears in the wordlist
                    print("word already entered")
                    allgood='false'
                    if random == userwords:  # check if word is 
                           print("same word")
                           allgood='false'
                else:
                     length=len(userwords)
                     tempList=[]
                     for y in random:
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


app.config['SECRET_KEY'] = 'thisismyultimatesecretkeyofdoom'
app.run(debug=True)
