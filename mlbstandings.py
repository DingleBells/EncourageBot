from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
from prettytable import PrettyTable

def getStandings(league, div):
    my_url = 'https://nytimes.stats.com/mlb/standings.asp'
    uClient = uReq(my_url)
    page_html = uClient.read()
    uClient.close()

    page_soup = soup(page_html, "html.parser")
    [americanleague, nationalleague] = page_soup.findAll('table', {"class": "shsTable shsBorderTable"})

    # 0 is al, 1 is nl
    if league == 0:
        wanted = americanleague
    else:
        wanted = nationalleague

    divdict = {'east': 0, 'central': 1, 'west': 2}
    outlist = []

    for i in range(1, 6):
        places = wanted.findAll('tr', {'class': f'shsStandPos{i}'})
        data = places[divdict[div]]
        datalist = []
        for thing in data:
            datalist.append(thing.text)
        outlist.append((datalist[0].strip(), datalist[1], datalist[2], datalist[3], datalist[4],
                        datalist[10].replace(" ", ""), datalist[11].replace(" ", "")))

    return outlist

def formatData(data):
    table = PrettyTable(['Team', 'W', 'L', 'PCT', 'GB', 'Last 10', 'Streak'])
    for team in data:
        table.add_row(list(team))
    return table

def returnstandings(league, div):
  return "```" + str(formatData(getStandings(league, div))) + "```"