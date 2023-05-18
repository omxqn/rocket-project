import random
from sys import exit

# Define functions
def displayMenu():
    # Displays the menu and returns the user choice
    choices = {1: "Add order",
               2: "Display order",
               3: "Display all orders",
               4: "Display orders per customer",
               5: "Display orders per country",
               6: "Display orders statistics",
               7: "Remove order",
               8: "Exit program"}

    print('''
****************************************
	        Al-Yaqeen Logistics
****************************************''')
    for i in choices:
        print(f"{i}) ", choices[i])
    print("****************************************")
    choice = (input("Enter your choice: "))
    return choice


def addOrder(database, GCC_COUNTRIES, ZONE1_COUNTRIES, ZONE2_COUNTRIES, ZONE1_COST, ZONE2_COST, OMR_PER_KG):
    """
    Prompts the user for a new order and adds it to the order information lists."""
    while True:
        user_input = input("Enter order information (customer phone number, country, weight in kg): \n")
        user_input = user_input.split()
        if len(user_input) < 3:
            print("ERROR: Few data entered! Try again.")
            continue
        elif len(user_input) > 3:
            print("ERROR: More data entered! Try again.")
            continue
        phone_num = user_input[0]
        destination = user_input[1]
        destination = destination.upper()
        weight = user_input[2]
        # Generate unique order number
        while True:
            order_num = str(random.randint(100000, 999999))
            for i in database:
                if order_num in i:
                    continue
                else:
                    break
            break

        # Check phone length
        if phone_num.isdigit() and len(phone_num) == 8:
            pass
        else:
            print("ERROR: Invalid phone number. Try again!")
            continue

        # Get order weight
        if (weight.isdigit() or (weight.replace('.', '', 1).isdigit() and weight.count('.') == 1)) and int(weight) > 0:
            weight = float(weight)

        else:
            print("ERROR: Invalid weight! Try again. \n")
            continue

        # Compute order cost
        if destination in GCC_COUNTRIES:
            if destination in ZONE1_COUNTRIES:
                cost = weight * OMR_PER_KG + ZONE1_COST

            elif destination in ZONE2_COUNTRIES:
                cost = weight * OMR_PER_KG + ZONE2_COST

            else:
                cost = weight * OMR_PER_KG
        else:
            print(f"""ERROR: None GCC country:{destination}
Currently no shipping services outside GCC.
Try again.\n""")
            continue

        # Add order information to database dict
        database.append([order_num,phone_num, destination, weight, cost])

        # Print order information
        print("A new order has been added...")
        print("***************************************************************************")
        print("%-15s %-16s %-16s %-16s %-16s" % ("Customer Phone", "Order Number", "Country", "Weight", "Cost"))
        print("***************************************************************************")
        print(" %-15s %-16s %-16s %-16s %-16.3f" % (phone_num, order_num, destination, weight, cost))
        print("***************************************************************************\n")
        print(database)
        return database


def displayOrder(x, database):
    # displays details of a specific order, identified by its order number, if it exists in the database
    for i,index in enumerate(database):
        if x in i:

            print("***************************************************************************")
            print("%-15s %-16s %-16s %-16s %-16s" % ("Customer Phone", "Order Number", "Country", "Weight", "Cost"))
            print("***************************************************************************")
            print(" %-15s %-16s %-16s %-16s %-16.3f" % (database[][x][0], x, database[x][1], database[x][2], database[x][3]))
            print("***************************************************************************\n")
        else:
            print("\nERROR: Invalid order number! Try again.")


def displayAllOrders(database):
    # displays details of all orders in the database
    print("***************************************************************************")
    print("%-15s %-16s %-16s %-16s %-16s" % ("Customer Phone", "Order Number", "Country", "Weight", "Cost"))
    print("***************************************************************************")

    for i in database:
        print(" %-15s %-16s %-16s %-16s %-16.3f" % (database[i][0], i, database[i][1], database[i][2], database[i][3]))

    print("***************************************************************************\n")


def displayCustomerOrders(phone_num, database):
    # displays details of all orders associated with a specific customer, identified by their phone number
    empty = True
    data = []
    for i in database:
        if database[i][0] == phone_num:
            data.append(" %-15s %-16s %-16s %-16s %-16.3f" % (
                database[i][0], i, database[i][1], database[i][2], database[i][3]))
            empty=False

    if empty:
        print(f"No orders for customer with phone {phone_num}.")
    else:
        print("***************************************************************************")
        print("%-15s %-16s %-16s %-16s %-16s" % ("Customer Phone", "Order Number", "Country", "Weight", "Cost"))
        print("***************************************************************************")
        for i in data:
            print(i)
        print("***************************************************************************\n")


