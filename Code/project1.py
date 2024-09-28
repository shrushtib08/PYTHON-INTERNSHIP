import mysql.connector
from mysql.connector import Error

# Establish a connection to MySQL
mydb = mysql.connector.connect(
    host='localhost',
    user='root',
    password='user'
)

mycursor = mydb.cursor()

class PassportDetails:
    def _init_(self, person_name, pid, urgent, idate, edate):
        self.person_name = person_name
        self.pid = pid
        self.urgent = urgent
        self.idate = idate
        self.edate = edate
        self.price = 200 if urgent else 100

    def _str_(self):
        return f'{self.person_name}, {self.pid}, {self.price}'

class PrintingQueue:
    @staticmethod
    def createDB():
        try:
            mycursor.execute("CREATE DATABASE IF NOT EXISTS Passportprinting;")
            print("Database 'Passportprinting' created successfully or already exists.")
        except mysql.connector.Error as err:
            print(f'Error: {err}')

    @staticmethod
    def useDB():
        try:
            mycursor.execute("USE Passportprinting;")
            print("Using database 'Passportprinting'.")
        except mysql.connector.Error as err:
            print(f'Error: {err}')

    @staticmethod 
    def createPassportTable():
        try:
            mycursor.execute("""
            CREATE TABLE IF NOT EXISTS PassportPrinting(
                name VARCHAR(20),
                pid INT(10) PRIMARY KEY,
                price INT(20),
                idate DATE,
                edate DATE
            );
            """)
            print('Table "PassportPrinting" created successfully or already exists.')
        except mysql.connector.Error as err:
            print(f'Error: {err}')

    @staticmethod
    def insertPassport(details: PassportDetails):
        try:
            sql = "INSERT INTO PassportPrinting (name, pid, price, idate, edate) VALUES (%s, %s, %s, %s, %s)"
            values = (details.person_name, details.pid, details.price, details.idate, details.edate)
            mycursor.execute(sql, values)
            mydb.commit()
            print("Passport details inserted successfully.")
        except mysql.connector.Error as err:
            print(f'Error: {err}')

    @staticmethod
    def updatePassport(pid, new_details: PassportDetails):
        try:
            sql = "UPDATE PassportPrinting SET name = %s, price = %s, idate = %s, edate = %s WHERE pid = %s"
            values = (new_details.person_name, new_details.price, new_details.idate, new_details.edate, pid)
            mycursor.execute(sql, values)
            mydb.commit()
            print("Passport details updated successfully.")
        except mysql.connector.Error as err:
            print(f'Error: {err}')

    @staticmethod
    def deletePassport(pid):
        try:
            sql = "DELETE FROM PassportPrinting WHERE name = %s"
            mycursor.execute(sql, (pid,))
            mydb.commit()
            print("Passport details deleted successfully.")
        except mysql.connector.Error as err:
            print(f'Error: {err}')

pq = PrintingQueue()
pq.createDB()
pq.useDB()
pq.createPassportTable()

passport = PassportDetails("John doe", 123456,False,"2020-01-01", "2025-01-10")
pq.insertPassport(passport)
p1= PassportDetails("sirisha",647884,True , "2020-01-01", "2025-02-16")
pq.insertPassport(p1)
updated_passport = PassportDetails("John doe", 123456, False, "2020-02-01", "2025-02-10")
pq.updatePassport(123456, passport)
pq.deletePassport("shrushti")
mycursor.close()
mydb.close()