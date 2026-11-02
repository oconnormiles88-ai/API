# database.py
# all the supabase stuff lives here so order_entry.py doesn't have to deal with it
from datetime import date
from supabase import create_client
from config import SUPABASE_URL, SUPABASE_KEY

# one connection that every function below shares
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)


def get_customers():
    # just need the id and name for the customer table
    response = supabase.table("customers").select("customer_id, name").order("customer_id").execute()
    return response.data


def get_products():
    # id, name, and price. price matters later for the order total
    response = supabase.table("products").select("product_id, product_name, price").order("product_id").execute()
    return response.data


def insert_order(customer_id, product_id, quantity, unit_price):
    # no order_id here on purpose, the database makes that itself
    new_order = {
        "customer_id": customer_id,
        "product_id": product_id,
        "quantity": quantity,
        "order_date": date.today().isoformat(),  # today's date as "2026-11-02"
        "unit_price": unit_price,
    }
    response = supabase.table("orders").insert(new_order).execute()
    # supabase sends back the saved row with its new order_id. empty means it didn't save
    if response.data:
        return response.data[0]
    return None


def get_order(order_id):
    # brand new query to double check the order actually made it into the database
    response = supabase.table("orders").select("*").eq("order_id", order_id).execute()
    if response.data:
        return response.data[0]
    return None


# quick connection test, only runs when you do "python database.py" directly
if __name__ == "__main__":
    customers = get_customers()
    products = get_products()
    print(f"Connected! Found {len(customers)} customers and {len(products)} products.")