def displayCountryOrders(country,GCC, database):

    # displays details of all orders associated with a specific country
    empty = True
    data = []
    total = 0
    for i in database:
        if database[i][1] == country:
            data.append(" %-15s %-16s %-16s %-16s %-16.3f" % (
            database[i][0], i, database[i][1], database[i][2], database[i][3]))
            empty = False
            total += database[i][3]

    if empty:
        if country in GCC:
            print(f"No orders for customer with phone {country}.")
        else:
            print(f"""ERROR: None GCC country:{country}
            Currently no shipping services outside GCC.
            Try again.""")

    else:
        print("****************************************************************************************************")
        print("%-15s %-16s %-16s %-16s %-16s" % ("Customer Phone", "Order Number", "Country", "Weight", "Cost"))
        print("****************************************************************************************************")
        for i in data:
            print(i)
        print("****************************************************************************************************\n")
        print(f"Total cost of orders shipped to {country} is {total} OMR.")




def displayStatistics(database):
    # calculates and displays some statistics related to the orders in the database, such as the total and average cost of all orders, and the order with the highest and lowest cost

    total_cost = 0
    highest_cost = 0
    highest_order_num = None
    highest_customer_phone = None
    highest_country = None
    lowest_cost = float('inf')
    lowest_order_num = None
    lowest_customer_phone = None
    lowest_country = None

    for order_num, order_info in database.items():
        cost = order_info[3]
        total_cost += cost
        if cost > highest_cost:
            highest_cost = cost
            highest_order_num = order_num
            highest_customer_phone = order_info[0]
            highest_country = order_info[1]
        if cost < lowest_cost:
            lowest_cost = cost
            lowest_order_num = order_num
            lowest_customer_phone = order_info[0]
            lowest_country = order_info[1]

    num_orders = len(database)
    avg_cost = total_cost / num_orders
    print("****************************************************************************************************")
    print(f"Numbers orders: {num_orders}")
    print("----------------------------------------------------------------------------")
    print(f"Total orders cost: OMR{total_cost:.3f}")
    print("----------------------------------------------------------------------------")
    print(f"Average order cost: OMR{avg_cost:.3f}")
    print("----------------------------------------------------------------------------")
    print("Order with highest cost:")
    print(
        f"order number: {highest_order_num}, customer phone: {highest_customer_phone}, country: {highest_country}, cost: OMR{highest_cost:.3f}")
    print("----------------------------------------------------------------------------")
    print("Order with lowest cost:")
    print(
        f"order number: {lowest_order_num}, customer phone: {lowest_customer_phone}, country: {lowest_country}, cost: OMR{lowest_cost:.3f}")
    print("****************************************************************************************************")


def removeOrder(order_num, database):
    # ask user if he want to remove or not
    user_confirmation = input(f"Are you sure that you want to remove order #{order_num} from the list? (yes or no): ")
    user_confirmation = user_confirmation.lower()
    if user_confirmation == "yes" and order_num in database:
        del database[order_num]
        print(f"Order number {order_num} has been removed.")
        return database
    else:
        print("You said no or the order doesn't exist")


def main():
    # Define constants
    GCC_COUNTRIES = ['OMAN', 'UAE', 'KSA', 'QATAR', 'BAHRAIN', 'KUWAIT']
    ZONE1_COUNTRIES = ["UAE", "QATAR"]
    ZONE2_COUNTRIES = ["BAHRAIN", "KUWAIT", "KSA"]
    OMR_PER_KG = 0.95
    ZONE1_COST = 5
    ZONE2_COST = 7

    # Define global order information lists
    database = []

    while True:
        choice = displayMenu()

        if choice == "1":
            database = addOrder(database, GCC_COUNTRIES, ZONE1_COUNTRIES, ZONE2_COUNTRIES, ZONE1_COST, ZONE2_COST,
                                OMR_PER_KG)

        elif choice == "2":

            if database != {}:
                display_input = input("\nEnter order number: ")
                displayOrder(display_input, database)
            else:
                print("No orders yet recorded. Select 1) Add order first!")
        elif choice == "3":

            displayAllOrders(database)

        elif choice == "4":
            cust_phone = input("\nEnter customer phone: ")
            if cust_phone.isdigit() and len(cust_phone) == 8:
                pass
            else:
                print("ERROR: Invalid phone number. Try again!")
                continue

            displayCustomerOrders(cust_phone, database)

        elif choice == "5":
            dest_country = input("\nEnter country name: ")
            dest_country=dest_country.upper()
            displayCountryOrders(dest_country, GCC_COUNTRIES,database)

        elif choice == "6":
            displayStatistics(database)

        elif choice == "7":
            if database != {}:
                order_num = input("\nEnter order number: ")
                database = removeOrder(order_num, database)
            else:
                print("No orders yet recorded. Select 1) Add order first!")


        elif choice == "8":
            user_confirmation = input("Are you sure you want to exit the application y/n: ")
            user_confirmation = user_confirmation.lower()
            if user_confirmation == "y":
                print("Goodbye!")
                exit()
            else:
                print("You said no.")

        else:
            print("ERROR: Invalid choice! Try again.")


main()