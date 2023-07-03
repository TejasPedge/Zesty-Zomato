import json
from tabulate import tabulate
from colorama import Fore, Style

# Define the menu as a list of dictionaries
menu = []

# Define the list of orders
orders = []

# Define the available statuses
statuses = ['received', 'preparing', 'ready for pickup', 'delivered']


def load_data():
    """Load menu and order data from JSON files"""
    global menu, orders
    try:
        with open('menu.json', 'r') as file:
            menu = json.load(file)
    except FileNotFoundError:
        menu = []

    try:
        with open('orders.json', 'r') as file:
            orders = json.load(file)
    except FileNotFoundError:
        orders = []


def save_data():
    """Save menu and order data to JSON files"""
    with open('menu.json', 'w') as file:
        json.dump(menu, file, indent=4)

    with open('orders.json', 'w') as file:
        json.dump(orders, file, indent=4)


def print_menu():
    """Display the menu"""
    print("\nMenu:")
    table = []
    for item in menu:
        table.append([item['id'], item['name'], item['price'], item['availability']])
    print(tabulate(table, headers=['ID', 'Dish', 'Price', 'Availability'], tablefmt="fancy_grid"))


def add_dish():
    """Add a new dish to the menu"""
    print("\nAdd a New Dish to the Menu")
    name = input("Enter the name of the dish: ")
    price = float(input("Enter the price of the dish: "))
    availability = input("Is the dish available? (yes/no): ").lower()

    dish = {
        'id': len(menu) + 1,
        'name': name,
        'price': price,
        'availability': availability
    }

    menu.append(dish)
    save_data()
    print(f"\n{Fore.GREEN}Dish added successfully!{Style.RESET_ALL}")


def remove_dish():
    """Remove a dish from the menu"""
    print("\nRemove a Dish from the Menu")
    dish_id = int(input("Enter the ID of the dish to remove: "))

    for dish in menu:
        if dish['id'] == dish_id:
            menu.remove(dish)
            save_data()
            print(f"\n{Fore.GREEN}Dish removed successfully!{Style.RESET_ALL}")
            return

    print(f"\n{Fore.RED}Error: Dish ID not found!{Style.RESET_ALL}")


def update_dish_availability():
    """Update the availability of a dish"""
    print("\nUpdate Dish Availability")
    dish_id = int(input("Enter the ID of the dish to update: "))

    for dish in menu:
        if dish['id'] == dish_id:
            availability = input("Is the dish available? (yes/no): ").lower()
            dish['availability'] = availability
            save_data()
            print(f"\n{Fore.GREEN}Dish availability updated successfully!{Style.RESET_ALL}")
            return

    print(f"\n{Fore.RED}Error: Dish ID not found!{Style.RESET_ALL}")


def take_order():
    """Take a new order"""
    print("\nTake a New Order")
    customer_name = input("Enter the customer name: ")
    order_dishes = input("Enter the dish IDs (comma-separated): ").split(',')

    # Check dish availability and calculate total price
    total_price = 0.0
    order_items = []
    for dish_id in order_dishes:
        dish_id = int(dish_id.strip())
        for dish in menu:
            if dish['id'] == dish_id and dish['availability'] == 'yes':
                total_price += dish['price']
                order_items.append(dish)
                break
        else:
            print(f"\n{Fore.RED}Error: Dish ID {dish_id} is not available!{Style.RESET_ALL}")
            return

    # Generate a unique order ID
    order_id = len(orders) + 1

    # Set the initial order status as 'received'
    order_status = 'received'

    # Create the order dictionary
    order = {
        'id': order_id,
        'customer': customer_name,
        'items': order_items,
        'total_price': total_price,
        'status': order_status
    }

    orders.append(order)
    save_data()
    print(f"\n{Fore.GREEN}Order placed successfully!{Style.RESET_ALL}")
    print(f"Order ID: {order_id}")


def update_order_status():
    """Update the status of an order"""
    print("\nUpdate Order Status")
    order_id = int(input("Enter the ID of the order to update: "))

    for order in orders:
        if order['id'] == order_id:
            print("\nCurrent Status:", order['status'])
            new_status = input("Enter the new status: ")

            if new_status not in statuses:
                print(f"\n{Fore.RED}Error: Invalid status!{Style.RESET_ALL}")
                return

            order['status'] = new_status
            save_data()
            print(f"\n{Fore.GREEN}Order status updated successfully!{Style.RESET_ALL}")
            return

    print(f"\n{Fore.RED}Error: Order ID not found!{Style.RESET_ALL}")


def review_orders():
    """Review all orders"""
    print("\nReview Orders")
    table = []
    for order in orders:
        table.append([order['id'], order['customer'], order['status']])
    print(tabulate(table, headers=['Order ID', 'Customer', 'Status'], tablefmt="fancy_grid"))


def main():
    """Main function to manage the Zesty Zomato system"""

    print()
    print("========================================================================================")
    print()
    print('                  🍽️   🍴   Z E S T Y   Z O M A T O    🍴   🍽️')
    print()
    print("========================================================================================")
    print()

    load_data()


    while True:
        print("\n---- Zesty Zomato ----")
        print("1. View Menu")
        print("2. Add Dish to Menu")
        print("3. Remove Dish from Menu")
        print("4. Update Dish Availability")
        print("5. Take Order")
        print("6. Update Order Status")
        print("7. Review Orders")
        print("8. Exit")

        choice = input("\nEnter your choice (1-8): ")
        if choice == '1':
            print_menu()
        elif choice == '2':
            add_dish()
        elif choice == '3':
            remove_dish()
        elif choice == '4':
            update_dish_availability()
        elif choice == '5':
            take_order()
        elif choice == '6':
            update_order_status()
        elif choice == '7':
            review_orders()
        elif choice == '8':
            save_data()
            break
        else:
            print(f"\n{Fore.RED}Error: Invalid choice!{Style.RESET_ALL}")

    print(f"\n{Fore.YELLOW}Thank you for using Zesty Zomato!{Style.RESET_ALL}")


# Run the main function
if __name__ == '__main__':
    main()
