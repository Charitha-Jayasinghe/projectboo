import smtplib
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import logging
from bs4 import BeautifulSoup


#here im sending the email using external smtp server 
#static/server-downtime-notification.html isa static html file the mail content replace by html parser and add your contents in the html and render it and send the email
class EmailSender:
    def __init__(self):
        self.user = 'abcname'
        self.password = 'pw'
        self.mail = {
            'sender': "info@bisevoapp.se",
            'receiver': ["user1@gmail.com","user2@gmail.com", "user3@gmail.com"],
        }

   
    def send_email(self,datatime,failed_services):

     
        message = MIMEMultipart()
        message["From"] = self.mail["sender"]
        message["To"] = ", ".join(self.mail["receiver"])
        message["Subject"] = "Urgent: Server Downtime Notification"

        with open("static/server-downtime-notification.html") as file:
            body = file.read()

        soup = BeautifulSoup(body, "html.parser")

        element_start_time = soup.find(text="Start Time:").parent
  
        element_start_time.string = f"Start Time: {datatime}"

        element_affected_services = soup.find(text="Affected Services:").parent

        affectedservices = ", ".join(failed_services)
            

        element_affected_services.string = f"Affected Services: {affectedservices}"

        html_as_string = str(soup)

        message.attach(MIMEText(html_as_string, "html"))
        logging.info("Attached message with updated datetime")


        context = ssl.create_default_context()

        try:
            with smtplib.SMTP_SSL("email-smtp.usa-north-82.amazonaws.com", 999, context=context) as server:
                server.login(self.user, self.password)
                server.sendmail(self.mail['sender'], self.mail['receiver'], message.as_string())
                
            return True
        except Exception as e:
            logging.error(f"Error sending email: {e}")
            return False
        
        

       