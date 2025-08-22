from dataclasses import dataclass

@dataclass
class FakeUserDto:
    def __init__(self, firstname: str, lastname: str):
        self.firstname = firstname
        self.lastname = lastname