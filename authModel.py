import os
import json

# pip install psycopg2
import psycopg2

#pip install -U python-dotenv
from dotenv import load_dotenv
load_dotenv()

# pip install pyjwt
import jwt

from authPayload import authPayload 
from authResponse import authResponse

# Get environment variables
DBNAME = os.getenv('DBNAME')
DBUSER = os.getenv('DBUSER')
DBPASSWORD = os.getenv("DBPASSWORD")
AUTHSECRET = os.getenv("AUTHSECRET")
EXPIRESSECONDS = os.getenv('EXPIRESSECONDS')

def authenticate(clientId, clientSecret):

    conn = None
    query = "select * from clients where \"ClientId\"='" + clientId + "' and \"ClientSecret\"='" + clientSecret + "'"
    try:
        conn = psycopg2.connect("dbname=" + DBNAME + " user=" + DBUSER +" password=" +DBPASSWORD)
        cur = conn.cursor()
        cur.execute(query)
        rows = cur.fetchall()
        isAdmin = False

        if cur.rowcount == 1:
            for row in rows:
                isAdmin = row[3]
                payload = authPayload(row[0],row[1], isAdmin)
                break

            encoded_jwt = jwt.encode(payload.__dict__, AUTHSECRET, algorithm='HS256')
            response = authResponse(encoded_jwt,EXPIRESSECONDS, isAdmin)
            
            return response.__dict__
        else:
            return False
        
    except (Exception, psycopg2.DatabaseError) as error:
        
        print(error)
        if conn is not None:
            cur.close()
            conn.close()

        return False
    finally:
        if conn is not None:
            cur.close()
            conn.close()

def verify(token):
    try:
        isBlacklisted = checkBlacklist(token)
        if isBlacklisted == True:
             return {"success": False}
        else:
            decoded = jwt.decode(token, AUTHSECRET, algorithms=['HS256'])
            return decoded
    except (Exception) as error:
        print(error)
        return {"success": False}

def create(clientId, clientSecret, isAdmin):
    conn = None
    query = "insert into clients (\"ClientId\", \"ClientSecret\", \"IsAdmin\") values(%s,%s,%s)"

    try:
        conn = psycopg2.connect("dbname=" + DBNAME + " user=" + DBUSER +" password=" +DBPASSWORD)
        cur = conn.cursor()
        cur.execute(query, (clientId ,clientSecret,isAdmin))
        conn.commit()
        return True
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        if conn is not None:
            cur.close()
            conn.close()

        return False
    finally:
        if conn is not None:
            cur.close()
            conn.close()

def blacklist(token):
    conn = None
    query = "insert into blacklist (\"token\") values(\'" + token +"\')"
    try:
        conn = psycopg2.connect("dbname=" + DBNAME + " user=" + DBUSER +" password=" +DBPASSWORD)
        cur = conn.cursor()
        cur.execute(query)
        conn.commit()
        return True
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        if conn is not None:
            cur.close()
            conn.close()

        return False
    finally:
        if conn is not None:
            cur.close()
            conn.close()

def checkBlacklist(token):
    conn = None
    query = "select count(*) from blacklist where token=\'" + token + "\'"
    print(query)
    try:
        conn = psycopg2.connect("dbname=" + DBNAME + " user=" + DBUSER +" password=" +DBPASSWORD)
        cur = conn.cursor()
        cur.execute(query)
        result = cur.fetchone()
        if result[0] == 1:
            return True
        else:
            return False
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        if conn is not None:
            cur.close()
            conn.close()

        return True
    finally:
        if conn is not None:
            cur.close()
            conn.close()
