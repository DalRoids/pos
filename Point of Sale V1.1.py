import time
import json

tax_rate = 1.12
last_charge_untaxed = 0
users = {}
master_login = {1001: 1234}

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

    menuOther("""Welcome to Point of Sale V1.1!
Please enter your login credentials to continue""")

    check = False

    while check is False:

        try:
            un = int(input("""Username
-> """))
            pw = int(input("""Password
-> """))
        except:
            menuOther("Incorrect entry, please try again")
            continue

        for x, y in master_login.items():
            if x == un:
                un_check = True
                if y == pw:
                    pw_check = True
                    check = True

        for x, y in users.items():
            if x == un:
                un_check = True
                if y == pw:
                    pw_check = True
                    check = True
            else:
                break

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
            inventoryMenu()
        elif x == "3":
            createUser()
        elif x == "4":
            time.sleep(0.2)
            print("System shutting down...")
            time.sleep(3)


########################
# Sales Menu Functions #
########################


def saleEntry():

    global last_charge
    global last_charge_untaxed
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
        mainMenu


#######################
# Inventory Functions #
#######################


def inventoryMenu():

    menuCreate("Inventory", "Back")

    menuOther("""1. Stock Lookup
2. SKU creation
3. View Stock File""")

    user_input = input("What would you like to do: ")

    if user_input == "1":
        stockLookup()

    if user_input == "2":
        skuCreate()

    if user_input == "3":
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
        print("Press D to return to Inventory Menu")
        user_input = input("-> ")

        if user_input.lower() == "d":
            break

    inventoryMenu()


##################
# User Functions #
##################

mainMenu()
