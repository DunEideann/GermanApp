import psycopg2
import datetime




class connectDB():
    def __init__(self):
        self.connectionDB = psycopg2.connect(
            database="germanaccounts", user='postgres', password='Holahola12345!', host='localhost', port='5432'
        ) 
        self.connectionDB.autocommit = True

        self.cursor = self.connectionDB.cursor()


    def executeDB(self, sql, message):
        try:
            self.cursor.execute(sql)
            print(message)
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        except:
            print("Something went horribly wrong....")

    def validateDB(self, user=None, mail=None, passw=None):
        sql = '''SELECT USERNAME, PASSWORD, EMAIL from USERS'''
        message = "Validating..."
        self.executeDB(sql, message)
        result = self.cursor.fetchall()

        if user!=None and mail!=None and passw!=None:
            for userName, passWord, eMail in result:
                if user==userName and mail==eMail and passw==passWord:
                    answer = True
                    break
                else:
                    answer = False
            return answer
        elif user!=None and mail!=None:
            for userName, passWord, eMail in result:
                if user==userName and mail==eMail:
                    answer = True
                    break
                else:
                    answer = False
            return answer
        elif user!=None and passw!=None:
            for userName, passWord, eMail in result:
                if user==userName and passw==passWord:
                    answer = True
                    break
                else:
                    answer = False
            return answer
        elif mail!=None and passw!=None:
            for userName, passWord, eMail in result:
                if mail==eMail and passw==passWord:
                    answer = True
                    break
                else:
                    answer = False
            return answer
        elif user!=None:
            for userName, passWord, eMail in result:
                if user==userName:
                    answer = True
                    break
                else:
                    answer = False
            return answer
        elif passw!=None:
            for userName, passWord, eMail in result:
                if passw==passWord:
                    answer = True
                    break
                else:
                    answer = False
            return answer
        elif mail!=None:
            for userName, passWord, eMail in result:
                if mail==eMail:
                    answer = True
                    break
                else:
                    answer = False
            return answer
        else:
            return "You must pass one, two or three options between: user, mail and password."


    def dbCreate(self):
        #CREATE DATABASE
        sql = '''CREATE database german_app''';
        message = "DB sucesfully created...."

        self.executeDB(sql, message)
        # self.connectionDB.close()


    def tableCreate(self):
        #CREATE TABLE
        sql = '''CREATE TABLE USERS(
            USER_ID serial PRIMARY KEY,
            USERNAME VARCHAR(30) UNIQUE NOT NULL,
            PASSWORD VARCHAR(20) NOT NULL,
            EMAIL VARCHAR(40) UNIQUE NOT NULL,
            CREATED_ON TIMESTAMP NOT NULL,
            LAST_LOGIN TIMESTAMP
        )'''
        message = "Table created sucessfully...."
        self.executeDB(sql, message)

        #COMMIT TABLE AND CLOSE
        self.connectionDB.commit()
        # self.connectionDB.close()

    def tableEvaluation(self):
        #CREATE EVALUATION TABLE
        sql = '''CREATE TABLE EVALUATION(
            USER_ID INT PRIMARY KEY,
            CORRECT INT NOT NULL,
            TOTAL INT NOT NULL,
            PERCENTAGE REAL NOT NULL
        )'''
        message = "Evaluation table created successfully..."
        self.executeDB(sql, message)

        #COMMIT TABLE AND CLOSE
        self.connectionDB.commit()
        # self.connectionDB.close()

    def insertUser(self, user, mail, passw):
        user_name = user
        e_mail = mail
        pass_word = passw
        dt = str(datetime.datetime.now()).split(".")[0]
        sql = f'''INSERT INTO USERS(USERNAME, PASSWORD, EMAIL, CREATED_ON, LAST_LOGIN)
         VALUES('{user_name}', '{pass_word}', '{e_mail}', TIMESTAMP '{dt}', TIMESTAMP '{dt}')'''
        message = "Insert added sucessfully...."

        self.executeDB(sql, message)
        self.connectionDB.commit()
        # self.connectionDB.close()

    def insertEvaluation(self, userId, correct, total, percentage):
        user_id = userId
        correct_words = correct
        total_words = total
        percentage_words = percentage
        sql = f'''INSERT INTO EVALUATION(USER_ID, CORRECT, TOTAL, PERCENTAGE)
         VALUES('{user_id}', '{correct_words}', '{total_words}', '{percentage_words}')'''
        message = "Insert evaluation successfully..."

        self.executeDB(sql, message)
        self.connectionDB.commit()

    def updateEvaluation(self, userId, correct, total):
        user_id = userId
        new_correct_words = correct
        new_total_words = total
        sql = f"SELECT CORRECT, TOTAL from EVALUATION WHERE USER_ID = '{user_id}' "
        message = "Old data retrived..."
        self.executeDB(sql, message)
        result = self.cursor.fetchall()
        
        for correctAnswer, totalAnswer in result:
            finalCorrect = correctAnswer + new_correct_words
            finalTotal = totalAnswer + new_total_words
        finalPercentage = finalCorrect*100/finalTotal

        sql = f"UPDATE EVALUATION SET CORRECT = {finalCorrect}, TOTAL = {finalTotal}, PERCENTAGE = {finalPercentage} WHERE USER_ID = {user_id}"
        message = "Updated data..."
        self.executeDB(sql, message)
        self.connectionDB.commit()


    def checkEvaluationExist(self, userId):
        user_id = userId
        sql = f"SELECT USER_ID FROM EVALUATION"
        message = "Searching for user id..."
        self.executeDB(sql, message)
        result = self.cursor.fetchall()
        existence = False
        
        for existingUserId in result:
            if existingUserId[0]==user_id:
                existence = True
                break
            else:
                existence = False 

        return existence

    def getData(self, userId):
        result = []
        user_id = userId
        sql = f"SELECT CORRECT, TOTAL, PERCENTAGE from EVALUATION WHERE USER_ID = '{user_id}' "
        message = "Searching data for user id..."
        self.executeDB(sql, message)
        result1 = self.cursor.fetchall()

        sql = f"SELECT USERNAME, EMAIL from USERS WHERE USER_ID = '{user_id}' "
        message = "Searching data for user id..."
        self.executeDB(sql, message)
        result2 = self.cursor.fetchall()

        result.append(result1[0][0])
        result.append(result1[0][1])
        result.append(result1[0][2])
        result.append(result2[0][0])
        result.append(result2[0][1])

        return result

    def loginDB(self, user, passw):
        user_name = user
        pass_word = passw

        #QUERY USERNAME AND PASSWORD FROM TABLE USERS
        sql = '''SELECT USERNAME, PASSWORD from USERS'''
        message = "Logging...."
        self.executeDB(sql, message)
        result = self.cursor.fetchall()

        #CHECK FOR MATCHES IN PASS AND USER
        for userName, passWord in result:
            if user_name == userName and pass_word == passWord:
                logMessage = "Log in succesfull"
                result = True
                break
            else:
                logMessage = "Usuario y/o contraseña incorrectos"
                result = False

        print(logMessage)
        return result

    def deleteDB(self, user):
        user_name = user
        tableName = 'USERS'
        sql = f'''DELETE FROM {tableName} WHERE USERNAME='{user_name}' ''';
        message = f"Usuario {user_name} borrado de tabla {tableName}"
        self.executeDB(sql, message)
        #COMMIT INSERT AND CLOSE
        self.connectionDB.commit()
        # self.connectionDB.close()


    def obtainID(self, user=None, mail=None):
        if user!=None:
            sql = '''SELECT USERNAME, USER_ID from USERS'''
            message = f"For user: {user} we obtain the user id"
        elif mail!=None:
            sql = '''SELECT EMAIL, USER_ID from USERS'''
            message = f"For mail: {mail} we obtain the user id"
        else:
            message = "Must pass user or mail to function."
        self.executeDB(sql, message)
        result = self.cursor.fetchall()

        for user_email, user_id in result:
            if user_email==user or user_email==mail:
                userId = user_id
                break

        return userId






#conexion = connectDB()
#conexion.dbCreate()
#conexion.insertUser('test3', 'test3@test.test', 'ptest3')
#print(datetime.datetime.now())
#conexion.loginDB('test1', 'ptest1')
#conexion.deleteDB('ger3')