import os
import json
#import base64

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

        if cur.rowcount == 1:

            for row in rows:
                payload = authPayload(row[0],row[1])
                break

            encoded_jwt = jwt.encode(payload.__dict__, AUTHSECRET, algorithm='HS256')
            response = authResponse(encoded_jwt,int(EXPIRESSECONDS))
            
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
        decoded = jwt.decode(token, AUTHSECRET, algorithms=['HS256'])
        return decoded
    except (Exception) as error:
        print(error)
        return {"success": False}