import sys
import sqlite3
from PyQt5.QtWidgets import *

con = sqlite3.connect("testbox.db") # или :memory: чтобы сохранить в RAM
cur = con.cursor()

boxExist = [21, 22, 23, 24, 25, 26, 27, 28]
print((' ').join(list(map(str, boxExist))))
trashStuff = cur.execute(f"SELECT id FROM stuff WHERE inBox NOT IN ({(', ').join(list(map(str, boxExist)))})")
trashList = []
for i in trashStuff:
    trashList.append(*i)
print(trashList)
