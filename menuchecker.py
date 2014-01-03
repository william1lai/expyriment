import urllib
import re
import argparse
import string
from HTMLParser import HTMLParser
from htmlentitydefs import name2codepoint

class MyHTMLParser(HTMLParser):
    def reset(self):
        HTMLParser.reset(self)
        self.text = []
        self.coveldata = []
        self.denevedata = []
        self.feastdata = []
        self.current = self.coveldata
        self.isinTag = False
        self.amp = False

    def handle_starttag(self, tag, attrs):
        if tag == "div":
            for a, b in attrs:
                if b == "menu-full menu-detailed":
                    self.isinTag = True
    def handle_endtag(self, tag):
        if tag == "div":
            self.isinTag = False
    def handle_data(self, data):
        if (re.search('[A-Za-z&]', data)) and self.isinTag:
            if data != "view full menu" and data != "vegetarian" and data != "vegan":
                if data == "Covel Dining":
                    self.current = self.coveldata
                elif data == "De Neve":
                    self.current = self.denevedata
                elif data == "FEAST at Rieber":
                    self.current = self.feastdata
                elif data == "&":
                    self.amp = True
                    self.text.append(data)
                else:
                    if self.amp:
                        self.text.append(data)
                        self.current.append("".join(self.text))
                        self.text = []
                        self.amp = False
                    elif self.text: #not empty and not ampersand
                        self.current.append("".join(self.text))
                        self.text = []
                        self.text.append(data)
                    else:
                        self.text.append(data)
                    
    def handle_comment(self, data):
        pass
    def handle_entityref(self, name):
        self.handle_data(self.unescape("&%s;" % name))
    def handle_charref(self, name):
        self.handle_entityref("#" + name)
    def handle_decl(self, data):
        pass

def main():
    menu_url = "http://m.dining.ucla.edu/menu/index.cfm?r=De%20Neve,Hedrick%20Dining,Covel%20Dining,Feast%20at%20Rieber&restaurantType=Residential"
    aparser = argparse.ArgumentParser(description='''Find out how good the menu is today. BruinPlate not supported because it's not supported on the UCLA mobile dining page''')
    aparser.add_argument('-l', '--lunch', action='store_true')
    aparser.add_argument('menu', nargs='?')
    aparser.add_argument('preferences', nargs='?')

    parser = MyHTMLParser()
    canopener = urllib.FancyURLopener({})
    args = aparser.parse_args()

    if args.lunch:
        menu_url = menu_url + "&m=Lunch"
    else:
        menu_url = menu_url + "&m=Dinner"

    if not args.menu:
        f = canopener.open(menu_url)
    else:
        f = open(args.infile, 'r')
    s = f.read()
    parser.feed(s)

    if not args.preferences:
        pf = open("menuchecker-preferences.txt", 'r')
    else:
        pf = open(args.preferences, 'r')
    npeople = int(pf.readline().strip())
    names = []
    dislikes = []
    likes = []
    cares = []
    for i in range(npeople):
        names.append(pf.readline().strip())
        dislikes.append(filter(None, [s.strip() for s in pf.readline().split(',')]))
        likes.append(filter(None, [s.strip() for s in pf.readline().split(',')]))
        cares.append(False)

    covel = '\n'.join(parser.coveldata)
    deneve = '\n'.join(parser.denevedata)
    feast = '\n'.join(parser.feastdata)
    print "Covel Menu:\n", covel
    print "\nDe Neve Menu:\n", deneve
    print "\nFeast Menu:\n", feast

    nhalls = 3
    covelscore = 0
    denevescore = 0
    feastscore = 0
    print ""

    for z in range(nhalls): #covel = 0, de neve = 1, feast = 2
        hallname = "Covel"
        data = parser.coveldata
        if z == 1:
            hallname = "De Neve"
            data = parser.denevedata
        elif z == 2:
            hallname = "Feast"
            data = parser.feastdata
        for item in data:
            for i in range(len(names)):
                person = names[i]
                dislikelist = dislikes[i]
                likelist = likes[i]

                result = 0 #0 neutral, >0 like, <0 dislike
                
                for food in dislikelist:
                    if food in str.lower(item):
                        result = result - 15
                for food in likelist:
                    if food in str.lower(item):
                        result = result + 10

                if result < 0:
                    print person, "won't like", hallname, "because of", item
                    cares[i] = True                    
                elif result > 0:
                    print person, "will like", hallname, "because of", item
                    cares[i] = True

                if z == 0:
                    covelscore = covelscore + result
                elif z == 1:
                    denevescore = denevescore + result
                else: #z == 2
                    feastscore = feastscore + result
               
    for i in range(len(names)):
        if cares[i] == False:
            print names[i], "doesn't care"

    print ""
    m = max(covelscore, denevescore, feastscore)
    if m < -20:
        print "This program recommends quick service.\n"
    elif m == feastscore: #tiebreaker order
        print "This program recommends Feast.\n"
    elif m == covelscore:
        print "This program recommends Covel.\n"
    else:
        print "This program recommends De Neve.\n"
    raw_input() #to keep window open


if __name__ == "__main__":
    main()
