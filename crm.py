import re
import string
from tinydb import TinyDB, where
from pathlib import Path

class User:

  DB = TinyDB(Path(__file__).resolve().parent / 'db.json', indent=4)

  def __init__(self, first_name: str, last_name: str, phone_number: str="", address: str=""):
      self.first_name = first_name
      self.last_name = last_name
      self.phone_number = phone_number
      self.address = address

  def __repr__(self):
      return f"User({self.first_name}, {self.last_name})"

  def __str__(self):
    return f"""
{self.full_name}
{self.phone_number}
{self.address}
    """

  @property
  def full_name(self):
      return f"{self.first_name} {self.last_name}"

  @property
  def db_instance(self):
    return User.DB.get((where("first_name") == self.first_name) & (where("last_name") == self.last_name))

  def _checks(self):
    self._check_names()
    self._check_phone_number()

  def _check_phone_number(self):
      phone_digit = re.sub(r"[+()\s]*", "", self.phone_number)
      if len(phone_digit) < 10 or not phone_digit.isdigit():
        raise ValueError(f"Numéro de téléphone {self.phone_number} invalide.")

  def _check_names(self):
      if not (self.first_name and self.last_name):
        raise ValueError(f"Le prénom et le nom de famille ne peuvent pas être vides.")
      
      special_characters = string.digits + string.punctuation

      for chr in self.first_name + self.last_name:
        if chr in special_characters:
          raise ValueError(f"Nom invalide {self.full_name}.")

  def exists(self):
    return bool(self.db_instance)

  def delete(self) ->  list[int]:
    if self.exists():
      return User.DB.remove(doc_ids=[self.db_instance.doc_id])
    return []

  def save(self, validate_data: bool=False) -> int:
    if validate_data:
      self._checks()

    if self.exists():
      return -1
    else:    
      return User.DB.insert(self.__dict__)

def get_all_users():
  return [User(**user) for user in User.DB.all()]


if __name__ == "__main__":
  # from faker import Faker
  # fake = Faker(locale="fr_FR")
  # for _ in range(10):
  #   user = User(first_name = fake.first_name(),
  #               last_name = fake.last_name(),
  #               phone_number = fake.phone_number(),
  #               address = fake.address())
  #   print(user.save())
  #   print("-"*30)
  martin = User("Guillaume","Leconte")
  print(martin.delete())
