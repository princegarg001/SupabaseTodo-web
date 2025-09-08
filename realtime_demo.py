import asyncio
from supabase import create_client, AsyncClient

url = "https://knkmsszpwvyamvqqsana.supabase.co"
key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imtua21zc3pwd3Z5YW12cXFzYW5hIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTYxMjI1NTAsImV4cCI6MjA3MTY5ODU1MH0.hr2Op4urTZNhVG_fL1m8GRBt3HHiXI2ljXDVqWt9jzc"

async def main():
    # ✅ Use AsyncClient explicitly
    supabase: AsyncClient = create_client(url, key, is_async=True)

    # Create a realtime channel
    channel = supabase.channel("db-changes")

    # Subscribe to Postgres changes on "tasks" table
    channel.on(
        "postgres_changes",
        {
            "event": "*",   # can be "INSERT", "UPDATE", "DELETE"
            "schema": "public",
            "table": "tasks"
        },
        lambda payload: print("📢 Change received:", payload)
    )

    # Subscribe
    await channel.subscribe()
    print("✅ Listening for realtime changes...")

    # Keep program alive
    while True:
        await asyncio.sleep(1)

if __name__ == "__main__":
    asyncio.run(main())
