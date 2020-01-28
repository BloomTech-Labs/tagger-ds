import imaplib
import email
import csv
import quopri
from bs4 import BeautifulSoup
import re

class IMap():
    def __init__(self, address=None, password=None):
        self.address = address
        self.password = password
        self.login(self.address, self.password)

    def login(self, address=None, password=None):
        if not address:
            raise Exception("Missing email address.")
        if not password:
            raise Exception("Missing email password.")
        
        if "@gmail" in address:
            server = "imap.gmail.com"
        elif "@yahoo" in password:
            server = "imap.mail.yahoo.com"
        else:
            raise Exception("Please use a Yahoo or Gmail email account.")
        try:
            self.mail = imaplib.IMAP4_SSL(server)
            self.mail.login(address, password)
        except Exception as e:
            raise
        print("Logged in as {}!".format(address))

    def search_mailbox(self, inbox="inbox"):
        self.mail.select(inbox)
        
        typ, data = self.mail.search(None, "ALL")
        
        mail_ids = data[0].decode()
        mail_ids = mail_ids.split()
        
        return self.mail, mail_ids

    def clean_text(self, from_, msg):
        from_ = re.sub(r"<(.*?)>", "", from_).strip().replace('"', "")
        msg = quopri.decodestring(msg).decode("utf-8", errors="ignore")
        html = BeautifulSoup(msg, "html.parser")
        removals = html.find_all("style")
        for match in removals:
            match.decompose()

        msg = re.sub(r"\\n|\\r", "", msg)
        msg = " ".join(re.findall(r"\b\w+\b", msg))
        return (from_, msg)

    def save_mail(self, i_d, filename='email_data.csv', verbose=False):
        csv_file = open(filename, 'w', encoding='utf-8')
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(['id', 'uid', 'from_', 'subject', 'msg', 'content_type'])
        
        for i in i_d:
            try:
                typ, data = self.mail.fetch(str(i).encode(), '(UID RFC822)')

                uid = email.message_from_bytes(data[0][0])
                uid = uid.get_payload()
                uid = uid.split()[-3]

                meta = email.message_from_bytes(data[0][1])
                from_ = meta['From']
                subject = meta['Subject']
                content_type = meta['Content-Type'].split(';')[0]
                
                msg = meta.get_payload()
                while type(msg) != str:
                    msg = msg[0].get_payload()
                
                print(i)
                if verbose:
                    print('UID: ', uid)
                    print('From: ', from_)
                    print('Subject: ', subject)
                    print('Content-Type: ', content_type)
                    print('Message: ', quopri.decodestring(msg))

                from_, msg = self.clean_text(from_, msg)
                
                csv_writer.writerow([i, uid, from_, subject, msg, content_type])
                print('Message saved')
            except Exception as e:
                print(e)

# mail = IMap("", "")
# m,i = mail.search_mailbox()
# mail.save_mail(i)
            
    
