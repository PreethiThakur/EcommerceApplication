# # shopping_list = []
# #
# # # Add a function to allow users to ask for help when they need to
# # def show_help():
# #     print("""
# #   Enter 'DONE' to stop adding items.
# #   Enter 'SHOW' to see your shopping list
# #   """)
# #
# # # Create a function that adds an item to the list
# # def add_to_list(item):
# #     shopping_list.append(item)
# #     print('{} was added to your shopping list!'.format(item))
# #     print('You have {} items on your list.'.format(len(shopping_list)))
# #
# #
# # # Create a function to print all the items in the shopping list
# # def show_list():
# #     print('My Shopping List:')
# #     for item in shopping_list:
# #         print(item)
# #
# #
# # show_help()
# #
# # while True:
# #     new_item = input('> ')
# #
# #     # If the user inputs 'DONE' exit the loop
# #     if new_item == 'DONE':
# #         break
# #     # if the user inputs 'SHOW' show the list
# #     elif new_item == 'SHOW':
# #         show_list()
# #         continue
# #
# #     # Call add_to_list with new item as an argument
# #     add_to_list(new_item)
# #
# # show_list()
#
#
#
#
# # ==============================================================================================
# #
# # class ShoppingCart(object):
# #
# #     def __init__(self):
# #         self.total = 0
# #         self.items = {}
# #
# #     def add_item(self, item_name, quantity, price):
# #         self.items[item_name] = quantity
# #         self.total += (price * quantity)
# #
# #     def remove_item(self, item_name, quantity, price):
# #         if quantity < self.items[item_name] and quantity >= 0:
# #             self.total -= price * quantity
# #             self.items[item_name] -= quantity
# #         elif quantity >= self.items[item_name]:
# #             del self.items[item_name]
# #         else:
# #             self.total -= price * self.items[item_name]
# #             del self.items[item_name]
# #
# #     def checkout(self, cash_paid):
# #         if cash_paid >= self.total:
# #             return cash_paid - self.total
# #         else:
# #             return "Cash paid not enough"
# #
# #
# # class Shop(ShoppingCart):
# #     def __init__(self):
# #         self.quantity = 100
# #
# #     def remove_item(self):
# #         self.quantity -= 1
# #
# # shopobj = ShoppingCart()
# # shopobj.add_item('apple', 10, 5)
# # shopobj.checkout()
#
# from products import *
# # ==================================================================================================
#
# class ShoppingCart:
#     # Constructor
#     def __init__(self):
#         # self.product = product
#         # self.quantity = quantity
#         self.items = {}  # A dictionary of all the items in the shopping basket: {item:quantity}
#         self.checkout = False
#
#     # def product_catalog(self):
#     #     df = pd.read_csv('products.csv')
#     #     print(df['Product'].unique())
#     #     # print(df['Product'].tolist())
#     #     # choose_product = input('What do you want to purchase today? ')
#
#     # Add an item to the shopping basket
#     def addItem(self):
#         df = pd.read_csv('products.csv')
#         # ShoppingCart.product_catalog(self)
#         product_choice = input("Please select an item from catalogue: ")
#         if product_choice in df['Product'].values:
#             quantity = int(input("How many? : "))
#             if quantity > 0:
#                 # Check if the item is already in the shopping basket
#                 if product_choice in self.items:
#                     self.items[product_choice] += quantity
#                 else:
#                     self.items[product_choice] = quantity
#             else:
#                 print("Invalid operation - Quantity must be a positive number!")
#
#         else:
#             print("Select only listed products")
#             ShoppingCart.product_catalog(self)
#             ShoppingCart.addItem(self)
#
#     # Remove an item from the shopping basket (or reduce it's quantity)
#     def removeItem(self, item, quantity=0):
#         if quantity <= 0:
#             # Remove the item
#             self.items.pop(item, None)
#         else:
#             if item in self.items:
#                 if quantity < self.items[item]:
#                     # Reduce the required quantity for this item
#                     self.items[item] -= quantity
#                 else:
#                     # Remove the item
#                     self.items.pop(item, None)
#
#         # A method to update the quantity of an item from the shopping basket
#
#     def updateItem(self, item, quantity):
#         if quantity > 0:
#             self.items[item] = quantity
#         else:
#             self.removeItem(item)
#
#     # A method to view/list the content of the basket.
#     def view(self):
#         totalCost = 0
#         print("---------------------")
#         for item in self.items:
#             quantity = self.items[item]
#             cost = quantity * item.price
#             print(" + " + item.name + " - " + str(quantity) + " x £" + '{0:.2f}'.format(
#                 item.price) + " = £" + '{0:.2f}'.format(cost))
#             totalCost += cost
#         print("---------------------")
#         print(" = £" + '{0:.2f}'.format(totalCost))
#         print("---------------------")
#
#     # A method to calculate the total cost of the basket.
#     def getTotalCost(self):
#         totalCost = 0
#         for item in self.items:
#             quantity = self.items[item]
#             cost = quantity * item.price
#             totalCost += cost
#         return totalCost
#
#     # A method to empty the content of the basket
#     def reset(self):
#         self.items = {}
#
#     # A method to return whether the basket is empty or not:
#     def isEmpty(self):
#         return len(self.items) == 0
#
# shopobj = ShoppingCart()
# shopobj.addItem()
# shopobj.view()



def ask_yes_no():
    while True:
        x = input()
        if x == "yes":
            return True
        if x == "no":
            return False
        print("Expecting yes/no")

grocery_items = []

while True:
    grocery_item = input("Add to Grocery ")
    print("Are you done? ", end="")

    if ask_yes_no():
        break

    grocery_items.append(grocery_item)