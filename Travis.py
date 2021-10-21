from tkinter import *
from tkinter import messagebox
import tkHyperlinkManager
from bs4 import BeautifulSoup as soup
import cv2
from urllib.request import urlopen
import pyttsx3
import datetime
import mysql.connector
import speech_recognition as sr
from email.message import EmailMessage
import wikipedia
import webbrowser
import os
import random
import smtplib



engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

window = Tk()
window.geometry('500x650')


global var
global var1
var = StringVar()
var1 = StringVar()

#values in list for general intelligence
greetings=['hi','how are you','hello','hey']
r_greetings=['hi','hello','hey']

state=['how are you doing','how’s it going','how’s everything','how are things']
r_state=['I am good',"Everything's well","Everything is well",'All good now']

thanks=["thanks", "thank you", "that's helpful"]
r_thanks=["Happy to help!", "Any time!",'My pleasure']

age=['how old are you',"what's your age",'what is your age']
r_age=['I am barely an year old',"I'm not too old...but I'm smart tho"]

creator=['who is your creator',"who's your creator",'who made you']
r_creator=['I was created by Mithun Menon','the one and only.....Mithun Menon','Mithun Menon','My creator is Mithun Menon']

keywords= ['search for ', 'what is ', 'what are ', 'when is ', 'when are ', 'how is ', 'how are ', 'why is ',
                       'why are ','who is ','who are ']



"""                 The function initializes pyttsx3
    The parameter audio can be replaced with a string so that it can be converted into audio """
def speak(audio):
    engine.say(audio)
    engine.runAndWait()


"""The function decides whether to say morning,afternoon or evening while wishing 
    in the initial stage of run. Datetime module is used within the function to determine 
    the exact time in the day"""
def wish():
    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour <= 12:
        var.set("Good Morning")
        window.update()
        speak("Good Morning!")
    elif hour >= 12 and hour <17:
        var.set("Good Afternoon!")
        window.update()
        speak("Good Afternoon!")
    else:
        var.set("Good Evening")
        window.update()
        speak("Good Evening !")
    speak(" I'm travis... How may i help you?")



"""The function use the module 'speech_recognition'. 
    It receives the user's spoken command as audio and converts it into a string """
def takeCommand():
    global com
    r = sr.Recognizer()
    with sr.Microphone() as source:
        var.set("Listening...")
        window.update()



        r.energy_threshold = 350        #variables set to tune the incoming audio
        audio = r.listen(source)

    try:
        var.set("Recognizing...")
        window.update()
        # print("Recognizing")
        com= r.recognize_google(audio, language='en-in')    #uses google's voice recognition api
        var1.set(com)                                       #for understanding the audio file
        window.update()
    except Exception as e:
        print(e)
        # return "None"


    return com



"""The function use the module 'mysql.connector'. 
    It receives data from the user and adds it into an sql table used for the storing 
      contact details for later uses."""
def add_email():
    try:
        #connects the mysql database to python
        connection = mysql.connector.connect(host='localhost',database='emailid',user='Mithun',password='mithun')
        cursor = connection.cursor()

        #tkinter code for a window to add the new contact
        w_add_email = Tk()
        w_add_email.geometry('250x200')
        w_add_email.title('Email Credentials')

        name_label = Label(w_add_email, text='Enter Name:').grid(row=1, column=1)
        email_label = Label(w_add_email, text='Enter Email ID:').grid(row=3, column=1)
        name_entry = Entry(w_add_email)
        name_entry.grid(row=2, column=2)
        email_entry = Entry(w_add_email)
        email_entry.grid(row=4, column=2)

        #function that will activate when the 'Done' button is clicked.It retrieves the values
        # from the window and adds to the sql table
        def done():
            name = name_entry.get()
            email = email_entry.get()

            sno = 'select max(sno) from emailid'
            cursor.execute(sno)
            osno = cursor.fetchone()

            for i in osno:
                nsno = int(i) + 1

            # instead of inputting the serial number,the existing highest value of serial number will be added by 1
            sno = 'select max(sno) from emailid'
            cursor.execute(sno)
            osno = cursor.fetchone()

            for i in osno:
                nsno = int(i) + 1

            query = f'insert into emailid (sno,name,id) values({nsno},"{name}","{email}")'
            cursor.execute(query)
            connection.commit()

            cursor.close()
            connection.close()
            var.set('EMAIL ID ADDED SUCCESSFULLY!!!')
            window.update()
            exit()

        butn_done = Button(w_add_email, text='Done', command=done).grid(row=7, column=35)

    #incase an error occurs it will the particular function again
    except mysql.connector.errors.InterfaceError:
        var.set('Make sure SQL is running or contact the admin')
        speak('Make sure S Q L is running..or contact the admin')
        window.update()
        sys.exit()



