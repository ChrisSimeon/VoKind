import DB_Functions as DB
import multiprocessing

def Definition():
    DB.Abfrage_Larousse(DB.DatenbankabfrageDefinition()) 

def Translation():
    DB.Abfrage_Leo(DB.DatenbankabfrageTranslation())


if __name__ == '__main__':
    p1 = multiprocessing.Process(target=Definition)  
    p2 = multiprocessing.Process(target=Translation) 


    p1.start()
    p2.start()

    p1.join()
    p2.join()


    print("Translation und Definition wurden in Datenbank ergänzt")