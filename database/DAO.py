from database.DB_connect import DBConnect
from model.fermata import Fermata
from model.connessione import Connesione

class DAO():

    @staticmethod
    def getAllEdgesPesati():
        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)
        query = """SELECT id_stazP, id_stazA, count(*) as peso
        FROM connessione c
        group by id stazP, id_stazA
        order by peso desc"""
        cursor.execute(query)
        for row in cursor:
            result.append((row["idP"], row["idA"], row["peso"]))


    @staticmethod
    def getAllFermate():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = "SELECT * FROM fermata"
        cursor.execute(query)

        for row in cursor:
            result.append(Fermata(**row))
        cursor.close()
        conn.close()
        return result

    @staticmethod
    def hasconn(u:Fermata, v:Fermata):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = "select * from connessione c where c.id_stazP = %s and c.id_stazA = %s"
        cursor.execute(query, (u.id_fermata, v.id_fermata))

        for row in cursor:
            result.append(row)
        cursor.close()
        conn.close()
        return len(result) > 0

    @staticmethod
    def getvicini(u:Fermata):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = "select * from connessione c where c.id_stazP = %s"
        cursor.execute(query, (u.id_fermata,))

        for row in cursor:
            result.append(Connesione(**row))
        cursor.close()
        conn.close()
        return result


    @staticmethod
    def getAllEdges():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = "SELECT * FROM connessione c "
        cursor.execute(query)

        for row in cursor:
            result.append(Connesione(**row))
        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getAllEdgesV():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """SELECT c.id_stazP, c.id_stazA, max(l.velocità) as v
        FROM connessione c, linea l
        WHERE l.id_linea = c.id_linea
        GROUP BY c.id_stazP, c.id_stazA
        ORDER BY v asc"""
        cursor.execute(query)

        for row in cursor:
            result.append((row["id_stazP"], row["id_stazA"], row["v"]))
        cursor.close()
        conn.close()
        return result