"""The function uses 'tkinter' module for a window to type down the mail with subject 
    and uses 'smtplib' module to send the mail """
def send_mail(rec):
    fromid = 'mithun.test.email@gmail.com'      #username

    with open('pass.txt', 'r') as f:            #password is being read from a
        password = f.read()                     #text file for security


    # tkinter code for creation of the window to type down the mail
    w_send_mail = Tk()
    w_send_mail.geometry('400x400')
    w_send_mail.title('Mail')

    frame1 = Frame(w_send_mail, height=100)
    frame2 = Frame(w_send_mail, height=100)
    frame3 = Frame(w_send_mail, height=100)
    frame4 = Frame(w_send_mail, height=100)

    frame1.pack(side=TOP, anchor='w')
    frame2.pack(side=TOP, anchor='w')
    frame3.pack(side=TOP, anchor='w')
    frame4.pack(side=TOP, anchor='w')

    l_from = Label(frame1, text='From:', anchor='w', font='Helvetica 10 bold').pack(fill=X)
    l_to = Label(frame2, text='To:', anchor='w', font='Helvetica 10 bold').pack(fill=X)
    l_sub = Label(frame3, text='Subject:', anchor='w', font='Helvetica 10 bold').pack(fill=X)
    l_content = Label(frame4, text='Content:', anchor='w', font='Helvetica 10 bold').pack(fill=X)

    e_from = Entry(frame1, width=30)
    e_from.insert(0, 'mithun.test.email@gmail.com')
    e_from.config(state=DISABLED)
    e_from.pack(fill=X, padx=10)


    e_to = Entry(frame2, width=30)
    e_to.insert(0, rec)
    e_to.config(state=DISABLED)
    e_to.pack(fill=X, padx=10)
    e_subject = Entry(frame3, width=30)
    e_subject.pack(fill=X, padx=10)

    scrollbar = Scrollbar(frame4)
    scrollbar.pack(side=RIGHT, fill=Y)
    t_content = Text(frame4, height=10, width=40, yscrollcommand=scrollbar.set)
    scrollbar.configure(command=t_content.yview)
    t_content.pack(fill=BOTH, padx=10)

    #this function initializes and directly uses smptlib to send the mail after the data is retrieved
    def send():
        try:
            sub = e_subject.get()
            content = t_content.get('1.0', 'end')
            w_send_mail.withdraw()

            msg = EmailMessage()
            msg['Subject'] = sub
            msg['From'] = fromid
            msg['To'] = rec
            msg.set_content(content)

            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                smtp.login(fromid, password)

                smtp.send_message(msg)

            var.set('EMAIL SENT SUCCESSFULLY!!!'), speak('EMAIL SENT SUCCESSFULLY!!!')
            return print('done')

        except smtplib.SMTPServerDisconnected:
            var.set('Server has been disconnected!\nTravis will restart now')
            window.destroy()
            play()
        except smtplib.SMTPDataError:
            var.set('Data enter is invalid...Please try again')
            send_mail(rec)


    b_send = Button(frame4, text='Send', command=send).pack()







"""The main function that runs the program in which rest of the functions are called in.
 The function gets activated when the play button is clicked in the gui"""

