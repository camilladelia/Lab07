from database.DB_connect import DBConnect
from model.libro_DTO import Libro

"""
    LIBRO DAO
    Gestisce le operazioni di accesso al database relative ai libri (Effettua le Query).
"""

class LibroDAO:
    def __init__(self):
        pass

    def get_generi (self)-> list[str] | None:
        cnx= DBConnect.get_connection()
        if cnx is None:
            return None

        cursor = cnx.cursor(dictionary=True)
        query= "SELECT DISTINCT genere FROM libro"
        cursor.execute(query)

        generi=[]
        for row in cursor.fetchall():
            generi.append(row["genere"])

        cursor.close()
        cnx.close()
        return generi

    def get_libri_filtrati(self,biblioteca: str, genere: str) -> list[Libro] | None:
        cnx= DBConnect.get_connection()
        if cnx is None:
            return None

        cursor = cnx.cursor(dictionary=True)
        query= """
            SELECT l.*
            FROM libro l, biblioteca b
            WHERE l.id_biblioteca=b.id
            AND b.nome=COALESCE(%s, b.nome)
            AND l.genere= COALESCE(%s, l.genere)
        """
        cursor.execute(query, (biblioteca, genere))

        libri= []
        for row in cursor.fetchall():
            libro=Libro(
                row["id"],
                row["titolo"],
                row["autore"],
                row["genere"],
                row["anno_pubblicazione"],
                row["id_biblioteca"]
            )
            libri.append(libro)

        cursor.close()
        cnx.close()
        return libri