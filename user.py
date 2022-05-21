""" Module to generate random users"""
from faker import Faker
import logging
from pathlib import Path

BASE_DIR = Path(r"G:\Prog\Projet perso\UserGenerator\user.py").resolve().parent
logging.basicConfig(level=logging.INFO,
                    filename=BASE_DIR / "user.log", 
                    filemode="a",
                    format='%(asctime)s - %(levelname)s - %(message)s')


fake = Faker(locale="fr_FR")


def get_user():
  """Generate a user

  Returns:
      str: user
  """
  logging.info("Generating user.")
  return f"{fake.first_name()} {fake.last_name()}"

def get_users(n:int):
  """Generate a list of users

  Args:
      n (int): Number of users

  Returns:
      list[str]: users
  """
  logging.info(f"Generating a list of {n} user.")

  return [get_user() for _ in range(n)]

# ******************************
#     test in module
# ******************************
if __name__ == "__main__":
  user = get_user()
  print(user)


  name_list = get_users(5)
  print(name_list)