# USER CLASS VERIFICATION FUNCTIONS
def is_basic(user):
    if user.user_type != 1:
        return False
    return True

def is_sponsor(user):
    if user.user_type != 2:
        return False
    return True

def is_admin(user):
    if user.user_type != 3:
        return False
    return True