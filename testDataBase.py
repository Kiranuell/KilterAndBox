import sys
import sqlite3
from PyQt5.QtWidgets import *

con = sqlite3.connect("testbox.db")
cur = con.cursor()

currentBox = None

# box = cur.execute("SELECT id, name, inBox FROM box")
# boxes = []
# for i in box:
#     boxes.append(i)
# for i in boxes:
#     print(i)
#
# item = cur.execute("SELECT id, name, amount, inBox FROM item")
# items = []
# for i in item:
#     items.append(i)
# for i in items:
#     print(i)

box = cur.execute("SELECT name FROM box WHERE inBox IS NULL")
print("Boxes")
for i in box:
    print(*i)
print("")
item = cur.execute("SELECT name, amount FROM item WHERE inBox IS NULL")
print("Items")
for i in item:
    print(*i)

def addBox():
    name = input()
    if currentBox:
        cur.execute("INSERT INTO box (name, inBox) VALUES (?, ?)", (name, currentBox))
        con.commit()
    else:
        cur.execute("INSERT INTO box (name) VALUES (?)", (name,))
        con.commit()

def openBox():
    name = input()


while True:
    if input() == "addBox":
        print("создайте коробку")
        addBox()


