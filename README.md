# Campus Store Order Entry

A Python terminal program that creates new orders for existing customers in a Supabase database. It displays customers and products, validates user input, saves the order through the Supabase API, then queries the database again to verify the order was saved.

## Files

| File | Purpose |
|------|---------|
| `order_entry.py` | Main program: displays tables, validates input, confirms, saves, and verifies orders |
| `database.py` | All Supabase queries (get customers, get products, insert order, get order by ID) |
| `config.py` | Loads the Supabase URL and key from `.env` |
| `supabase.sql` | Creates the tables and sample data in Supabase |
| `requirements.txt` | Required Python packages |
| `.env.example` | Template for your own credentials |

## Setup

1. Clone this repo and open it in VS Code.
2. Install the packages:
   ```
   pip install -r requirements.txt
   ```
3. Create a new Supabase project. Go to **SQL Editor → New query**, paste the contents of `supabase.sql`, and click **Run**. It should show 20 customers, 12 products, and 60 orders.
4. Copy `.env.example` into a new file named `.env` and fill in your own values:
   - `SUPABASE_URL`: Project Settings → Data API → Project URL (without `/rest/v1/`)
   - `SUPABASE_KEY`: Project Settings → API Keys → Secret key (`sb_secret_...`)

`.env` is listed in `.gitignore`, so credentials are never uploaded to GitHub.

## How to Run

```
python order_entry.py
```

## How It Works

- **Display:** On startup, customers and products are pulled from Supabase (not hard-coded or read from CSVs) and shown in two tables. Prices are formatted to two decimals.
- **Validation:** Each input has its own loop. `int()` inside `try/except ValueError` catches text and decimals. IDs are checked against the records loaded from the database, and quantity must be greater than 0. Invalid input shows a message and asks that same question again.
- **Confirm and save:** An order summary is shown and the user enters Y or N (either case). On Y, the order is inserted with the product's current price from the database and today's date. The database generates the order ID. A success message only prints if Supabase returns the saved row. If the request fails, a generic error is shown with no credentials.
- **Verify:** The new order ID from the insert response is used to send a separate query to Supabase. The returned row is displayed in a table, and the total is calculated from the stored `unit_price`. If that query fails or finds nothing, the program reports that verification couldn't be completed and does not insert again.
- **Extra credit:** After each order or cancellation, the user can enter another order. Each order runs inside its own function, so no information carries over from the previous one.

## Testing Results

| Test | Input | Result |
|------|-------|--------|
| Text instead of customer ID | `hello` | ✅ Message shown, asked again |
| Customer ID that doesn't exist | `999` | ✅ Rejected, asked again |
| Product ID that doesn't exist | `999` | ✅ Rejected, asked again |
| Invalid quantities | `0`, `-2`, `1.5`, `hello` | ✅ Each rejected with a message, asked again |
| Cancel at confirmation | `n` | ✅ "Order cancelled. Nothing was saved." No order inserted |
| Confirm a valid order | Customer 5, product 7, quantity 3, `y` | ✅ Exactly one order inserted (order ID 1002) |
| Retrieve the new order | Automatic after saving | ✅ Order 1002 shown in the verification table from a fresh query |
| Extra credit: enter