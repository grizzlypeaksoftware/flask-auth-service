class authResponse(dict):
    
    def __init__(self, token, expiresin, isAdmin):
        self.token = token.decode('utf-8')
        self.expiresin = expiresin