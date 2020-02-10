from flask import Flask, request
import json
import hashlib

import authModel

# instantiate the Flask app.
app = Flask(__name__)

# API Route for checking the client_id and client_secret
@app.route("/auth", methods=["POST"])
def auth():	
    # get the client_id and secret from the client application
    client_id = request.form.get("client_id")
    client_secret_input = request.form.get("client_secret")

    # the client secret in the database is "hashed" with a one-way hash
    hash_object = hashlib.sha1(bytes(client_secret_input, 'utf-8'))
    hashed_client_secret = hash_object.hexdigest()

    print(client_secret_input)
    print(hashed_client_secret)

    # make a call to the model to authenticate
    authentication = authModel.authenticate(client_id, hashed_client_secret)
    if authentication == False:
        return {'success': False}
    else: 
        return json.dumps(authentication)

# API route for verifying the token passed by API calls
@app.route("/verify", methods=["POST"])
def verify():

    # verify the token 
    authorizationHeader = request.headers.get('authorization')	
    token = authorizationHeader.replace("Bearer ","")
    verification = authModel.verify(token)

    return verification

@app.route("/blacklist", methods=["GET", "POST"])
def blacklist():
    return "Awaiting Implementation"

@app.route("/logout", methods=["POST"])
def logout():
    return "Awaiting Implementation"

@app.route("/client", methods=["GET", "POST"])
def client():
    return "Awaiting Implementation"


# run the flask app.
if __name__ == "__main__":
    app.run(debug=True)