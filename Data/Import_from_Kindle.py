import DB_Functions as DB
import Kindle_Functions

buff = DB.get_Vokabeln()

if buff ==0:
    Kindle_Functions.Kindle_leeren()
else:
    print("Fehler, Kindle nicht geleert")