from users import *
from products import *

print("\n-----Hi! Welcome to My Groceries-----\n")

# Displaying products catalog
print("====================Products====================\n")
product_catalog()
print("\n================================================")

# Checking type of the login: Existing user login, Guest user login or Admin login
# Then displaying pages with respect to the type of login - Inventory page for admin, Shopping page for customer
statusobj = LoginAction()
statusobj.status_check()





