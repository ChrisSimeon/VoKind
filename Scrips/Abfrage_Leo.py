def Abfrage_Leo(word, lang=0):
    # imports
    import requests
    from bs4 import BeautifulSoup
    import unicodedata
    from Linguee_Transl import request_Linguee

    # variables
    baseurl = "https://dict.leo.org/französisch-deutsch/"
    DatabaseLeo = {"word": word, "German": "", "French": ""}
    # lang = 1 is from German to French
    # lang = 0  is French to German

    # Get the Site
    url = baseurl + str(word)
    r = requests.get(url)

    if r.status_code == 200:
        src = r.content
        soup = BeautifulSoup(src, "html5lib")
        soup = soup.find('tbody')
        if soup:
            if lang == 0:
                for tr in soup.find_all('tr')[0:5]:
                    td = tr.find("td", {"lang": "de"})
                    if td:
                        DatabaseLeo["German"] += unicodedata.normalize(
                            "NFKD", td.text) + " \n "
                    else:
                        buff = request_Linguee(word)
                        if buff:
                            DatabaseLeo["German"] = buff["Translation"]
                        return DatabaseLeo

            elif lang == 1:
                for tr in soup.find_all('tr')[0:5]:
                    td = tr.find("td", {"lang": "fr"})
                    if td:
                        DatabaseLeo["French"] += unicodedata.normalize(
                            "NFKD", td.text) + " \n "
                    else:
                        DatabaseLeo["French"] = request_Linguee(word)["Translation"]
                        return DatabaseLeo

    return DatabaseLeo


