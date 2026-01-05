from dotenv import load_dotenv
load_dotenv()

import os
from supabase import create_client

url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")

print("URL:", url)
print("KEY starts:", key[:30] if key else None)

client = create_client(url, key)
print("✅ Client criado com sucesso!")

# teste simples
res = client.table("products").select("*").limit(1).execute()
print("✅ Query OK:", res.data)
