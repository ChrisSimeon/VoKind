# -*- coding: utf-8 -*-
import sys
import requests
import time
from bs4 import BeautifulSoup
import sqlite3
import webbrowser
import unicodedata
from wiktionaryparser import WiktionaryParser





def ankiconn(vokab, translation, definition):
    import json
    import urllib.request
    import unicodedata

    deckname = "Englisch"
    modelName = "Englisch Cards"

    if definition:
        fields = {"English": vokab, "German": translation, "Definition": definition}
    else:
       fields = {"English": translation, "German": vokab, "Definition": ""}
    request = {"action": "addNote", "version": 6, "params": {"note": {"deckName": deckname, "modelName": modelName, "fields": fields, "options": {"allowDuplicate": False, "duplicateScope": "deck", "duplicateScopeOptions": {
                        "deckName": deckname, "checkChildren": True}}, "tags": [""]}}}
    requestJson = json.dumps(request).encode('utf-8')
    try:
        json.load(urllib.request.urlopen(urllib.request.Request('http://localhost:8765', requestJson)))
    except urllib.error.URLError:
        print("Please Open Anki")
    with open("/Users/chris/Documents/OneDrive/Christian/Sprachen/Englisch/english.txt", "a") as f:
        print("printed in Anki", file=f)



def request_Linguee(query, buff=0):
    baseurl = "https://www.linguee.de/deutsch-englisch/search?query="
    url = baseurl + query
    #print(url)
    page = requests.get(url)

    #print(page)

    if page.status_code == 200:
        #print(buff)''  
        src = page.content
        soup = BeautifulSoup(src, "html5lib")
        #print(soup)
        Database = {}
        Database["word"] = query
        #soup1 = soup.find("div", {"class": "exact"})
        #soup2 = soup.find("div", {"class": "lemma_content"})
        if soup.find("div", {"class": "isMainTerm"}):
            soup1 =soup.find("div", {"class": "isMainTerm"}).attrs
            Database["language"] = soup1["data-source-lang"].lower()
            if Database["language"] == "de":
               Database["langto"] = "en"
            elif Database["language"] == "en":
               Database["langto"] = "de" 


        elif soup.find("div", {"class": "isForeignTerm"}):
            soup1=soup.find("div", {"class": "isForeignTerm"}).attrs
            Database["language"] = soup1["data-source-lang"].lower()
            if Database["language"] == "de":
               Database["langto"] == "en"
            elif Database["language"] == "en":
               Database["langto"] = "de" 
        else: 
            Database["language"] = ""
        # print(soup)
        # if soup1:
        #     Infinitiv = soup.find_all("span", {"class": "tag_trans"})
        #     #print("loop1", soup1)
        # elif soup2:
        Infinitiv = soup.find_all("span", {"class": "tag_trans"})
        #print(Infinitiv)

            # print(Infinitiv)
        if Infinitiv:
            c = ""
            for a in Infinitiv[0:8]:
                c += a.text.replace(",", "") + "\n"
            Database["Translation"] = c
            #print(c)
        else:
            print("Not Found, Opening Browser")
            webbrowser.open(url)
            return

        # timecode 
        ts = time.time()
        Database["timestamp"] = int(str(ts)[0:10])

        if buff == 1:
            Datenbankpfad = "/Users/chris/Documents/OneDrive/Christian/Sprachen/ProgrammVokabeln/Datenbank/Vokabldatebank.sqlite3"
            conn =sqlite3.connect(Datenbankpfad)
            c = conn.cursor()
            c.execute('Select Incoming.words from Incoming where Incoming.words = "{Vokab}"'.format(Vokab=Database["word"]))
            res = c.fetchone()
            if res:
                c.execute("UPDATE Incoming SET wordcount = wordcount + :number, timestamp = :updateat  WHERE words = :vokabeln",{"vokabeln": Database["word"], "number": 5, "updateat": Database["timestamp"]})
            else:
                c.execute("INSERT INTO Incoming VALUES (:word, :usage, :book, :timestamp, :language, :wordcount, :languageto)", {"word": Database["word"], "usage": "", "book": "", "timestamp": Database["timestamp"], "language": Database["language"], "wordcount": 5, "languageto": Database["langto"]})
                c.execute("INSERT INTO Translation VALUES (:word, :infinitiv, :translation, :language)", {"word": Database["word"], "infinitiv": "", "translation":Database["Translation"], "language": Database["language"]})
            conn.commit()
            conn.close()

    else:
        print("Internetverbindung Fehlerhaft oder Wort nicht gefunden")
        return
    
    return Database

def definition_english(buff):
    from wiktionaryparser import WiktionaryParser
    import json
    parser = WiktionaryParser()
    word = json.dumps(parser.fetch(buff),sort_keys=True, indent=4)
    data = json.loads(word)
    c = ""
    try:
        for i in data[0]["definitions"][0]["text"]:
            c += i + "\n"
        return c
    except IndexError:
        return

if __name__ == "__main__":
    if len(sys.argv) == 1:
        #print(sys.argv[0])
        webbrowser.open("https://www.linguee.de/deutsch-englisch/")
    elif len(sys.argv) == 2:
        query = sys.argv[1]
        sysencoding = sys.getfilesystemencoding()
        query_unicode = sys.argv[1].encode(sysencoding)
        query = query_unicode.decode("utf-8")
        #print(sys.argv[0] + " " + sys.argv[1])
        print(query + "\n" + "-----")
        abc= request_Linguee(query, buff=1)["Translation"]
        print(abc)
        defenglish = definition_english(query)
        print(defenglish)
        with open("/Users/chris/Documents/OneDrive/Christian/Sprachen/Englisch/english.txt", "a") as f:
            print("\n" + "--------------", file=f)
            print(query + "\n" + "..........", file=f)
            print(abc, file=f)
            print(".......", file=f)
            print(defenglish, file=f)
        ankiconn(query,abc,defenglish)


    else:
        query = ""
        ag1 = len(sys.argv)
        for i in sys.argv[1:ag1]:
            query += i + " "
        #print (query)
        print(query + "\n" + "-----")
        print(request_Linguee(query, buff=1))
    
