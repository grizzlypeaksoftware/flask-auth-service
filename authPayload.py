from datetime import datetime  
from datetime import timedelta  
import os

class authPayload(dict):

    def __init__(self, id, clientId):

        EXPIRESSECONDS = int(os.getenv('EXPIRESSECONDS'))

        # set the id of the object from Postgres
        self.id = id

        #  The client id (like the user id)
        self.clientId = clientId

        # set the expiry attrbute to 30 minutes
        self.exp = str(datetime.utcnow() + timedelta(seconds=EXPIRESSECONDS))