##Imorts
import sqlite3
import sys
import Kindle_Functions as KF
import Abfrage_Larousse as AL
import Abfrage_Leo as ALe
import time
##Variables
Datenbankpfad = "/Users/chris/Documents/OneDrive/Christian/Sprachen/ProgrammVokabeln/Datenbank/Vokabldatebank.sqlite3"


def get_Vokabeln():
    Vokabeln = KF.Kindle_Import()
    conn =sqlite3.connect(Datenbankpfad)
    c = conn.cursor()
    for Vokabel in Vokabeln:
        c.execute("Select words from Incoming where words = :vokabel",{"vokabel": Vokabel["word"]})
        abc = c.fetchone()
        if abc:
            print("Wort: '{Vokab}' bereits vorhanden, Anzahl wirds geupdatet".format(Vokab=Vokabel["word"]))
            c.execute("UPDATE Incoming SET wordcount = wordcount + :number, timestamp = :updateat  WHERE words = :vokabeln",{"vokabeln": Vokabel["word"], "number": Vokabel["count"], "updateat": Vokabel["timestamp"]})
            conn.commit()
        else:
            if Vokabel["lang"] == "de":
                Vokabel["langto"] = None
            
            elif Vokabel["lang"] == "en":
                Vokabel["langto"] = "de"

            elif Vokabel["lang"] == "fr":
                Vokabel["langto"] = "de"
            
            c.execute("INSERT INTO Incoming VALUES (:word, :usage, :book, :timestamp, :language, :wordcount, :languageto)", {"word": Vokabel["word"], "usage": Vokabel["usage"], "book": Vokabel["booktitle"], "timestamp": Vokabel["timestamp"], "language": Vokabel["lang"], "wordcount":Vokabel["count"], "languageto":Vokabel["lang"]})
            conn.commit()

    conn.close()
    return 0

def DatenbankabfrageDefinition():
    conn =sqlite3.connect(Datenbankpfad)
    c = conn.cursor()
    c.execute('Select Incoming.words, Incoming.language from Incoming LEFT JOIN Definition ON Incoming.words = Definition.words WHERE Definition.words is NULL AND Incoming.wordcount > 2 AND Incoming.language = "fr"')
    abc = c.fetchall()
    vokabs = []
    for i in abc:
        vokab = {"word": i[0], "lang":i[1]}
        vokabs.append(vokab)
    conn.close()
    return vokabs

#buffer = DatenbankabfrageDefinition()
#print(buffer)

def Abfrage_Larousse(buffer):
    conn =sqlite3.connect(Datenbankpfad)
    c = conn.cursor()
    n = 0
    for i in buffer:
        if i["lang"] == "fr":
            larousserep = AL.get_Larousse(i["word"])
            #print(larousserep)
            if larousserep is not None:
                c.execute("INSERT INTO Definition VALUES (:word, :infinitiv, :definition, :expression, :difficultes, :linfuisticdef, :origin, :linkprononc, :larousselink)",\
                    {"word": larousserep["word"], "infinitiv": larousserep["Infinitiv"], "definition": larousserep["Definitions"], "expression": larousserep["Expressions"], \
                        "difficultes": larousserep["Difficultes"], "linfuisticdef": larousserep["LinguisticDef"], "origin": larousserep["Origin"], "linkprononc": larousserep["LinkPronouciation"],"larousselink": larousserep["URL"]})
                
                conn.commit()
        else:
            print("Das Wort " + str(i["word"]) + " existiert bereits")
        time.sleep(5)
        n += 1
        print("Abfrage Larousse: " + str(n) + "/" + str(len(buffer)) )
                
    
    conn.close()
    return


def DatenbankabfrageTranslation():
    conn =sqlite3.connect(Datenbankpfad)
    c = conn.cursor()
    c.execute("SELECT Incoming.words, incoming.language, Definition.Infinitiv FROM Incoming JOIN Definition ON  Incoming.words = Definition.words LEFT JOIN Translation ON Incoming.words = Translation.words WHERE Translation.words is NULL AND Incoming.wordcount > 1")
    abc = c.fetchall()
    vokabs = []
    for i in abc:
        vokab = {"word": i[0], "lang": i[1], "infinitiv": i[2]}
        vokabs.append(vokab)
    conn.close()
    return vokabs

def Abfrage_Leo(buffer):
    conn =sqlite3.connect(Datenbankpfad)
    c = conn.cursor()
    n = 0
    for i in buffer:
        if i["lang"] == "fr":
            leorep = ALe.Abfrage_Leo(i["infinitiv"], 0)
            #print(leorep["German"])
            if leorep["German"] is not None:
                c.execute("INSERT INTO Translation VALUES (:word, :infinitiv, :translation, :ausgangssprache)",{"word": i["word"], "infinitiv": i["infinitiv"], "translation": leorep["German"], "ausgangssprache": i["lang"]})
                conn.commit()
            else: 
                pass       
        elif i["lang"] == "de":
            leorep = ALe.Abfrage_Leo(i["word", 1])
            if leorep is not None:
                c.execute("INSERT INTO Translation VALUES (:word, :infinitiv, :translation, :ausgangssprache)",{"word": i["word"], "infinitiv": "", "translation": leorep["French"], "ausgangssprache": i["lang"]})
                conn.commit()
        time.sleep(5)
        n += 1
        print("Abfrage Leo: " + str(n) + "/" + str(len(buffer)) )
    return


def word_not_found(word):
    conn =sqlite3.connect(Datenbankpfad)
    c = conn.cursor()
    c.execute('Insert into nichts_gefunden (words, usage, book, timestamp, language, wordcount) SELECT words, usage, book, timestamp, language, wordcount FROM Incoming where Incoming.words = "{word1}"'.format(word1=word))
    c.execute('Delete from Incoming WHERE words = "{word1}"'.format(word1=word))
    conn.commit()
    conn.close()
    return

if __name__ == "__main__":
    Abfrage_Larousse(DatenbankabfrageDefinition())
    Abfrage_Leo(DatenbankabfrageTranslation())