def play():
    #btn2['state'] = 'disabled'
    # btn0['state'] = 'disabled'
    global com
    btn1.configure(bg='orange')
    wish()
    while True:
        com = takeCommand().lower()
        btn1.configure(bg='orange')

        if 'quit' in com:
            var.set("Bye sir")
            window.update()
            btn1.configure(bg='#5C85FB')
            btn2['state'] = 'normal'
            # btn0['state'] = 'normal'
            speak("Bye sir")


            window.quit()
            break

        #code for commands containing the use of wikipedia or opening of it
        elif 'wikipedia' in com:
            if 'open wikipedia' in com:
                webbrowser.open('wikipedia.com')
            else:
                #it reads out 2 lines from he wikipedia search about the topic
                # searched and displays it in a window
                try:
                    w_wiki=Tk()
                    w_wiki.title('Result')
                    # w_wiki.geometry('300x200')
                    speak('Searching Wikipedia...')
                    com = com.replace("wikipedia", "")
                    for i in keywords:
                        if i in com:
                            com1=com.strip(i)
                    answer = wikipedia.summary(com1, sentences=2)



                except Exception as e:
                    var.set('sorry,could not find any results')
                    window.update()
                    speak('sorry...sir could not find any results')
                    break

                finally:
                    l_wiki = Label(w_wiki, text=answer)
                    l_wiki.pack()
                    # var.set(answer)

                    window.update()
                    speak("According to wikipedia")
                    speak(answer)
                    w_wiki.mainloop()


        # code for commands containing the opening of youtube
        elif 'open youtube' in com:
            var.set('opening Youtube')
            window.update()
            speak('opening Youtube')
            webbrowser.open("youtube.com")
            com=''


        # code for commands containing the opening of google
        elif 'open google' in com:
            var.set('opening google')
            window.update()
            speak('opening google')
            webbrowser.open("google.com")
            com=''


        # code for commands containing the opening of stakoverflow
        elif 'open stackoverflow' in com :
            var.set('opening stackoverflow')
            window.update()
            speak('opening stackoverflow')
            webbrowser.open('stackoverflow.com')
            com=''


        # code for commands containing the opening of spotify-a music streaming platform
        elif 'open spotify' in com:
            var.set('Opening Spotify')
            window.update()


            webbrowser.open('spotify.com/qa-en/')
            speak('Opening Spotify')
            com=''


        # code for commands containing the request for time
        elif 'the time' in com:
            strtime = datetime.datetime.now().strftime("%H:%M:%S")
            var.set("The time is %s" % strtime)
            window.update()
            speak("The time is %s" % strtime)
            com = ''


        # code for commands containing the request for date
        elif 'the date' in com:
            strdate = datetime.datetime.today().strftime("%d %m %y")
            var.set("Today's date is %s" % strdate)
            window.update()
            speak("Today's date is %s" % strdate)
            com = ''


        # code for commands containing the request to open pycharm
        elif 'open pycharm' in com:

            var.set("Opening Pycharm")
            window.update()
            speak("Opening Pycharm")
            path = 'C:\\Users\\mithu\\AppData\\Local\\PyCharm Community Edition 2020.1\\bin\\pycharm64.exe'
            os.startfile(path)
            com=''


        # code for commands containing the request to open chrome
        elif 'open chrome' in com or 'open google chrome' in com:
            var.set("Opening Google Chrome")
            window.update()
            speak("Opening Google Chrome")
            path = 'C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe'
            os.startfile(path)
            com.replace(com, '')


        # code for commands containing the request to send mail
        elif 'send mail' in com or 'send email' in com:
            com.replace(com, '')
            w_send_mail = Tk()
            w_send_mail.title('Test')
            w_send_mail.eval(f'tk::PlaceWindow {w_send_mail.winfo_toplevel()} center')
            w_send_mail.withdraw()

            msg = messagebox.askyesno('', 'Do u have the EmailID saved?')

            if msg == True:
                pass
            elif msg == False:
                add_email()


            connection = mysql.connector.connect(host='localhost', database='emailid', user='Mithun',
                                                 password='mithun')
            try:
                def enterName():
                    l = e_email_id.get()
                    w_send_mail.quit()
                    select_query = f"select id from emailid where sno={l}"
                    cursor.execute(select_query)
                    id = cursor.fetchall()
                    for row in id:
                        rec = row
                        send_mail(rec)
                        com=''


                w_send_mail = Tk()
                w_send_mail.geometry('400x400')
                w_send_mail.title('Contacts')




                table = 'select * from emailid'
                cursor = connection.cursor()
                cursor.execute(table)
                records = cursor.fetchall()

                lab1 = Label(w_send_mail, text='Index\t    Name\t\tID', font=('Helvetica 15 bold'))
                lab1.pack(anchor='w')
                for row in records:
                    t = '        ' + str(row[0]) + '\t\t        ' + row[1] + '\t     ' + row[2]

                    lab2 = Label(w_send_mail, text=t, anchor='w')
                    lab2.pack(fill=X)
                lab2 = Label(w_send_mail, text='\n', anchor='w')
                lab2.pack(fill=X)

                e_email_id = Entry(w_send_mail)
                b_ok = Button(w_send_mail, text='Done', command=enterName)
                l_email_id = Label(w_send_mail, text="Enter contact's index no.:", anchor='w')

                # e_email_id.pack(side='left',anchor='s',padx=5,pady=5)
                # b_ok.pack(side='left',anchor='s',pady=5)
                l_email_id.pack(anchor='nw', side='left')
                e_email_id.pack(anchor='nw', side='left', padx=5)
                b_ok.pack(anchor='nw', side='left', padx=5)
                com=''
                w_send_mail.mainloop()

            except mysql.connector.errors.InterfaceError:
                print('Please make sure SQL is running or contact the admin'), speak(
                    'Please make sure S Q L is running....or contact the admin')
                sys.exit()

            connection.close()


        # code for commands containing the request to take a picture
        elif 'click photo' in com or 'click picture' in com or 'take a photo' in com or 'take a pic' in com or \
                'take a picture' in com or 'click a picture' in com or 'click a photo' in com :


            cam = cv2.VideoCapture(0)

            count = 0
            m=True
            while m:
                ret, img = cam.read()

                cv2.imshow("'SPACE' to CAPTURE___'ESC' to END", img)

                if not ret:
                    break

                k = cv2.waitKey(1)

                if k % 256 == 27:
                    # For Esc key
                    print("Close")
                    m=False
                    cv2.destroyAllWindows()
                elif k % 256 == 32:
                    # For Space key

                    print("Image " + str(count) + "saved")
                    file = 'G:\\Projects\\Travis\\pics\\' + str(count) + '.jpg'
                    cv2.imwrite(file, img)
                    count += 1
            com=''
            cam.release()



        # code for commands containing the request to record a video
        elif 'record video' in com or 'record a video' in com:
            cap = cv2.VideoCapture(0)
            out = cv2.VideoWriter('vid.mp4', -1, 20.0, (640, 480))
            com = takeCommand().lower()
            while (cap.isOpened()):
                ret, frame = cap.read()
                if ret:

                    out.write(frame)

                    cv2.imshow('frame', frame)
                    if cv2.waitKey(1) & 0xFF == ord('0'):
                        break
                else:
                    break
            cap.release()
            out.release()
            cv2.destroyAllWindows()
            com = ''


        # code for commands containing the request to know the news
        #Uses urllib and tkHyperlinkManager for thee working with tkinter for gui
        elif 'news' in com or "what is today's news" in com or "what's today's news" in com or "today's news" in com or "show news" in com:
            url = 'https://news.google.com/rss/search?q=India&hl=en-GB&gl=GB&ceid=GB%3Aen'

            Client = urlopen(url)
            xml_page = Client.read()
            Client.close()

            soup_page = soup(xml_page, 'xml')
            news_list = soup_page.findAll('item')

            w_news = Tk()
            w_news.title('News')
            w_news.geometry('700x700')
            f_heading = Frame(w_news)
            f_news = Frame(w_news)
            f_heading.pack()
            f_news.pack()

            strtime = datetime.datetime.now().strftime("%H:%M")
            strdate = datetime.datetime.today().strftime("%d %m %y")
            strdate = strdate.replace(' ', '-') + '\t\t\t\t'
            l_date = Label(f_heading, text=strdate, font='Helvetica 11')
            l_title = Label(f_heading, text='News\t\t\t', font='Helvetica 16 bold')
            l_time = Label(f_heading, text=strtime, font='Helvetica 11')

            l_date.grid(row=1, column=1)
            l_title.grid(row=1, column=2)
            l_time.grid(row=1, column=3)

            scrollbar = Scrollbar(f_news)
            scrollbar.pack(side=RIGHT, fill=Y)
            t_news = Text(f_news, height=38, width=80, yscrollcommand=scrollbar.set)

            def clickLink(link):
                webbrowser.open(link)

                return

            hyperlink = tkHyperlinkManager.HyperlinkManager(t_news)

            c = 0
            for news in news_list:
                c += 1

                # report=++
                t_news.insert(END, (news.title.text + '\n\n'))
                # t_news.insert(END, news.link.text)
                t_news.insert(END, news.link.text, hyperlink.add(lambda: clickLink(news.link.text)))

                t_news.insert(END, ('\n' + news.pubDate.text + '\n' + ('-' * 60) + '\n'))
                t_news.pack(pady=20)
                if c == 50:
                    break

            scrollbar.configure(command=t_news.yview)
            t_news.config(state=DISABLED)
            w_news.mainloop()


        # replies for general intelligence based questions using random fuction
        elif 'thank you' in com:
            var.set("Welcome Sir")
            window.update()
            speak("Welcome Sir")
            com = ''

        elif com in thanks:
            response = random.choice(r_thanks)
            var.set(response)
            window.update()
            speak(response)
            com = ''

        elif com in age:
            response = random.choice(r_age)
            var.set(response)
            window.update()
            speak(response)
            com = ''

        elif com in creator:

            response = random.choice(r_creator)
            var.set(response)
            window.update()
            speak(response)
            com = ''

        elif com in greetings:
            response = random.choice(r_greetings)
            var.set(response)
            window.update()
            speak(response)
            com = ''


        #code for commands containing the request for searching queries on google
        elif 'search for' in com or 'what' in com or 'when' in com or 'how' in com or 'why' in com or 'are' in com or \
                'who' in com and 'what is the time' != com and 'quit' != com and com not in thanks and com not in age \
                and com not in creator and com not in greetings and com not in "what is today's news" and com not in \
                "what's today's news" and com not in "today's news" and com not in "show news":
            com1=''


            for i in range(11):
                if keywords[i] in com:
                    n=keywords[i]
                    com1 = com.strip(n)
            com=com.replace(' ','+')

            webbrowser.open(f'https://google.com/search?#q={com}')
            var.set(f'Searching for {com1} on google...')
            speak(f'Searching for {com1} on google...')
            com = ''



