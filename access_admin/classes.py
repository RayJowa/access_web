
class User:
    def __init__(self, user_id, first_name, surname, **kwargs):
        self.user_id = user_id
        self.first_name = first_name
        self.surname = surname
        self.phone = kwargs.get('phone', None)
