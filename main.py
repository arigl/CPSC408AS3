import sqlite3
import pandas as pd
from pandas import DataFrame

# Connect to SQL Server
conn = sqlite3.connect('/Users/alexrigl/PycharmProjects/pythonProject/StudentDB.sqlite')
cursor = conn.cursor()

def initTable():
    cursor.execute("DROP TABLE Student")
    cursor.execute("CREATE TABLE Student "
               "(StudentID INTEGER PRIMARY KEY,"
               "FirstName TEXT,"
               "LastName TEXT,"
               "GPA REAL,"
               "Major TEXT,"
               "FacultyAdvisor TEXT,"
               "Address TEXT,"
               "City TEXT,"
               "State TEXT,"
               "ZipCode TEXT,"
               "MobilePhoneNumber TEXT,"
               "isDeleted INTEGER)"
               )

def chooseOption():
    choice = int(input("0) Create Table, 1) Import CSV, 2)Display All students, 3)Add Student, 4)Update Student, 5)Delete Student, 6)Search for Student, 7)To exit:  "))
    if (choice == 0):
        initTable()
    elif (choice == 1):
        insertCSV()
    elif (choice == 2):
        showStudents()
    elif (choice == 3):
        addStudent()
    elif (choice == 4):
        updateStudent()
    elif (choice == 5):
        deleteStudent()
    elif (choice == 6):
        searchStudent()
    elif (choice == 7):
        exit()
    else:
        print("Try again")


def insertCSV():
    df = pd.read_csv("students.csv")
    df.to_sql("Student", conn, if_exists='append', index=False)
    chooseOption()

def showStudents():
    cur = conn.execute('''SELECT * FROM Student;''')
    df = DataFrame(cur,columns = ['StudentId','FirstName','LastName', 'GPA', 'Major', 'FacultyAdvisor', 'Address', 'City',
                                  'State', 'ZipCode', 'MobilePhoneNumber','isDeleted'])
    print(df)
    chooseOption()

def addStudent():
    sID = int(input("What is the StudentID: "))
    fName = input("What is the student's first name?: ")
    lName = input("What is the student's last name?: ")
    GPA = float(input("What is the student's GPA?: "))
    Major = input("What is the students major?: ")
    FA = input("What is the students advisor?: ")
    Address = input("What is the student's address?: ")
    City = input("What is the students city?: ")
    State = input("What is the students state?: ")
    Zipcode = input("What is the students zip-code?: ")
    MPN = int(input("What is the students phone number?: "))
    sql = """INSERT INTO Student(
       StudentID, FirstName, LastName, GPA, Major, FacultyAdvisor, Address, City, State, ZipCode, MobilePhoneNumber,isDeleted)
       VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"""
    conn.execute(sql, (sID, fName, lName, GPA, Major, FA, Address, City, State, Zipcode, MPN, 0))
    chooseOption()

def updateStudent():
    sID = int(input("What is the student's id?: "))
    choice = int(input("Would you like to: 1)Update Major 2)Update Advisor 3)Phone Number: "))
    if (choice == 1):
        major = input("What is the major you would like it to be changed to? :")
        sql = "UPDATE Student SET Major = ? WHERE StudentID = ?"
        conn.execute(sql, (major,sID))
    elif (choice == 2):
        advisor = input("Who is the new advisor?: ")
        sql = "UPDATE Student SET FacultyAdvisor = ? WHERE StudentID = ?"
        conn.execute(sql, (advisor, sID))
        print(advisor)
    elif (choice == 3):
        number = input("What is the new phone number?: ")
        sql = "UPDATE Student SET MobilePhoneNumber = ? WHERE StudentID = ?"
        conn.execute(sql, (number, sID))
        print(number)
    else:
        print("incorrect input")
        updateStudent()
    chooseOption()


def deleteStudent():
    choice = input("Which student(ID) would you like to delete?: ")
    sql = "UPDATE Student SET isDeleted = 1 WHERE StudentID = ?"
    conn.execute(sql, (choice,))
    print("Delete Student")
    chooseOption()


def searchStudent():
    student = int(input("Search student by:  Major(1), GPA(2), City(3), State(4), Advisor(5) "))
    if (student == 1):
        print("Major")
        major = input("What major are you looking for?: ")
        sql = "SELECT * FROM Student WHERE Major = ?"
        conn.execute(sql, (major,))

        myresult = conn.fetchall()
        for x in myresult:
            print(x)

    if (student == 2):
        print("GPA")
        gpa = float(input("What GPA are you looking for?: "))
        sql = "SELECT * FROM Student WHERE GPA = ?"
        conn.execute(sql, (gpa,))

        myresult = conn.fetchall()
        for x in myresult:
            print(x)
    if (student == 3):
        print("City")
        city = input("What City are you looking for?: ")
        sql = "SELECT * FROM Student WHERE City = ?"
        conn.execute(sql, (city,))

        myresult = conn.fetchall()
        for x in myresult:
            print(x)
    if (student == 4):
        print("State")
        state = input("What State are you looking for?: ")
        sql = "SELECT * FROM Student WHERE State = ?"
        conn.execute(sql, (state,))

        myresult = conn.fetchall()
        for x in myresult:
            print(x)
    if (student == 5):
        print("Advisor")
        adv = input("What advisor are you looking for?: ")
        sql = "SELECT * FROM Student WHERE FacultyAdvisor = ?"
        conn.execute(sql, (adv,))

        myresult = conn.fetchall()
        for x in myresult:
            print(x)
    chooseOption()

#Method Calling
chooseOption()

conn.commit() #uploads changes to DB
