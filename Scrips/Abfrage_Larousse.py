# -*- coding: utf-8 -*-


def get_Larousse(word):
    #Import
    import requests
    from bs4 import BeautifulSoup
    import unicodedata 
    import Levenshtein_Distance as LD
    from DB_Functions import word_not_found


    word = unicodedata.normalize("NFC", word)
    # Variablen
    baseurl = "https://www.larousse.fr/dictionnaires/francais/"
    DatabaseLarousse = {"word": word, "Infinitiv": "", "Definitions": "", "Expressions": "", "Difficultes": "", "LinguisticDef": "", "Origin": "", "LinkPronouciation": "", "URL": ""}
    #Get the Site
    url = baseurl + str(word)
    DatabaseLarousse["URL"] = url
    r = requests.get(url)
    #print(r.encoding)
    #print(r.status_code)

    if r.status_code == 200:
        src = r.content
        soup = BeautifulSoup(src, "html5lib")

        #infinitiv  
        Infinitiv = soup.find("h2", { "class": "AdresseDefinition"})
        if Infinitiv:
            DatabaseLarousse["Infinitiv"] = Infinitiv.text.replace("", "")
        else:
            print("Wort nicht gefunden:" + DatabaseLarousse["word"])
            Error_Vorschläge = soup.find('section', {"class": "corrector"})
            cd = {}
            for li in Error_Vorschläge.find_all("a"):
                bd = LD.levenshtein_ratio_and_distance(word, li.text, ratio_calc=True)
                cd.update({li.text: bd})
            dc = max(cd, key=cd.get)
            if cd[dc] > 0.90:
                url = baseurl + dc
                print(dc)
                DatabaseLarousse["URL"] = url
                r = requests.get(url)
                if r.status_code == 200:
                    src = r.content
                    soup = BeautifulSoup(src, "html5lib")
                    src = r.content
                    soup = BeautifulSoup(src, "html5lib")
                    Infinitiv = soup.find("h2", { "class": "AdresseDefinition"})
                    if Infinitiv:
                        DatabaseLarousse["Infinitiv"] = Infinitiv.text.replace("", "")
                    else:
                        print("Wort entgültig nicht gefunden (Errorvorschläge durchlaufen):" + DatabaseLarousse["word"])
                        word_not_found(DatabaseLarousse["word"])

                        return None
                elif r.status_code == 301:
                    print(r.is_permanent_redirect())
                    print(r.headers)
                    print(r.__attrs__)
                else:
                    print("Internetverbindung Fehlerhaft oder Wort nicht gefunden bei " + word)
                    word_not_found(DatabaseLarousse["word"])
                    return None
            else:
                print("Kein passender Error vorschlag")
                word_not_found(DatabaseLarousse["word"])
                return None
        
            

        #Definitions
        Definitions = soup.find('ul', { 'class': 'Definitions' })
        if Definitions:
            for li in Definitions.find_all("li")[0:5]:
                if li:
                    DatabaseLarousse["Definitions"]+= unicodedata.normalize("NFKD", li.text) + " \n "
                else:
                    pass
        else:
            pass


        #Expressions
        Expressions = soup.find('ul', { 'class': 'ListeLocutions' })
        if Expressions:
            ba = Expressions.find_all('li')
            for li in ba[0:5]:
                ca = li.find("h2", {"class": "AdresseLocution"}).text + li.find("span", {"class", "TexteLocution"}).text
                DatabaseLarousse["Expressions"]+= (ca) + " \n"
        else:
            pass
        
        #Difficultes
        Schwierigkeiten = soup.find('div', { 'id': 'difficulte' })
        if Schwierigkeiten:
            for li in Schwierigkeiten.find_all('li'):
                for p in li.find_all("p"):
                    DatabaseLarousse["Difficultes"] += unicodedata.normalize("NFKD", p.text) + "\n"
        else:
            pass


        #Linguistic Definition
        LingDef = soup.find("p", { "class": "CatgramDefinition"})
        if LingDef:
            DatabaseLarousse["LinguisticDef"] = LingDef.text.replace("CONJUGAISON","")
            # hier ließe sich bei Verben der Link zur Konjugation herbekommen/ evtl ließen sich sogar bei Verben automatisch die wichtigsten konjugationen hinzufügen
        else:
            pass

        # Word Origin
        origin = soup.find("p", { "class": "OrigineDefinition"})
        if origin:
            DatabaseLarousse["Origin"] = origin.text
        else:
            pass

        #Link to Pronounciation mp3
        pronounce = soup.find("span", { "class": "linkaudio fontello"})
        if pronounce:
            pronounce = pronounce.attrs
            audioID = pronounce["onclick"].replace("onSpeaker('","").replace("')","")
            DatabaseLarousse["LinkPronouciation"] =  "https://www.larousse.fr/dictionnaires-prononciation/francais/tts/" + audioID
        else:
            pass

        
        return DatabaseLarousse
        


    else:
        print("Internetverbindung Fehlerhaft oder Wort nicht gefunden bei " + word)
        return None


