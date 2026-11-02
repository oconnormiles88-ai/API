# order_entry.py
# terminal program for entering new orders and double checking they saved in supabase
from database import get_customers, get_products, insert_order, get_order


def load_data():
    # grab customers and products from supabase and store them by id
    # so checking if an id exists later is just a quick lookup
    customers = {}
    for customer in get_customers():
        customers[customer["customer_id"]] = customer

    products = {}
    for product in get_products():
        products[product["product_id"]] = product

    return customers, products


def show_customers(customers):
    print("\nCUSTOMERS")
    print(f"{'ID':<6}{'Name':<20}")
    print("-" * 26)
    for customer_id, customer in customers.items():
        print(f"{customer_id:<6}{customer['name']:<20}")


def show_products(products):
    print("\nPRODUCTS")
    print(f"{'ID':<6}{'Product':<18}{'Price':>10}")
    print("-" * 34)
    for product_id, product in products.items():
        price_text = f"${float(product['price']):.2f}"
        print(f"{product_id:<6}{product['product_name']:<18}{price_text:>10}")


def ask_for_id(prompt, valid_ids, label):
    # keeps asking until they type a whole number that actually exists in the table
    while True:
        entry = input(prompt).strip()
        try:
            number = int(entry)
        except ValueError:
            print(f"'{entry}' isn't a valid {label} ID. Enter a whole number from the table.")
            continue
        if number in valid_ids:
            return number
        print(f"There's no {label} with ID {number}. Pick one from the table above.")


def ask_for_quantity():
    # int() fails on text and decimals like 1.5, then we also block 0 and negatives
    while True:
        entry = input("Enter quantity: ").strip()
        try:
            quantity = int(entry)
        except ValueError:
            print(f"'{entry}' isn't a whole number. Enter something like 1, 2, or 3.")
            continue
        if quantity > 0:
            return quantity
        print("Quantity has to be at least 1.")


def ask_yes_no(prompt):
    # only takes y or n (upper or lowercase), anything else gets asked again
    while True:
        answer = input(prompt).strip().lower()
        if answer == "y":
            return True
        if answer == "n":
            return False
        print("Please enter Y or N.")


def show_summary(customer, product, quantity):
    unit_price = float(product["price"])
    total = quantity * unit_price
    print("\nORDER SUMMARY")
    print(f"Customer:   {customer['name']}")
    print(f"Product:    {product['product_name']}")
    print(f"Quantity:   {quantity}")
    print(f"Unit price: ${unit_price:.2f}")
    print(f"Total:      ${total:.2f}")


def save_order(customer_id, product_id, quantity, unit_price):
    # tries the insert and only says success if supabase sends the saved row back
    try:
        saved = insert_order(customer_id, product_id, quantity, unit_price)
    except Exception:
        # generic message on purpose so no url or key ever gets printed
        print("\nError: couldn't save the order to Supabase. Check your internet connection and try again.")
        return None

    if saved is None:
        print("\nError: Supabase didn't confirm the order, so it was not saved.")
        return None

    print(f"\nSuccess! Order saved with order ID {saved['order_id']}.")
    return saved


def verify_order(order_id, customers, products):
    # sends a brand new query to supabase to prove the order is really there
    try:
        order = get_order(order_id)
    except Exception:
        order = None

    if order is None:
        # just report it, never try inserting again
        print(f"Verification could not be completed for order ID {order_id}.")
        return

    show_order_table(order, customers, products)


def show_order_table(order, customers, products):
    # total uses the unit_price stored in the database, not what we sent
    customer_name = customers[order["customer_id"]]["name"]
    product_name = products[order["product_id"]]["product_name"]
    unit_price = float(order["unit_price"])
    total = order["quantity"] * unit_price
    price_text = f"${unit_price:.2f}"
    total_text = f"${total:.2f}"

    print("\nVERIFIED ORDER (pulled fresh from Supabase)")
    header = f"{'Order ID':<10}{'Customer':<16}{'Product':<16}{'Qty':>5}{'Unit Price':>12}{'Total':>10}  Order Date"
    print(header)
    print("-" * len(header))
    print(f"{order['order_id']:<10}{customer_name:<16}{product_name:<16}{order['quantity']:>5}{price_text:>12}{total_text:>10}  {order['order_date']}")


def place_one_order(customers, products):
    # everything for one order lives in here, so nothing carries over to the next one
    customer_id = ask_for_id("\nEnter customer ID: ", customers, "customer")
    product_id = ask_for_id("Enter product ID: ", products, "product")
    quantity = ask_for_quantity()

    customer = customers[customer_id]
    product = products[product_id]
    show_summary(customer, product, quantity)

    if not ask_yes_no("Confirm this order? (Y/N): "):
        print("Order cancelled. Nothing was saved.")
        return

    saved = save_order(customer_id, product_id, quantity, float(product["price"]))
    if saved is not None:
        verify_order(saved["order_id"], customers, products)


def main():
    print("=== Campus Store Order Entry ===")
    try:
        customers, products = load_data()
    except Exception:
        print("Couldn't load customers and products from Supabase. Check your .env file and internet connection.")
        return

    # extra credit: keep going until they say no
    while True:
        show_customers(customers)
        show_products(products)
        place_one_order(customers, products)
        if not ask_yes_no("\nEnter another order? (Y/N): "):
            print("Goodbye!")
            break


if __name__ == "__main__":
    main()