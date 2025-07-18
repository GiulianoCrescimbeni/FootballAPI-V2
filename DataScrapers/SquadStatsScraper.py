import bs4
import requests
import sched
import time
import json
import sys
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup

class Squad:
    #Squad Class#
    def __init__(self, position, logo, name, points, played, win, loose, tie, gd):
        self.position   = position
        self.logo       = logo
        self.name       = name
        self.points     = points
        self.played     = played
        self.win        = win
        self.loose      = loose
        self.tie        = tie
        self.gd         = gd

#Getting the name of the championship#
championship = str(sys.argv[1])

#Getting filters#
is_filtered = len(sys.argv) > 2
if is_filtered:
    filters = str(sys.argv[2]).split("-")
    parameter = filters[0]
    value = filters[1]

#Opening the connection with the site#
uClient = uReq("https://onefootball.com/en/competition/"+championship+"/table")
page_html = uClient.read()
uClient.close()

#Souping the page and getting data#
page_soup = soup(page_html,"html.parser")
squads = page_soup.findAll("li", {"class":"standings__row standings__row--link"})
squads_list = []
data = "["
counter = 0

for squad in squads:
    counter = counter + 1
    #Scraping data from the hmtl#
    squad_position_container = squad.find("span", {"class":"title-7-bold"})
    squad_position = squad_position_container.text.replace(" ","")

    squad_logo_container = squad.find("of-image", {"class":"entity-logo"})
    squad_logo = squad_logo_container.find("img", attrs = {'src' : True})['src']

    squad_name_container = squad.find("p", {"class":"title-7-medium standings__team-name"})
    squad_name = squad_name_container.text[1:-1]

    squad_stats = squad.findAll("span", {"class":"title-7-medium standings__cell-text--dimmed"}) + squad.findAll("span", {"class":"title-7-bold"})

    squad_played = squad_stats[0].text.replace(" ","")
    squad_win = squad_stats[1].text.replace(" ","")
    squad_loose = squad_stats[3].text.replace(" ","")
    squad_tie = squad_stats[2].text.replace(" ","")
    squad_gd = squad_stats[4].text.replace(" ","")

    squad_points = squad_stats[6].text

    #Checking Parameters and adding the squad in the squad list#
    if(is_filtered):
        if(parameter == "position"):
            if(squad_position == value):
                squad_class = Squad(squad_position, squad_logo, squad_name, squad_points, squad_played, squad_win, squad_loose, squad_tie, squad_gd)
                squads_list.append(squad_class)
        elif(parameter == "name"):
            if(squad_name.upper().find(value.upper()) != -1):
                squad_class = Squad(squad_position, squad_logo, squad_name, squad_points, squad_played, squad_win, squad_loose, squad_tie, squad_gd)
                squads_list.append(squad_class)
    else:
        squad_class = Squad(squad_position, squad_logo, squad_name, squad_points, squad_played, squad_win, squad_loose, squad_tie, squad_gd)
        squads_list.append(squad_class)

#    if(parameter == "position"):
#        if(squad_position == value):
#            data_set = '{ "Position":"'+squad_position+'", "Name":"'+squad_name+'", "Points":"'+squad_points+'", "Played":"'+squad_played+'", "Winned":"'+squad_win+'", "Loosed":"'+squad_loose+'", "Tie":"'+squad_tie+'"}'
#            data = data + data_set
#            break
#    else:
#        if(counter < len(squads)):
#            if(is_filtered):
#                #Applying name filter#
#                if(parameter == "name"):
#                    if(value in squad_name):
#                        data_set = '{ "Position":"'+squad_position+'", "Name":"'+squad_name+'", "Points":"'+squad_points+'", "Played":"'+squad_played+'", "Winned":"'+squad_win+'", "Loosed":"'+squad_loose+'", "Tie":"'+squad_tie+'"},'
#                        data = data + data_set
#            else:
#                data_set = '{ "Position":"'+squad_position+'", "Name":"'+squad_name+'", "Points":"'+squad_points+'", "Played":"'+squad_played+'", "Winned":"'+squad_win+'", "Loosed":"'+squad_loose+'", "Tie":"'+squad_tie+'"},'
#                data = data + data_set
#        else:
#            if(is_filtered):
#                #Applying name filter#
#                if(parameter == "name"):
#                    if(value in squad_name):
#                        data_set = '{ "Position":"'+squad_position+'", "Name":"'+squad_name+'", "Points":"'+squad_points+'", "Played":"'+squad_played+'", "Winned":"'+squad_win+'", "Loosed":"'+squad_loose+'", "Tie":"'+squad_tie+'"}'
#                        data = data + data_set
#            else:
#                data_set = '{ "Position":"'+squad_position+'", "Name":"'+squad_name+'", "Points":"'+squad_points+'", "Played":"'+squad_played+'", "Winned":"'+squad_win+'", "Loosed":"'+squad_loose+'", "Tie":"'+squad_tie+'"}'
#                data = data + data_set

#Printing all the data#
i = 0
for squad in squads_list:
    if(i == 0):
        data_set = '{"Position":"'+squad.position+'", "SquadLogo":"'+squad.logo+'", "Name":"'+squad.name+'", "Points":"'+squad.points+'", "Played":"'+squad.played+'", "Winned":"'+squad.win+'", "Loosed":"'+squad.loose+'", "Tie":"'+squad.tie+'", "Goal Difference":"'+squad.gd+'"}'
        i = i + 1
    else:
        data_set = ',{"Position":"'+squad.position+'", "SquadLogo":"'+squad.logo+'", "Name":"'+squad.name+'", "Points":"'+squad.points+'", "Played":"'+squad.played+'", "Winned":"'+squad.win+'", "Loosed":"'+squad.loose+'", "Tie":"'+squad.tie+'", "Goal Difference":"'+squad.gd+'"}'
    data = data + data_set

data = data + "]"
json_dump = json.dumps(data)
print(json_dump)
exit()