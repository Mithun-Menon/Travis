#add a way to show the features
import pyttsx3
import datetime
import speech_recognition as sr
import webbrowser
import wikipedia
import os
import sys
import mysql.connector
import smtplib
from email.message import EmailMessage


#voice engine
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice',voices[0].id)


def speak(audio):
    engine.say(audio)
    engine.runAndWait()

# To wish according to the time of the day
def wish():
# To wish according to the time of the day
    hour = int(datetime.datetime.now().hour)
    if hour > 0 and hour < 12:
        print('Good Morning')
        speak('Good Morning!')
    elif hour >= 12 and hour < 17:
        print('Good Afternoon')
        speak('Good Afternoon')
    elif hour >= 17:
        print('Good Evening')
        speak('Good Evening!')



def takecommand():
# To input voice and convert it into string
    r = sr.Recognizer()
    with sr.Microphone() as source:                   #using default microphone
        print("Listening...")
        audio = r.listen(source)

    try:
        print('Recogonizing...')

        com =r.recognize_google(audio,language='en-in')                #converts the voice input to a string
        print(f"User said: {com}\n")

    except Exception as e:
        print('Say that again...')
        return 'none'
    return com


def add_email():
    try:
        #connects the mysql database to python
        connection = mysql.connector.connect(host='localhost',database='emailid',user='Mithun',password='mithun')
        cursor = connection.cursor()

        # values for the record
        name = (input('Enter name:'))
        emailid = (input('Enter emailid:'))

        # instead of inputting the serial number,the existing highest value of serial number will be added by 1
        sno = 'select max(sno) from emailid'
        cursor.execute(sno)
        osno = cursor.fetchone()

        for i in osno:
            nsno = int(i) + 1



    except mysql.connector.errors.InterfaceError:
        print('Make sure SQL is running or contact the admin'),speak('Make sure S Q L is running..or contact the admin')
        sys.exit()

    # to add the new record
    query = f'insert into emailid (sno,name,id) values({nsno},"{name}","{emailid}")'
    cursor.execute(query)
    connection.commit()

    cursor.close()
    connection.close()
    print('EMAIL ID ADDED SUCCESSFULLY!!!')


def send_mail():
    fromid = 'mithun.test.email@gmail.com'

    f = open('pass.txt', 'r')
    password = f.read()

    sub = input('Enter the subject of your email:')
    content = input('Enter your message:')

    msg = EmailMessage()
    msg['Subject'] = sub
    msg['From'] = fromid
    msg['To'] = rec
    msg.set_content(content)

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(fromid, password)
        smtp.send_message(msg)

    print('EMAIL SENT SUCCESSFULLY!!!'), speak('EMAIL SENT SUCCESSFULLY!!!')


if __name__ == '__main__':
    wish()
    speak(" I'm travis... How may i help you?")

    while True:

        com = takecommand().lower()

        if 'wikipedia' in com:
            speak('Searching Wikipedia...')
            com = com.replace("wikipedia", "")
            answer = wikipedia.summary(com, sentences=2)

            print('According to Wikipedia:'), speak('According to Wikipedia:')
            print(answer), speak(answer)



        elif 'open youtube' in com:
            webbrowser.open('youtube.com')

        elif 'open google' in com:
            webbrowser.open('google.com')

        elif 'open spotify' in com:
            webbrowser.open('spotify.com/qa-en/')



        elif 'the time' in com or 'what is the time' in com:
            time = datetime.datetime.now().strftime('%H:%M:%S')
            speak(f'The time is {time}')

        elif 'add email id' in com or 'add email address' in com or 'add email' in com:
            add_email()

        elif 'send email' in com:
            print('Do you have the Email ID saved? (Say YES or NO) :')
            speak('Do you have the Email ID saved?')


            com = takecommand().lower()
            if 'yes' in com:
                pass

            elif 'no' in com:
                add_email()
                break




            try:
                connection = mysql.connector.connect(host='localhost', database='emailid', user='Mithun', password='mithun')

                table = 'select * from emailid'
                cursor = connection.cursor()
                cursor.execute(table)
                records = cursor.fetchall()
                for row in records:
                    print(row)

                l =input('Enter name of contact:')
                select_query = f"select id from emailid where name='{l.lower()}'"
                cursor.execute(select_query)
                id = cursor.fetchall()
                for row in id:
                    rec = row

            except mysql.connector.errors.InterfaceError:
                print('Please make sure SQL is running or contact the admin'), speak('Please make sure S Q L is running....or contact the admin')
                sys.exit()



            connection.close()
            send_mail()


        elif 'search for' in com or 'what' in com or 'when' in com or 'how' in com or 'why' in com or 'are' in com or 'who' in com and 'what is the time' != com and 'quit' != com:
            com1=''
            keywords= ['search for', 'what is', 'what are', 'when is', 'when are', 'how is', 'how are', 'why is',
                       'why are','who is','who are']

            for i in range(11):
                if keywords[i] in com:
                    n=keywords[i]
                    com1 = com.strip(n)
            com=com.replace(' ','+')

            webbrowser.open(f'https://google.com/search?#q={com}')
            print(f'Searching for {com1} on google...'), speak(f'Searching for {com1} on google...')




        elif 'quit' in com:
            print('Thank You...Bye')
            speak('Thank You...Bye')
            sys.exit()