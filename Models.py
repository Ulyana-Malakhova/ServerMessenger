class Role:
    def __init__(self, id, name):
        self.id = id
        self.name = name


class UserRole:
    def __init__(self, user_id, role_id):
        self.user_id = user_id
        self.role_id = role_id


class User:
    def __init__(self, id, given_name, family_name, middle_name, nickname, isActive):
        self.id = id
        self.given_name = given_name
        self.family_name = family_name
        self.middle_name = middle_name
        self.nickname = nickname
        self.isActive = isActive


class University:
    def __init__(self, id, name):
        self.id = id
        self.name = name


class Group:
    def __init__(self, id, name, ts):
        self.id = id
        self.name = name
        self.ts = ts


class Message:
    def __init__(self, id, content, user_id, ts):
        self.id = id
        self.content = content
        self.user_id = user_id
        self.ts = ts


class GroupMessages:
    def __init__(self, group_id, message_id):
        self.group_id = group_id
        self.message_id = message_id


class GroupUsers:
    def __init__(self, group_id, user_id):
        self.group_id = group_id
        self.user_id = user_id


class UserToUserMessages:
    def __init__(self, user_recipient_id, message_id):
        self.user_recipient_id = user_recipient_id
        self.message_id = message_id


class UniversityGroups:
    def __init__(self, university_id, group_id):
        self.university_id = university_id
        self.group_id = group_id
