import json
import urllib.request
import unicodedata
from Datenbankpfad import pfadDatenbank



# Fehler mit dem Encoding{'result': None, 'error': "'ascii' codec can't encode character '\\xf6' in position 16: ordinal not in range(128)"}
# Ich hab jetzt die alten Vokabln aus vokabs_all datenbank mit in die neue Datenbank mitaufgenommen, die Dinger sind aber seltsam encoded

# def request(action, **params):
#     return {'action': action, 'params': params, 'version': 6}

# def addcart(Karte): #Karte als Dict, Felder müssen mit Anki übereintimmen
# 	return 	{"action": "addNote","version": 6,"params": {"note": {"deckName": "test1","modelName": "Larousse Vokabs","fields": {"Front": "front content","Back": "back content"},"options": {"allowDuplicate": False,"duplicateScope": "deck","duplicateScopeOptions": {"deckName": "test1","checkChildren": False}}, "tags": ["test"],"audio": [{"url": "https://voix.larousse.fr/francais/66235fra2.mp3","filename": "66235fra2.mp3","skipHash": "7e2c2f954ef6051373ba916f000168dc","fields": ["Front"]}]}}}


def Datenbankabfrage_Anki():
    import sqlite3
    import time

    conn = sqlite3.connect(pfadDatenbank())
    c = conn.cursor()
    c.execute("Select Translation.Translation, Definition.Infinitiv, Definition.Origin, Definition.Definitions, Incoming.usage, Incoming.book, Definition.Expressions, Incoming.wordcount, Definition.LinguisticDef, Definition.LarousseLink, Definition.Diffucultes, Definition.LinkPronounciation FROM Definition JOIN Incoming ON Incoming.words = Definition.words JOIN Translation  ON Translation.words = Definition.words Where Definition.LinkPronounciation is NULL")
    ab = c.fetchall()
    counter = 0
    for i in ab:
        counter += 1
        print (str(counter) + " / " + str(len(ab)) )
        i = list(i)
        for c in i:
            if c == None:
                c = ""
        a = {"Deutsch": i[0], "Französisch": i[1], "Herkunft": i[2], "Erklärung Franz": i[3], "Textstelle": i[4], "Buch": i[5],"Expressions": i[6], "Anzahl der Abfragen": str(i[7]), "Linguistic_Def": i[8], "Larousse_Link": i[9], "Schwierigkeiten": i[10]}
        filename = i[1] + ".mp3"
        soundfile = i[11]
        #print(a)
        if int(i[7]) >= 5:
            deckname = "Französisch::1"
        elif int(i[7]) == 4:
            deckname = "Französisch::2"
        elif int(i[7]) == 3:
            deckname = "Französisch::3"
        elif int(i[7]) == 2:
            deckname = "Französisch::4"
        else:
            deckname = "Französisch::5"
        print(deckname)
        
        # Überprüfung, ob Karte schon existiert
        request = {"action": "findNotes", "version": 6, "params": {"query": "deck:Französisch Französisch:{vokab}".format(vokab= i[1])}}
        requestJson = json.dumps(request).encode('utf-8')
        try:
            response1 = json.load(urllib.request.urlopen(
                urllib.request.Request('http://localhost:8765', requestJson)))
        except urllib.error.URLError:
            print("Please Open Anki")
            return
        
        request = {"action": "findNotes", "version": 6, "params": {"query": "deck:Französisch Französisch:{vokab}*".format(vokab= i[1])}}
        requestJson = json.dumps(request).encode('utf-8')
        try:
            response2 = json.load(urllib.request.urlopen(
                urllib.request.Request('http://localhost:8765', requestJson)))
        except urllib.error.URLError:
            print("Please Open Anki")
            return

        
        
        
        
        
        if response['error'] is None:
            ## Szenario 3: Karte existiert nicht -> response1=0, reponse2=0, no error
            if response1["result"] == [] and response2["result"] == []:
                if i[11]:
                    request = {"action": "addNote", "version": 6, "params": {"note": {"deckName": deckname, "modelName": "Larousse Vokabs", "fields": a, "options": {"allowDuplicate": False, "duplicateScope": "deck", "duplicateScopeOptions": {
                        "deckName": "Französisch", "checkChildren": True}}, "tags": [""], "audio": [{"url": soundfile, "filename": filename, "skipHash": "7e2c2f954ef6051373ba916f000168dc", "fields": ["Französisch"]}]}}}
                else:
                    request = {"action": "addNote", "version": 6, "params": {"note": {"deckName": deckname, "modelName": "Larousse Vokabs", "fields": a, "options": {"allowDuplicate": False, "duplicateScope": "deck", "duplicateScopeOptions": {
                    "deckName": "Französisch", "checkChildren": True}}, "tags": [""]}}}
                requestJson = json.dumps(request).encode('utf-8')
                #hier fehlt noch die request
            ## Szenario 1: Karte existiert und hat keine Prononciation -> response1=1, response2=id, no error
            elif len(response1["result"]) == 1:
                request = {"action": "updateNoteFields", "version": 6, "params": {"note": { "id": response1['result'], "fields": a , "audio": [{"url": soundfile, "filename": filename, "skipHash": "7e2c2f954ef6051373ba916f000168dc", "fields": ["Französisch"]}]}}}
                requestJson = json.dumps(request).encode('utf-8')
                response = json.load(urllib.request.urlopen(urllib.request.Request('http://localhost:8765', requestJson)))
                request = {"action": "changeDeck", "version": 6, "params": {"cards": response1['result'], "deck": deckname}}
                requestJson = json.dumps(request).encode('utf-8')
                response = json.load(urllib.request.urlopen(urllib.request.Request('http://localhost:8765', requestJson)))
                

            ##Szenario 2: Karte existiert und hat Prononciation -> response1=1, response2=1, no error
            elif len(response2["result"]) == 1  and response1["result"] == []:
                request = {"action": "updateNoteFields", "version": 6, "params": {"note": { "id": response2['result'], "fields": {"Textstelle": a["Textstelle"], "Buch": a["Buch"]}}}}
                requestJson1 = json.dumps(request).encode('utf-8')
                response = json.load(urllib.request.urlopen(urllib.request.Request('http://localhost:8765', requestJson)))
                request = {"action": "changeDeck", "version": 6, "params": {"cards": response2['result'], "deck": deckname}}
                requestJson1 = json.dumps(request).encode('utf-8')
                response = json.load(urllib.request.urlopen(urllib.request.Request('http://localhost:8765', requestJson)))


            
            ## Szenatio 4: Es werden mehrere Ids zurückgegeben
            else:
                print("Found Multiple Cards on the Duplicate Search Parameters Card ids: " + response2["result"] + " , " + response2["result"])


            if len(response['result']) == 1:
                pass
            elif:
                    len(response['result']) > 1:
                
            else: 
                print("Search Parameters don't seem to find a Card eventought it is in the Duplicate loop")
            #c.execute('INSERT INTO AC_Error_Dubplicates VALUES (":Deutsch", ":Infinitiv")',{"Deutsch": i[0], "Infinitiv": i[1]})


        ## Szenario 4: Error
        else:
        if len(response) != 2:
            print('response has an unexpected number of fields')
        if 'error' not in response:
            print('response is missing required error field')
        if 'result' not in response:
            print('response is missing required result field')
        raise Exception: 
                (print(response1["error"]) + " " + print(response2["error"])
        


    

        if not response["result"] == [] and len(response["result"]) == 1 and not response["error"]: 
            
        ## Szeanario 2
        elif response["result"] == [] and not response["error"]:
            if response["result"] and len(response["result"]) == 1 and not response["error"]:

            elif response["result"] == [] and not response["error"]:
                

        # print(requestJson)
                print("Duplicate, ist eingetragen")
                request = {"action": "findNotes", "version": 6, "params": {"query": "deck:Französisch {vokab}".format(vokab= i[1][0:10])}}
                requestJson = json.dumps(request).encode('utf-8')
                response = json.load(urllib.request.urlopen(urllib.request.Request('http://localhost:8765', requestJson)))
                print(response)

            elif response['error'] == 'cannot create note because it is empty':
                pass
            else:
                raise Exception(response['error'])
        print(response['result'])
        time.sleep(10)
        
    conn.close()
    return


def invoke(action, **params):
    try:
        requestJson = json.dumps(addcart("Karte")).encode('utf-8')
        response = json.load(urllib.request.urlopen(
            urllib.request.Request('http://localhost:8765', requestJson)))
    except:
        print("Please start Anki")
        return "Please start Anki"

    if len(response) != 2:
        raise Exception('response has an unexpected number of fields')
    if 'error' not in response:
        raise Exception('response is missing required error field')
    if 'result' not in response:
        raise Exception('response is missing required result field')
    if response['error'] is not None:
        raise Exception(response['error'])
    return response['result']



if __name__ == "__main__":
    Datenbankabfrage_Anki()
