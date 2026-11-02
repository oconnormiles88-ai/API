# config.py
# pulls the supabase url and key out of .env so they're never written in the code itself
import os
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# if either one's missing, stop right away with a clear message instead of a confusing error later
if not SUPABASE_URL or not SUPABASE_KEY:
    raise SystemExit("Missing SUPABASE_URL or SUPABASE_KEY. Check your .env file.")