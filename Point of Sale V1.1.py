import time
import json

tax_rate = 1.12
last_charge_untaxed = 0


def main():

    login_check = False

    while login_check == False:
        login_check = login()

    if login_check == True:
        mainMenu()

############################
# User Interface Functions #
############################


def menuCreate(menuName: str, menuFunction: str):  # creates menu surrounded by dashes
    # set x to menu name
    # set y to variable function within menu

    z = f"| {menuName} | D - {menuFunction} | E - Main Menu |"

    counter = 0
    for _ in z:
        counter += 1
    dash = "-"

    print(f"""{dash * counter}
{z}
{dash * counter}""")


def menuOther(menuText):

    counter = 0
    highest_count = 0
    dash = "-"

    for _ in menuText:
        counter += 1
        if _ == "\n":
            if highest_count < counter:
                highest_count = counter
            counter = 0
        if counter > highest_count:
            highest_count = counter

    print(f"""{dash * highest_count}
{menuText}
{dash * highest_count}""")


def pointer():
    print("-> ")


###################
# Login Functions #
###################


def login():

    un_check = False
    pw_check = False

    menuOther("""Welcome to Point of Sale V1.1!
Please enter your login credentials to continue""")

    check = False

    while check is False:

        with open("Users.txt", "r") as file:
            data = json.load(file)

        try:
            un = input("""Username
-> """)
            if un not in data:
                print("Incorrect username")
                continue

            pw = int(input("""Password
-> """))

        except:
            menuOther("Incorrect entry, please try again")
            continue

        for x, y in data.items():

            if x == un:
                un_check = True
            if y == pw:
                pw_check = True

        if un_check is True and pw_check is True:
            check = True
        else:
            print("Incorrect Password")
            continue

    time.sleep(1)
    print("")
    print("You are being logged in...")
    time.sleep(1)

    return True


#######################
# Main Menu Functions #
#######################


def mainMenu():

    while True:

        x = input("""
Main Menu
--------------
1. Sale Entry
2. Inventory
3. Users
4. Exit System
--------------
-> """)

        if x == "1":
            saleEntry()
        elif x == "2":
            time.sleep(0.2)
            print("Loading Inventory Functions...")
            time.sleep(0.3)
            inventoryMenu()
        elif x == "3":
            userMenu()
        elif x == "4":
            time.sleep(0.2)
            print("System shutting down...")
            time.sleep(3)
            exit("System succesfully shut down")


########################
# Sales Menu Functions #
########################


def saleEntry():

    global last_charge
    global last_charge_untaxed
    receipt_details = ""
    p_name = 0
    p_price = 1
    total = 0
    if last_charge_untaxed > 0:
        total = last_charge_untaxed
    time.sleep(0.2)
    print("Loading Sale Entry...")
    time.sleep(0.3)

    menuCreate("SKU Entry", "Payment")

    while True:

        with open("Inventory.txt", "r") as file:
            sku_data = json.load(file)

        sku = input("Enter SKU: ")
        if sku.lower() == "e":
            time.sleep(0.2)
            print("Sales entry cancelled, returning to Main Menu...")
            time.sleep(0.5)
            mainMenu()
        if sku.lower() == "d":
            time.sleep(0.2)
            if total < 0.01:
                print(
                    ">>> No items entered, please enter items or enter E to return to main menu")
                continue
            else:
                break

        if sku in sku_data:

            sku_list = sku_data[sku]
            product = sku_list[p_price]
            product_name = sku_list[p_name]

        elif sku not in sku_data:
            print(f'"{sku}" not found in Inventory, please retry')
            continue

        product = float(product)
        print(f">>> {product_name}")
        quantity = int(input("Quantity: "))
        # sums product and quantity to 2 decimal points
        total = float("{:.2f}".format(total + (product * quantity)))
        time.sleep(0.3)

        receipt_entry = f"""{sku} | {product_name} | {product} | {quantity}"""
        if receipt_details == "":
            receipt_details = receipt_details + receipt_entry
        else:
            receipt_details = receipt_details + "\n" + receipt_entry

    for each in receipt_details.split("\n"):
        time.sleep(0.1)
        print(each)

    last_charge_untaxed = total
    last_charge = total * tax_rate
    format_charge = "{:.2f}".format(last_charge)
    last_charge = float(format_charge)
    time.sleep(0.3)
    print("")
    print(f""">>> Customer total: {last_charge}""")
    time.sleep(1)
    payment()