"""                                     CODE FOR GUI
    uses tkinter to make a gui window for a welcoming aesthetic to attract the user """
def update(ind):
    frame = frames[(ind) % 84]
    ind += 1
    label.configure(image=frame)
    window.after(150, update, ind)


label2 = Label(window, textvariable=var1, bg='#FAB60C')
label2.config(font=("Courier", 20))
var1.set('User Said:')
label2.pack()

label1 = Label(window, textvariable=var, bg='#ADD8E6')
label1.config(font=("Courier", 20))
var.set('Welcome')
label1.pack(pady=2)


frames = [PhotoImage(file='t.gif', format=f'gif -index {i}') for i in range(84)]

window.title('TRAVIS')
window.iconbitmap('G:\Projects\Travis\icon.ico')

label = Label(window, width=500, height=475)
label.pack(anchor='center')
window.after(0, update, 0)



def about_menubar():
   messagebox.showinfo(title='TRAVIS',message='Developer: Mithun Menon \n\n Animator: Sia Prasad')


menubar=Menu(window)
window.config(menu=menubar)

help_menu=Menu(menubar,tearoff=0)
menubar.add_cascade(label='Help',menu=help_menu)
help_menu.add_command(label='About',command=about_menubar)


btn1 = Button(text='PLAY', width=20, command=lambda: play(), bg='#5C85FB')
btn1.config(font=("Courier", 12))
btn1.pack()
btn2 = Button(text='EXIT', width=20, command=window.destroy, bg='#5C85FB')
btn2.config(font=("Courier", 12))
btn2.pack()

window.mainloop()

