# Parsing congress.gov/members/

import requests
from lxml import html
from lxml.html import fromstring
import sqlite3
import os

def find(name, path):
    return_val = False
    files = [f for f in os.listdir('.') if os.path.isfile(f)]
    for f in files:
        if name in files:
            return_val = True
    return return_val

# FIRST: Create a database, or connect if it already exists.

if find('congresspeople.db', os.path.relpath('parsing.py')):
    conn = sqlite3.connect('congresspeople.db')
    c = conn.cursor()
    c.execute('''DELETE FROM'''+ ' congress')

else:
    conn = sqlite3.connect('congresspeople.db')
    c = conn.cursor()
    # Create table
    c.execute('''CREATE TABLE congress
             (name text, state text, district text, party text, time text, phone text, website text, address text)''')

# SECOND: Get Senators and Reps.
# create dictionary
takeadict = []

# get info from website
page = requests.get('https://www.congress.gov/members?pageSize=250&q={"congress":"115"}')
tree = html.fromstring(page.content)

# get senator urls
hrefs = tree.xpath('//select[@id="members-senators"]/option/@value')
del hrefs[0]

# get representative urls
representativehrefs = tree.xpath('//select[@id="members-representatives"]/option/@value')
del representativehrefs[0]

# put senators in dictionary
for i in range(441):
    hrefs.append( representativehrefs[ i ] )


#THIRD: Yo visit all those links tho. And get all the data.
for href in hrefs:
#for i in range(1):
    hpage = requests.get( href )
    htree = html.fromstring( hpage.content )

    # get names
    names = htree.xpath('//h1[@class="legDetail"]/text()')

    # get state, district and time in congress
    statedistrictcon = htree.xpath('//table[@class="standard01 lateral01"]/tbody/tr/td/text()')

    # put those in separate lists
    states = []
    districts = []
    times =[]

    for cnt in range( 3 ):
        if cnt == 0:
            states.append(statedistrictcon[cnt])
        elif cnt == 1:
            districts.append(statedistrictcon[cnt])
        elif cnt == 2:
            times.append(statedistrictcon[cnt])
    
    # get website
    websites = htree.xpath('//table[@class="standard01 nomargin"]/tr/td/a/@href')

    if len(websites) == 0:
        websites.append('--')

    # get address, phone number and party
    contacts = htree.xpath('//table[@class="standard01 nomargin"]/tr/td/text()')

    # put those in separate lists
    addresses = []
    phones = []
    parties = []
    inc = 0

    if len(contacts) == 5 :
        for cnt in range(5):
            if cnt == 2:
                addresses.append(contacts[cnt])
            elif cnt == 3:
                phones.append(contacts[cnt])
            elif cnt == 4:
                parties.append(contacts[cnt])

    elif len(contacts) == 3 :
        for cnt in range(3):
            if cnt == 0:
                addresses.append(contacts[cnt])
            elif cnt == 1:
                phones.append(contacts[cnt])
            elif cnt == 2:
                parties.append(contacts[cnt])
                
    else:
        addresses.append('--')
        phones.append('--')
        parties.append(contacts[0])

    # do something with them before the for loop ends probably. like put them in a database.
    for cnt in range(1):
        temp = [names[cnt], states[cnt], districts[cnt], parties[cnt], times[cnt], phones[cnt], websites[cnt], addresses[cnt]]
        c.execute('INSERT INTO congress VALUES (?,?,?,?,?,?,?,?)', temp)
        conn.commit()

conn.close()
