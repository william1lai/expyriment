import urllib
import re
import argparse
import string
from HTMLParser import HTMLParser
from htmlentitydefs import name2codepoint

menu_url = "http://m.dining.ucla.edu/menu/index.cfm?r=De%20Neve,Hedrick%20Dining,Covel%20Dining,Feast%20at%20Rieber&restaurantType=Residential"

hi = "&m=Dinner&d=01%2F05%2F2014"

aparser = argparse.ArgumentParser(description='''Find out how good the menu is today. BruinPlate not supported because it's not supported on the UCLA mobile dining page''')
aparser.add_argument('-l', '--lunch', action='store_true')
aparser.add_argument('infile', nargs='?')

tagofinterest = "div class=menu-full menu-detailed"

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


parser = MyHTMLParser()

canopener = urllib.FancyURLopener({})
args = aparser.parse_args()

if args.lunch:
    menu_url = menu_url + "&m=Lunch"
else:
    menu_url = menu_url + "&m=Dinner"

print menu_url

if not args.infile:
    f = canopener.open(menu_url)
else:
    f = open(args.infile, 'r')
s = f.read()
parser.feed(s)

covel = '\n'.join(parser.coveldata)
deneve = '\n'.join(parser.denevedata)
feast = '\n'.join(parser.feastdata)
print "Covel Menu:\n", covel
print "\nDe Neve Menu:\n", deneve
print "\nFeast Menu:\n", feast

ericdislikes = [ "mushroom", "shrimp", "seafood" ]
ericlikes = [ "pho", "spaghetti", "tacos" ]
briandislikes = [ "pepper shrimp" ]
brianlikes = [ "fish", "mahi", "baked potato", "shrimp" ]
edec = False
bdec = False

print ""
for item in parser.coveldata:
    for food in ericdislikes:
        if string.find(string.lower(item), food) != -1:
            print "Eric won't like Covel because of", item
            edec = True
for item in parser.denevedata:
    for food in ericdislikes:
        if string.find(string.lower(item), food) != -1:
            print "Eric won't like De Neve because of", food
            edec = True
for item in parser.feastdata:
    for food in ericdislikes:
        if string.find(string.lower(item), food) != -1:
            print "Eric won't like Feast because of", food
            edec = True
for item in covel:
    for food in ericlikes:
        if string.find(string.lower(item), food) != -1:
            print "Eric will like Covel because of", food
            edec = True
for item in parser.denevedata:
    for food in ericlikes:
        if string.find(string.lower(item), food) != -1:
            print "Eric will like De Neve because of", food
            edec = True
for item in parser.feastdata:
    for food in ericlikes:
        if string.find(string.lower(item), food) != -1:
            print "Eric will like Feast because of", food
            edec = True

for item in parser.coveldata:
    for food in briandislikes:
        if string.find(string.lower(item), food) != -1:
            print "Brian won't like Covel because of", food
            bdec = True
for item in parser.denevedata:
    for food in briandislikes:
        if string.find(string.lower(item), food) != -1:
            print "Brian won't like De Neve because of", food
            bdec = True
for item in parser.feastdata:
    for food in briandislikes:
        if string.find(string.lower(item), food) != -1:
            print "Brian won't like Feast because of", food
            bdec = True
for item in parser.coveldata:
    for food in brianlikes:
        if string.find(string.lower(item), food) != -1:
            print "Brian will like Covel because of", food
            bdec = True
for item in parser.denevedata:
    for food in brianlikes:
        if string.find(string.lower(item), food) != -1:
            print "Brian will like De Neve because of", food
            bdec = True
for item in parser.feastdata:
    for food in brianlikes:
        if string.find(string.lower(item), food) != -1:
            print "Brian will like Feast because of", food
            bdec = True

if not edec:
    print "Eric doesn't care"
if not bdec:
    print "Brian doesn't care"

print "Victor doesn't care\n"
