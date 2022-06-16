import os
import uuid
import pandas as pd
from past.builtins import raw_input


class AdminAccess:
    """Class for Admin to
    Add, Remove, View
    products in inventory"""

    # Constructor
    def __init__(self):
        pass

    # Adding products to inventory
    def add_to_inventory(self):
        self.product_id = uuid.uuid4()
        print('What do you want to add today?')

        # Taking inputs from the admin
        product = input("Enter product : ")
        size = input("Enter size : ")
        price = input("Enter price  :")
        quantity = input("How many of these you want to add? :")

        # Creating dataframe to add new row to the dataset and import it to csv file
        new_row = {'ProductID': str(self.product_id), 'Product': [product], 'Size': [size], 'Price': [price],
                   'Quantity': [quantity]}
        df = pd.DataFrame(new_row)

        # Checking if the file already exists to prevent header from repeating
        file_exists = os.path.exists('products.csv')
        while file_exists:
            # Importing the dataframe to a csv file with no header
            df.to_csv('products.csv', mode='a', index=False, header=False)
            break
        else:
            # Importing the dataframe to a csv file with header
            df.to_csv('products.csv', mode='a', index=False, header=True)
        print("Product information added successfully")

        # Need to check if this is working --- TBD
        # if product in df['Product']:
        #     if df.loc[df['Product' == product, 'Size']] == size:
        #         pd.merge(df, df, on=['Product'])
        # else:
        #     df.to_csv('products.csv', mode='a', index=False, header=False)
        #     print("Product information added successfully!")

        # If condition - whether admin wants to or doesn't want to add more products to inventory
        more_items = input("Do you have more items to add? Y or N: ")
        while True:
            if more_items == 'Y':
                AdminAccess.add_to_inventory(self)
                break
            elif more_items == 'N':
                AdminAccess.view_inventory(self)
                break
            else:
                print('Incorrect response, let us try again')
                break

    # View products information in inventory
    def view_inventory(self):
        pd.set_option('display.max_columns', None)
        print(pd.read_csv('products.csv'))

    # Remove products from inventory
    def remove_from_inventory(self):
        df = pd.read_csv('products.csv')
        delete_id = input("Please enter product id of an item you wish to delete: ")
        # if condition - to check user input exists in csv file
        if delete_id in df['ProductID'].values:
            confirmation = input("""Are you sure? Product will be deleted permanently!! 
            Type Y to delete Type 
            Type N to go back to inventory: """)
            if confirmation == 'Y':
                new_df = df[df.ProductID != delete_id]
                new_df.to_csv("products.csv", index=False)
            elif confirmation == 'N':
                print("All these products are available in inventory")
                AdminAccess.remove_from_inventory(self)
            else:
                print("Invalid input 1")
                AdminAccess.remove_from_inventory(self)
                exit()
        else:
            print("Invalid product id")
            continue_delete = input("""Do you want to try again: 
            Type Y or N: """)
            if continue_delete == 'Y':
                AdminAccess.view_inventory(self)
                AdminAccess.remove_from_inventory(self)
            elif continue_delete == 'N':
                print('Have a nice day!')
            else:
                print("Invalid entry")

        # If condition - whether admin wants to or doesn't want to remove more products from inventory
        more_items = input("Do you have more items to update? Y or N: ")
        while True:
            if more_items == 'Y':
                AdminAccess.remove_from_inventory(self)
                break
            elif more_items == 'N':
                AdminAccess.view_inventory(self)
                break
            else:
                print('Expecting Y or N')
                break


    def update_inventory(self):
        df = pd.read_csv('products.csv')
        product_name = input("Which product information you want to update? ")
        if product_name in df['Product'].values:
            while True:
                update_item = input("Choose Size or Price or Quantity : ")
                if update_item == 'Size':
                    size_update = input("Enter the new size : ")
                    df.loc[df.Product == product_name, 'Size'] = size_update
                    df.to_csv("products.csv", index=False)
                    break
                elif update_item == 'Price':
                    price_update = input("Enter the new price : ")
                    df.loc[df.Product == product_name, 'Price'] = price_update
                    df.to_csv("products.csv", index=False)
                    break
                elif update_item == 'Quantity':
                    quantity_update = input("Enter the new quantity : ")
                    df.loc[df.Product == product_name, 'Quantity'] = quantity_update
                    df.to_csv("products.csv", index=False)
                    break
                else:
                    print("Invalid input, Try again")
        else:
            print("{} is not in inventory, try again".format(product_name))
            AdminAccess.update_inventory(self)

        # If condition - whether admin wants to or doesn't want to update more products to inventory
        more_items = input("Do you have more items to update? Y or N: ")
        while True:
            if more_items == 'Y':
                AdminAccess.update_inventory(self)
                break
            elif more_items == 'N':
                AdminAccess.view_inventory(self)
                break
            else:
                print('Expecting Y or N')
                break


