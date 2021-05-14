import LarousseEngl as LE
import sqlite3
from Datenbankpfad import pfadDatenbank


Datenbankpfad = pfadDatenbank() + "/Vokabldatebank.sqlite3"
conn = sqlite3.connect(Datenbankpfad)
c = conn.cursor()