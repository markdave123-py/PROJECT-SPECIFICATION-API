from passlib.context import CryptContext
from email.message import EmailMessage
import ssl
import smtplib
from datetime import datetime


import os
from dotenv import load_dotenv

load_dotenv()


pwd_context = CryptContext(schemes=["bcrypt"], deprecated= "auto")

def hash_password(password: str): 
    return pwd_context.hash(password)

def verify(attempt_password,main_password):
    return pwd_context.verify(attempt_password,main_password)


expire = datetime.now().day + 1
deadline_time = f"{datetime.now().year}/{datetime.now().month}/{expire}"

def convert_month_day(deadline):
    days_31 = [1, 2, 3, 5, 7, 8, 10, 12]
    days_30 = [9, 4, 6, 11]
    list_deadline = deadline.split("/")
    if int(list_deadline[1]) in days_30:
        if int(list_deadline[2]) > 30:
            new_month = int(list_deadline[1]) + 1
            new_day = int(list_deadline[2]) - 30
        else:
            new_month = int(list_deadline[1])
            new_day = int(list_deadline[2])



    elif int(list_deadline[1]) in days_31:
        if int(list_deadline[2]) > 31:
            new_month = int(list_deadline[1]) + 1
            new_day = int(list_deadline[2]) - 31

        else:
            new_month = int(list_deadline[1])
            new_day = int(list_deadline[2])

    else:
        if int(list_deadline[2]) > 28:
            new_month = int(list_deadline[1]) + 1
            new_day = int(list_deadline[2]) - 31

        else:
            new_month = int(list_deadline[1])
            new_day = int(list_deadline[2])

    new_date = f"{datetime.now().year}/{new_month}/{new_day}"

    if int(new_date.split("/")[2]) > 30:
        new_date = convert_month_day(new_date)


    return new_date

def sendEmail(sender_email, sender_password, receiver_email, subject, body):

    em = EmailMessage()  

    em['From'] = sender_email
    em['To'] = receiver_email
    em['subject'] = subject
    em.set_content(body)

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(sender_email, sender_password)
        smtp.sendmail(sender_email, receiver_email, em.as_string())

body_of_join = "Please permitte me to join ur project i promise to be a good participant and make meaningful contributions "
def removing(value,removed):
    value.remove(removed)
    return value

def adding(value,added):
    value.append(added)
    return value
