import json
import datetime
import random

from enum import Enum

from parse import Meal
from parse import MenuParser

from flask import Flask
from flask import render_template
from flask import request

app = Flask(__name__)


def isWeekend(date):
    if date.weekday() == 5 or date.weekday() == 6:
        return True
    else:
        return False

def fuckShitUp(s):
    # Divide into words
    words = s.split(' ')
    # Pick a random spot to insert the fucking
    n = random.randint(0, len(words)-1)
    s = ' '.join(words[:n]) + ' Fucking ' + ' '.join(words[n:])
    return s

# Needed so we can use in the jinja templates
app.jinja_env.globals.update(isWeekend=isWeekend)
app.jinja_env.globals.update(fuckShitUp=fuckShitUp)

currentDate = datetime.datetime.today()
currentPath = "./menus/"

dateNamePath = currentPath + currentDate.year + "-" + currentDate.month + "-" + currentDate.day

# check if file exists yet
if os.path.exists(dateNamePath) and os.path.isfile(dateNamePath):
    file = open(dateNamePath, "r")
    menuJSON = file.read()
    file.close()
    menus = json.loads(menuJSON)
else:
    menus = {"b":[],"l":[],"d":[]}



@app.route('/')
def showIndexPage():
    if isWeekend(currentDate):
        if 3 <= currentDate.hour <= 10:
            menu = menus["Breakfast"]
        elif 10 < currentDate.hour <= 12+2:
            menu = menus["Lunch"]
        else:
            menu = menus["Dinner"]
    else:
        if 3 <= currentDate.hour <= 12+2:
            menu = menus["Lunch"]
        else:
            menu = menus["Dinner"]

    # dinner
    return render_template('main.html', menu=menu, currentDate=currentDate)


@app.route('/breakfast')
def showBreakfastPage():
    if not isWeekend(currentDate):
        menu = menus["Breakfast"]
        return render_template('main.html', menu=menu, currentDate=currentDate)
    else:
        failText = "There's no breakfast on the weekend, motherfucker."
        return render_template('fail.html', failText=failText, currentDate=currentDate)

@app.route('/brunch')
def showBrunchPage():
    if isWeekend(currentDate):
        menu = menus["Lunch"]
        return render_template('main.html', menu=menu, currentDate=currentDate)
    else:
        failText = "There's no brunch on weekdays, motherfucker."
        return render_template('fail.htm', failText=failText, currentDate=currentDate)


@app.route('/lunch')
def showLunchPage():
    if not isWeekend(currentDate):
        menu = menus["Lunch"]
        return render_template('main.html', menu=menu, currentDate=currentDate)
    else:
        failText = "There's no lunch on the weekend, motherfucker."
        return render_template('fail.html', failText=failText, currentDate=currentDate)

    menu = menus["Lunch"]
    return render_template('main.html', menu=menu, currentDate=currentDate)


@app.route('/dinner')
def showDinnerPage():
    menu = menus["Dinner"]
    return render_template('main.html', menu=menu, currentDate=currentDate)


if __name__ == "__main__":
    app.run()