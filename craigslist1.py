"""

This program upon running will email the specified email address all the fender jazzmaster guitars on sale from the specified craigslist website.  The original case will be the Long Island craigslist.  Runs on Python 3.x


Dependencies:
    Beautiful Soup
    urllib

"""


from bs4 import BeautifulSoup as soup
from urllib.request import urlopen as uReq


#email information set up
user = 'ENTER SENDER EMAIL HERE'
pwd = 'ENTER SENDER PASSWORD HERE'
recipient = 'ENTER RECIPIENT PASSWORD HERE'
subject = 'Daily Guitar Digest'
body = '--- BEGIN GUITAR DAILY DIGEST ---\n'
my_url = 'https://longisland.craigslist.org/search/sss?query=fender+jazzmaster&sort=rel'    # change to whichever craigslist you choose
def send_email(user, pwd, recipient, subject, body):
    import smtplib

    gmail_user = user
    gmail_pwd = pwd
    FROM = user
    TO = recipient if type(recipient) is list else [recipient]
    SUBJECT = subject
    TEXT = body

    # Prepare actual message
    message = """From: %s\nTo: %s\nSubject: %s\n\n%s
    """ % (FROM, ", ".join(TO), SUBJECT, TEXT)
    try:
        # SMTP_SSL Example
        server_ssl = smtplib.SMTP_SSL("smtp.gmail.com", 465)
        server_ssl.ehlo() # optional, called by login()
        server_ssl.login(gmail_user, gmail_pwd)
        # ssl server doesn't support or need tls, so don't call server_ssl.starttls()
        server_ssl.sendmail(FROM, TO, message)
        #server_ssl.quit()
        server_ssl.close()
        print ('successfully sent the mail')
    except:
        print ("failed to send mail")

#scrape the page
uClient = uReq(my_url)
page_html = uClient.read()
uClient.close()

page_soup = soup(page_html, "lxml")

for item in page_soup.findAll('p', {'class':'result-info'}):
    price = item.find('span', {'class':'result-price'})
    if price != None:
        price = price.text
    title = item.a.text
    link = item.a['href']
    body += title
    if price != None:
        body += ' ---> ' + price + '\n' + link + '\n*****\n\n\n\n\n'
    else:
        body += '\n' + link + '*****\n\n\n\n\n'

body += '--- END GUITAR DAILY DIGEST ---\n'

#send the email
send_email(user, pwd, recipient, subject, body)