class ShoppingCart:
    """Class to add, remove, update
    items and view the shopping cart"""
    order_id = uuid.uuid4()

    # Constructor
    def __init__(self):
        super().__init__()

        self.items = {}  # Shopping basket dictionary : {item:quantity}

    # Display products at home page
    def product_catalog(self):
        df = pd.read_csv('products.csv')

        df.index = ([''] * len(df))  # making index empty for better visual
        print(df[['Product', 'Price']])

    # Add items to the shopping cart
    def add_item_to_cart(self):
        df = pd.read_csv('products.csv')
        while True:
            self.product_choice = input("Please select item from catalog: ")
            if self.product_choice in df['Product'].values:
                quantity = int(input("How many? : "))
                # Comparing the given quantity of the selected product with the quantity available in the inventory
                if 0 < quantity <= df.loc[df.Product == self.product_choice, 'Quantity'].item():
                    # Updating the inventory
                    df.loc[df.Product == self.product_choice, 'Quantity'] -= quantity
                    df.to_csv("products.csv", index=False)
                    # Checking if the item is already in the shopping basket
                    if self.product_choice in self.items:
                        self.items[self.product_choice] += quantity
                        # break
                    else:
                        self.items[self.product_choice] = quantity
                else:
                    print("Sorry only {} left".format(df.loc[df['Product'] == self.product_choice, 'Quantity'].iloc[0]))
            else:
                print("Select only listed products")
                ShoppingCart.add_item_to_cart(self)
                break
            # Adding more items to the cart
            print("Are you done Shopping? : ", end="")
            if ShoppingCart.yes_or_no(self):
                break

    # Method to decide what to do next on user's input
    def yes_or_no(self):
        while True:
            next_item = input()
            if next_item == "Y":
                return True
            if next_item == "N":
                return False
            print("Expecting Y or N")

    # Remove item from the shopping cart or reduce item quantity
    def remove_item_from_cart(self):
        df = pd.read_csv('products.csv')
        while True:
            to_remove = input("Please enter the item you want to remove from the cart : ")
            if to_remove in self.items:
                quantity = int(input("How many of {} you want to remove? : ".format(to_remove)))
                if quantity <= 0:
                    # Remove the item
                    self.items.pop(to_remove, None)
                else:
                    if quantity < self.items[to_remove]:
                        # Reduce the required quantity for this item
                        self.items[to_remove] -= quantity
                        # Sending rejected items back into inventory
                        df.loc[df.Product == self.product_choice, 'Quantity'] += quantity
                        df.to_csv("products.csv", index=False)
                    else:
                        # Remove the item
                        self.items.pop(to_remove, None)
                    ShoppingCart.view_cart(self)
            else:
                print("Product not in the cart")
                ShoppingCart.remove_item_from_cart(self)
            # Removing more items from the cart
            print("Are you done Shopping? : ", end="")
            if ShoppingCart.yes_or_no(self):
                break

    # View the content of the shopping cart
    def view_cart(self):
        df = pd.read_csv('products.csv')
        self.total_cost = 0
        temp_price = df.loc[df['Product'] == self.product_choice, 'Price'].item()
        price = float(temp_price)
        print("---------------------")
        for item in self.items:
            self.quantity = self.items[item] #made it self.quantity TBD
            # Calculating final price of the product in the cart if quantity more than 1
            cost = self.quantity * price
            print(item + "               " + str(self.quantity) + " - " + "{} ".format(
                price) + " - " + "${}".format(cost))
            # print(tabulate([item, str(quantity), "$" + str(price), "$" + str(cost)],
            #                headers=['Product', 'Qty', "", ""]))
            self.total_cost += cost
        print("=====================")
        print("Total Price                      ${}".format(self.total_cost))
        print("---------------------")

    # Checking out to payment if shopping is completed
    def checkout(self):
        df = pd.read_csv('products.csv')
        user_choice = input("Ready to checkout? Y or N : ")
        while True:
            if user_choice == "Y":
                ShoppingCart.payment(self)
                break
            elif user_choice == "N":
                ShoppingCart.view_cart(self)
                # Emptying cart as user doesn't want to check out
                ShoppingCart.empty_cart(self)
                # Putting back items into the inventory _ I added now TBD
                df.loc[df.Product == self.product_choice, 'Quantity'] += self.quantity  # added self.quantity TBD
                df.to_csv("products.csv", index=False)
                print("Emptied your cart!")
                break
            else:
                print("Expecting Y or N")
                ShoppingCart.checkout(self)

    # Giving user payment options
    def payment(self):
        self.payment_selection = input("Please select Cash or Card : ")
        # while payment type is card
        if self.payment_selection == 'Card':
            card_number = int(input("Please enter card number : "))
            exp_date = input("Please enter month and year of expiry as mm/yy : ")
            cvv = input("Please enter cvv at the back of the card : ")
            # creating a dataframe to add new row to the dataset and save DF to csv file
            self.new_row = {'OrderID': [str(__class__.order_id)], 'TotalAmount': [self.total_cost],
                            'Payment': [self.payment_selection], 'Card': [card_number], 'Expiry': [exp_date],
                            'CVV': [cvv]}
        # while payment type is cash
        elif self.payment_selection == 'Cash':
            self.cash_paid = float(input("Please enter total amount to be paid: "))
            if self.cash_paid == self.total_cost:
                print("Order accepted!")
                # self.cash_paid -= self.total_cost
            elif self.cash_paid < self.total_cost:
                self.cash_paid = raw_input("Cash paid not enough. Try again")
            # creating a dataframe to add new row to the dataset and save DF to csv file
            # need to check how to add userid - TBD
            self.new_row = {'OrderID': str(__class__.order_id), 'TotalAmount': [self.cash_paid],
                            'Payment': [self.payment_selection], 'Card': ['NA'], 'Expiry': ['NA'], 'CVV': ['NA']}

            print("Order accepted!")
        else:
            print("Invalid selection! Try again")
            ShoppingCart.payment(self)

        # Importing dataframe to csv
        orderdf = pd.DataFrame(self.new_row)
        file_exist = os.path.exists('orders.CSV')
        if file_exist:
            orderdf.to_csv('orders.csv', mode='a', index=False, header=False)
        else:
            orderdf.to_csv('orders.csv', mode='a', index=False, header=True)

    # Empty the shopping cart
    def empty_cart(self):
        self.items = {}


# Products display at home page
def product_catalog():
    df = pd.read_csv('products.csv')
    # Making index empty
    df.index = ([''] * len(df))
    print(df[['Product', 'Price']])
