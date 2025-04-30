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

class UserNotPermitions(Exception):
    pass

class UserRegisterError(Exception):
    pass

class PageNotFound(Exception):
    def __init__(self,page):
        self.page = page

class ProfilePrivate(Exception):
    def __init__(self, user_profile):
        self.user_profile = user_profile
