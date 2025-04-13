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

class UserFriendsException(Exception):
    pass

class UserBadgesException(Exception):
    pass

class UserGetOwnedGames(Exception):
    pass
