import LarousseEngl as LE
import sqlite3

Datenbankpfad = "/Users/chris/Documents/OneDrive/Christian/Sprachen/ProgrammVokabeln/Datenbank/Vokabldatebank.sqlite3"
conn = sqlite3.connect(Datenbankpfad)
c = conn.cursor()