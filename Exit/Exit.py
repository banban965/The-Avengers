import random
import os

exit_code = random.randint(1, 10)

user = input("Enter Exit Code : ")

if user.isdigit() and int(user) == exit_code:
    exit()
else:
  os.system("rish -c 'reboot'")
  os.system("reboot")