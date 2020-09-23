import random as rand
import csv
import smtplib
import imapclient

account = input('Email address: ')
passwd =  input('Password: ')

def emaildict(santacsv):            ## creates list of senders and dict of emails from csv
    with open(santacsv, 'r') as f:
        reader = csv.reader(f)
        lst = list(reader)
        
    emaildct = {} 
    sender = []

    for x in lst:
        emaildct[x[0]] = x[1]
        sender.append(x[0])
        
    return emaildct, sender
    
def hamiltonsanta(sender):  ##creates hamiltonian cycle of senders; i is paired with i+1%len(sender)
    
    pairings = []
    
    length = len(sender)
    rand.shuffle(sender)
    for i in range(length):
        pairings.append([sender[i], sender[(i+1)%len(sender)]])
    return pairings
    
def email(pairings, dct):           ## sends out emails with pairings
    smtpObj = smtplib.SMTP('smtp.gmail.com', 587)
    smtpObj.starttls()
    smtpObj.login(account, passwd )
    for x in range(len(pairings)):
        notified = pairings[x][0]
        reciever = pairings[x][1]
        smtpObj.sendmail(account, dct[notified], 'Subject: Secret Santa \nDear {}, you are paired with {}. Good luck getting them a gift.'.format(notified, reciever))
        ## email is hard coded but can easily be changed into a input(), which would make deletemail easier as well
        
def deletemail():  ## delete emails after sending them to ensure complete anonymity
    imapObj = imapclient.IMAPClient('imap.gmail.com', ssl = True)
    imapObj.login(account, passwd)
    imapObj.select_folder('[Gmail]/Sent Mail', readonly = False)
    toDelete = imapObj.search(['SUBJECT', 'Secret Santa'])
    imapObj.delete_messages(toDelete)
    imapObj.expunge()
    
def prog(santacsv):
    emaildct, sender = emaildict(santacsv)
    pairings = hamiltonsanta(sender)
    print(pairings)
    email(pairings, emaildct)
    deletemail()
    
if __name__ == "__main__":
    santacsv = input('CSV of Names and Emails of Members: ') 
    account = input('Email address: ')
    passwd =  input('Password: ')
    prog(santacsv)
