class UserNotAuthorized(Exception):
    pass

class UserNotFound(Exception):
    pass

class PasswordIncorrect(Exception):
    pass

class TokenNotFound(Exception):
    pass

class BlacklistToken(Exception):
    pass

class ProfilePrivate(Exception):
    def __init__(self, user_profile):
        self.user_profile = user_profile
