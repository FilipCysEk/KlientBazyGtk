import mysql.connector
import datetime
from mysql.connector import errorcode, FieldType

from error import *

class MainModel:
    def __init__(self):
        self.connection = None
        pass

    def testConnection(self, user, host, passw, database):
        #return True
        try:
            if database == None or database == '':
                raise ErrorClass(1, "Błąd połączenia", "Nie podano bazy danych")

            connection = mysql.connector.connect(host=host, user=user, password=passw, database=database)
            connection.close()
            return True

        except mysql.connector.Error as err:
            #return True
            return err
            print(err)
        except ErrorClass as err:
            return err
            print(err)

    def makeConnection(self, user, host, passw, database):
        #return True
        try:
            self.connection = mysql.connector.connect(host=host, user=user, password=passw, database=database)
            return True

        except mysql.connector.Error as err:
            #return True
            raise ErrorClass(1, "Błąd połączenia", "Błąd tworzenia połączenia z bazą danych", str(err))
            return err

    def closeConnection(self):
        if self.connection == 0:
            raise ErrorClass(0, "Błąd zamykania połączenia", "Próbowano zamknąć połączenie, któ©e nie zostało otwarte")
        else:
            self.connection.close()

    def getTableList(self):
        if self.connection == 0:
            raise ErrorClass(0, "Błąd połączneia", "Brak połączenia z bazą!!", "Przy pobieraniu tabeli")
        else:
            try:
                #self.connection = mysql.connector.connect(host=host, user=user, password=passw, database=database)
                query = "SHOW TABLES"
                cursor = self.connection.cursor()

                cursor.execute(query)
                result = cursor.fetchall()
                #print(result)

                cursor.close()
                return result
            except mysql.connector.Error as err:
                raise ErrorClass(0, "Błąd zapytania", str(err))

    def createTable(self, data, tableName):
        if data == None or len(data) == 0 or len(tableName) == 0:
            raise ErrorClass(0, "Błąd danych", "Brak danych", "Błąd przekazanych danych do funkcji")
        else:
            try:
                sql = "CREATE TABLE "
                sql += tableName
                sql += " ("
                for row in data:
                    sql += row[0]
                    sql += " "
                    sql += row[1]
                    if len(row[2]) != 0:
                        sql += "("
                        sql += row[2]
                        sql += ")"
                    sql += ", "

                sql = sql[:len(sql) - 2]
                sql += ")"
                #print(sql)

                cursor = self.connection.cursor()

                cursor.execute(sql)

            except mysql.connector.Error as err:
                raise ErrorClass(0, "Błąd zapytania", str(err))
                return False

            return True

    def SelectAll(self, table):
        if table == None or len(table) == 0:
            raise ErrorClass(1, "Błąd komunikacji w programie", "Błąd!!", "Nieprzekazano nazwy tabeli, z której mamy wyciągnąć dane")
        try:
            sql = "SELECT * FROM "
            sql += table

            cursor = self.connection.cursor()
            cursor.execute(sql)
            result = cursor.fetchall()
            colnames = cursor.column_names
            fieldTypes = []
            #print(result)
            #print(colnames)

            #typy kolumn
            for desc in cursor.description:
                fieldTypes.append(FieldType.get_info(desc[1]))

            cursor.close()
            return (colnames, result, fieldTypes)

        except mysql.connector.Error as err:
            raise ErrorClass(0, "Błąd zapytania", str(err))
            return False

    def deleteTable(self, tableName):
        if tableName == None or len(tableName) == 0:
            raise ErrorClass(0, "Błąd danych", "Brak danych", "Błąd przekazanych danych do funkcji")
        else:
            try:
                sql = "DROP TABLE "
                sql += tableName

                cursor = self.connection.cursor()

                cursor.execute(sql)

            except mysql.connector.Error as err:
                raise ErrorClass(0, "Błąd zapytania", str(err))
                return False

            return True

    def deleteRow(self, tableName, rowData, rowTitle):
        '''
        Function deleted row in table
        :param tableName: Name of table
        :param rowData: data existing in row
        :param rowTitle: column names
        :return:
        '''
        if tableName == None or len(tableName) == 0 or rowData == None or len(rowData) == 0 or rowTitle == None or len(rowTitle) == 0:
            raise ErrorClass(0, "Błąd danych", "Brak danych", "Błąd przekazanych danych do funkcji")
        else:
            try:
                sql = "DELETE FROM "
                sql += tableName
                sql += " WHERE "

                for i in range(len(rowData)):
                    print(type(rowData[i]))
                    sql += rowTitle[i]\
                    #+ "="
                    if rowData[i] == None:
                        sql += " IS NULL"
                    elif isinstance(rowData[i], str):
                        sql += "='" + rowData[i] + "'"
                    elif isinstance(rowData[i], datetime.date):
                        sql += "='" + str(rowData[i]) + "'"
                    else:
                        sql += "=" + str(rowData[i])

                    sql += " AND "

                sql = sql[:-5]
                print(sql)


                cursor = self.connection.cursor()

                cursor.execute(sql)

            except mysql.connector.Error as err:
                raise ErrorClass(0, "Błąd zapytania", str(err))
                return False

            return True

