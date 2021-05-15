import pickle
import os


def createDatabase():
    Datenbankpfad= input("Bitte den Pfad angeben, in dem die Datebank erstellt werden soll. \n") + "/Vokabldatebank.sqlite3"
    if Datenbankpfad == "/Vokabldatebank.sqlite3":
        Datenbankpfad = "./Database/Vokabldatebank.sqlite3"
    Data = {"Datenbank": Datenbankpfad}
    newpath = "./Database"
    if not os.path.exists(newpath):
        os.makedirs(newpath)
    pickle_out = open("./Database/Data.pckl", "wb") 
    pickle.dump(Data, pickle_out)
    pickle_out.close()
    


def pfadDatenbank():
    try:
        pickle_in = open("./Database/Data.pckl", "rb")
        
    except:
        createDatabase()
        pickle_in = open("./Database/Data.pckl", "rb")
    
    return pickle.load(pickle_in)["Datenbank"]
    




if __name__ == "__main__":
    createDatabase()