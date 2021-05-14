import pickle


def createDatabase():
    Datenbankpfad= input("Bitte den Pfad angeben, in dem die Datebank erstellt werden soll.")
    Data = {"Datenbank": Datenbankpfad}
    pickle_out = open("Data.pckl", "wb") 
    pickle.dump(Data, pickle_out)
    pickle_out.close()


def pfadDatenbank():
    try:
        pickle_in = open("Data.pckle", "rb")
        return pickle.load(pickle_in)["Datenbank"]
    except:
        createDatabase()



if __name__ == "__main__":
    createDatabase()