import random

class FamilyStructure:
    def __init__(self, last_name):
        self.last_name = last_name
        self._members = []

    def _generateId(self):
        return random.randint(0, 99999999)

    def add_member(self, member):
        member.id = self._generateId()
        member.last_name = self.last_name
        self._members.append(member)

    def delete_member(self, id):
        self._members = [member for member in self._members if member.id != id]

    def get_member(self, id):
        for member in self._members:
            if member.id == id:
                return member
        return None

    def get_all_members(self):
        return self._members

class FamilyMember:
    def __init__(self, first_name, age, lucky_numbers):
        self.id = None
        self.first_name = first_name
        self.age = age
        self.lucky_numbers = lucky_numbers
        self.last_name = None

    def __str__(self):
        return f"{self.first_name} {self.last_name}, Age: {self.age}, Lucky Numbers: {self.lucky_numbers}"