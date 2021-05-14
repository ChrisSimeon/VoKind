def Kindle_Import():#gibt liste mit dict von vokabeln zurück, [words,usage,booktitle,timestamp,lang,count]

    import sqlite3
    import sys 
    import unicodedata

    try:     
         conn = sqlite3.connect("/Volumes/Kindle/system/vocabulary/vocab.db")
    except: 
        print("Kindle nicht angeschlossen")
        sys.exit()
        
    
    Kindle_Vokabs = []


    c = conn.cursor()

    c.execute("""select words.word,lookUPS.usage,booK_INFO.title,words.timestamp, words.lang, count(word)
             from lookups, wordS, booK_INFO 
             where looKUPS.word_key = wordS.id and lookUPS.book_key = booK_INFO.id
			GROUP by word
			order by count (word) DESC""")


    conn.commit()

    buffer = c.fetchall()
        
    conn.close()

    for i in buffer:
        Kindle_Vokabs.append({"word": unicodedata.normalize("NFC", i[0]),"usage": unicodedata.normalize("NFC", i[1]),"booktitle":unicodedata.normalize("NFC", i[2]),"timestamp":int(str(i[3])[0:10]), "lang": i[4], "count": i[5]})



    return Kindle_Vokabs

def Kindle_leeren():
    import sqlite3
    import sys
    try:     
         conn = sqlite3.connect("/Volumes/Kindle/system/vocabulary/vocab.db")
    except: 
        print("Kindle nicht angeschlossen")
        sys.exit()
        
    c = conn.cursor()

    c.execute("DELETE FROM LOOKUPS")
    c.execute("DELETE FROM WORDS")
    c.execute("DELETE FROM BOOK_INFO")

    conn.commit()
        
    conn.close()
    print("Datenbank Kindle geleert")
       



