import sqlite3
import unicodedata
import time
from Datenbankpfad import pfadDatenbank



Datenbank2 = pfadDatenbank() + "/Vokabldatebank.sqlite3"
Datenbank1 = pfadDatenbank() + "/Vokabs_all.db"

conn1 = sqlite3.connect(Datenbank1)
conn2 = sqlite3.connect(Datenbank2)
c1 = conn1.cursor()
c2 = conn2.cursor()
c1.execute("Select * from Ubersetzung")
ab = c1.fetchall()
besteht = 0
bestehtnicht = 0
for i in ab:
    c2.execute('Select * from Translation where words = "{word}"'.format(word = i[2]))
    response = c2.fetchone()
    #print(response)
    if response == None:
        bestehtnicht += 1
        c2.execute("INSERT INTO Translation VALUES (:word, :infinitiv, :translation, :ausgangssprache)", {"word": i[2], "infinitiv": i[0], "translation": i[1], "ausgangssprache": "fr"})
    elif response:
        besteht += 1
        #c2.execute("UPDATE Incoming SET wordcount = wordcount WHERE words = :vokabeln",{"vokabeln": i[0], "number": i[5]})
conn1.commit()
conn2.commit()
conn1.close()
conn2.close()

print(besteht)
print(bestehtnicht)
