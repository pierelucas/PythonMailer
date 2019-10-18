# Author: PiereLucas (Julian H.)
# Python SMTP Mailer

import os
import smtplib
import sys
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

class MultiMail():

    def __init__(self):

        # SMTP Data
        self.host = "smtp.sendgrid.net"
        self.port = 587
        self.user_name = "apikey"
        self.pass_word = ""

        # Mail Header
        self.mail_from = None
        self.mail_to = []
        self.subject = None

        # Mail Text
        self.mail_text_path = None
        self.mail_text = None

        # Mailinglist
        self.mail_list_path = None

    def inp(self):
        # Insert sendgrid api key
        self.subject = str(input("Subject » "))
        self.mail_from = str(input("Mail From » "))

        while True:
            choice_list = str(input("Wanna load mailing list [y|n] » "))
            if choice_list == 'y':
                while True:
                    self.mail_list_path = str(input("Mail List » "))
                    if os.path.isfile(self.mail_list_path):
                        mail_list_true = self.read_mail_list()
                        if mail_list_true: break
                    else:
                        print("Path not readable")
                        continue
                break
            if choice_list == 'n':
                mail_to = str(input("Mail To » "))
                self.mail_to.append(mail_to)
                break
            else:
                print("Wrong Input")
                continue

        while True:
            choice_path = str(input("Build mail from file or input [file|input] » "))
            if choice_path == 'file':
                while True:
                    self.mail_text_path = str(input("FILE // Path » "))
                    if os.path.isfile(self.mail_text_path):
                        mail_text_true = self.read_mail_text()
                        if mail_text_true: break
                    else:
                        print("Path not readable")
                        continue
                break
            elif choice_path == 'input':
                self.mail_text = str(input("INPUT // Mail Text » "))
                break
            else:
                print("Wrong Input")
                continue

        return

    def out(self, *, mode):
        if mode == 'success': return "Program Completed"
        elif mode == 'fail': return "Programm exited earlier"

    def check_apikey(self):
        try:
            while True:
                if os.path.isfile("apikey.txt"):
                    with open("apikey.txt", 'rt') as f:
                        self.pass_word = f.read()

                    print("Host:" + self.host)
                    print("Api-Key loaded: " + self.pass_word)

                    smtp_true = self.smtp_check()
                    if smtp_true: pass
                    else: continue

                    break
                elif not os.path.isfile("apikey.txt"):
                    print("Host:" + self.host)
                    self.pass_word = str(input("No Api-Key found, please insert one: "))

                    smtp_true = self.smtp_check()
                    if smtp_true:
                        pass
                    else:
                        continue

                    with open("apikey.txt", 'wt') as f:
                        f.write(self.pass_word)
                    break
                else: raise PermissionError
            return
        except PermissionError:
            while True:
                print("Host:" + self.host)
                print("No Permission, we have to work without files")
                self.pass_word = str(input("Insert Api-Key: "))

                smtp_true = self.smtp_check()
                if smtp_true:
                    pass
                else:
                    continue

                return
        except KeyboardInterrupt:
            print("CTRL + C")
            sys.exit(0)

    def smtp_check(self):
        try:
            s = smtplib.SMTP(host=self.host, port=self.port)
            s.starttls()
            s.login(user=self.user_name, password=self.pass_word)
            print("Api-Key is Valid")
            return True
        except:
            print("Error in SMTP Authentification")
            print("Api-Key not loaded")
            return False

    def mail(self):
        with smtplib.SMTP(host=self.host, port=self.port) as s:
            try:
                try:
                    s.connect(host=self.host, port=self.port)
                    print("Sucessfully connected: " + self.host)
                except: print("Can't connect: " + self.host)

                try:
                    s.starttls()
                    print("TLS loaded: " + self.host)
                except: print("Can't load TLS: " + self.host)

                try:
                    s.login(user=self.user_name, password=self.pass_word)
                    print("Sucessfully login: " + self.user_name)
                except: print("Can't login: " + self.user_name)

                for row in self.mail_to:
                    msg = MIMEMultipart()
                    msg["Subject"] = self.mail_text
                    msg["From"] = self.mail_from
                    msg["To"] = row
                    msg.attach(MIMEText(self.mail_text))

                    s.sendmail(from_addr=msg["From"], to_addrs=msg["To"], msg=msg["To"])

                return True
            except:
                print("Error in sendmail")
                return False

    def read_mail_text(self):
        with open(self.mail_text_path, 'rt') as f:
            self.mail_text = f.read()
        return True

    def read_mail_list(self):
        with open(self.mail_list_path, 'rt') as f:
            self.mail_to = f.readlines()
        return True

    def run(self):
        self.check_apikey()
        self.inp()
        _true = self.mail()
        if _true: print(self.out(mode="success"))
        else: print(self.out(mode="fail"))


# TO BE CONTINUED

if __name__ == "__main__":
    mm = MultiMail()
    mm.run()
