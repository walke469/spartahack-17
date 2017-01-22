# Parsing congress.gov/members/

import requests
from lxml import html
from lxml.html import fromstring

# FIRST: Get Senators and Reps's websites.

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


#SECOND: Yo visit all those links tho. And get all the data.
for href in range(1):
    hpage = requests.get( hrefs[href] )
    htree = html.fromstring( hpage.content )

    # get names
    names = htree.xpath('//h1[@class="legDetail"]/text()')

    # get state, district and time in congress
    statedistrictcon = htree.xpath('//table[@class="standard01 lateral01"]/tbody/tr/td/text()')

    # put those in separate lists
    states = []
    districts = []
    times =[]
    inc = 0

    for cnt in range( len(statedistrictcon) ):
        if inc == 0:
            states.append(statedistrictcon[cnt])
            inc = inc + 1
        elif inc == 1:
            districts.append(statedistrictcon[cnt])
            inc = inc + 1
        elif inc == 2:
            times.append(statedistrictcon[cnt])
            inc = 0

    # get website
    websites = htree.xpath('//table[@class="standard01 nomargin"]/tr/td/a/@href')

    # get address, phone number and party
    contacts = htree.xpath('//table[@class="standard01 nomargin"]/tr/td/text()')

    # put those in separate lists
    addresses = []
    phones = []
    parties = []
    inc = 0

    for cnt in range( len(contacts) ):
        if inc == 0 or inc == 1:
            inc = inc + 1
        elif inc == 2:
            addresses.append(contacts[cnt])
            inc = inc + 1
        elif inc == 3:
            phones.append(contacts[cnt])
            inc = inc + 1
        elif inc == 4:
            parties.append(contacts[cnt])
            inc = 0

    # do something with them before the for loop ends probably. like put them in a database.
    # for cnt in range(541)
    #   names[cnt]
    #   states[cnt]
    #   districts[cnt]
    #   times[cnt]
    #   websites[cnt]
    #   address[cnt]
    #   phones[cnt]
    #   parties[cnt]