def payment():

    global last_charge
    global last_charge_untaxed
    payment_success = None
    while payment_success is None:

        menuOther("""Please select payment method:
1. Cash 2. Debit 3. Credit 4. Price Entry 5. Abort""")
        payment_method = input("-> ")

        if payment_method == "1":
            amount = float(input(">>> Enter amount given: "))
            change = "{:.2f}".format(amount - last_charge)
            print(f">>> Customer change: {change}")
            payment_success = True
            break

        elif payment_method == "2" or payment_method == "3":
            print(f">>> Total: {last_charge}")
            time.sleep(0.3)
            print(">>> Please insert card")
            time.sleep(2)
            while True:
                check = input(""">>> Did payment go through? Y/N
-> """)
                if check.lower() == "y":
                    payment_success = True
                    break
                elif check.lower() == "n":
                    recheck = input("Try again? Y/N")
                    if recheck == "y":
                        continue
                    elif recheck == "n":
                        payment_success = False

        elif payment_method == "4":
            saleEntry()

        elif payment_method == "5":
            confirm = input("""Are you sure you want to abort payment? Y/N
-> """)

            if confirm.lower() == "y":
                last_charge_untaxed = 0
                print("Returning to main menu...")
                time.sleep(1)
                mainMenu()
            elif confirm.lower() == "n":
                continue

    if payment_success == True:
        last_charge_untaxed = 0
        last_charge = 0
        time.sleep(1)
        print("Sale complete, returning to main menu...")
        time.sleep(0.5)
        mainMenu()
    elif payment_success == False:
        last_charge_untaxed = 0
        last_charge = 0
        time.sleep(1)
        print("Sale did not go through, customer not charged, returning to main menu...")
        time.sleep(0.5)
        mainMenu()


#######################
# Inventory Functions #
#######################


def inventoryMenu():

    menuCreate("Inventory", "Back")

    menuOther("""1. Stock Lookup
2. SKU creation
3. View Stock File""")

    user_input = input("-> ")

    if user_input.lower() == "d" or user_input.lower() == "e":
        time.sleep(0.5)
        mainMenu()

    if user_input == "1":
        time.sleep(0.2)
        stockLookup()

    if user_input == "2":
        time.sleep(0.2)
        skuCreate()

    if user_input == "3":
        time.sleep(0.2)
        viewAll()


def skuCreate():

    menuCreate("SKU Creation", "Back")

    while True:

        product_sku = input("Enter product SKU number: ")
        product_name = input("Product name: ")
        product_price = input("Product price: ")

        if product_sku.lower() == "d":
            break
        if product_name.lower() == "d":
            break
        if product_sku.lower() == "d":
            break

        sku_object = [product_name, product_price]

        sku_entry = {product_sku: sku_object}

        with open("Inventory.txt", "r") as file:
            data = json.load(file)

        data.update(sku_entry)

        with open("Inventory.txt", "w") as file:
            data = json.dump(data, file)

        choice = input("""Add another SKU to inventory?
-> """)

        if choice.lower() == "y":
            continue

        else:
            break

    inventoryMenu()


def stockLookup():

    p_name = 0
    p_price = 1

    menuCreate("SKU Lookup", "Back")

    while True:

        menuOther("Enter SKU")
        sku = input("-> ")

        if sku.lower() == "d":
            time.sleep(0.5)
            inventoryMenu()

        with open("Inventory.txt", "r") as file:
            data = json.load(file)

        time.sleep(0.5)

        if sku in data:
            product_list = data[sku]

            print(f">>> {product_list[p_name]}", "|", product_list[p_price])

        time.sleep(0.5)


def viewAll():

    while True:

        with open("Inventory.txt", "r") as file:
            stock_list = json.load(file)

        for each in stock_list:
            time.sleep(0.1)
            s_list = stock_list[each]
            print(each, "|", s_list[0], "|", s_list[1])

        time.sleep(1)
        print("""Press D to return to Inventory Menu""")
        user_input = input("-> ")

        if user_input.lower() == "d":
            break

    time.sleep(0.5)
    inventoryMenu()


##################
# User Functions #
##################


def userMenu():

    menuCreate("User Functions", "Back")

    print("""1. Add User
2. Delete User
3. View Users""")

    user_choice = input("-> ")

    if user_choice.lower() == "d" or user_choice.lower() == "e":
        time.sleep(0.5)
        print(">>> Loading main menu")
        time.sleep(0.5)
        mainMenu()
    if user_choice == "1":
        time.sleep(0.5)
        userAdd()
    if user_choice == "2":
        time.sleep(0.5)
        userDelete()
    if user_choice == "3":
        time.sleep(0.5)
        viewUsers()


def userAdd():

    while True:

        try:
            username = int(input("Please enter a 4 digit numerical user ID: "))
            password = int(
                input("Please enter a 6 digit numerical password: "))
        except:
            continue

        user = {username: password}

        with open("Users.txt", "r") as file:
            data = json.load(file)

        data.update(user)

        with open("Users.txt", "w") as file:
            data = json.dump(data, file)

        time.sleep(0.5)
        print("Adding User...")
        time.sleep(0.5)
        print("User added, returning to User Menu")
        break

    userMenu()


def userDelete():

    while True:

        try:
            username = input("Enter user to delete: ")
        except:
            continue

        with open("Users.txt", "r") as file:
            data = json.load(file)

        if username in data:
            data.pop(username)
        else:
            print("User not found, returning to main menu...")

        with open("Users.txt", "w") as file:
            data = json.dump(data, file)

        break

    print("User succesfully deleted, returning to main menu")


def viewUsers():

    with open("Users.txt", "r") as file:
        data = json.load(file)

    for each, value in data.items():
        print(each, value)


main()
