from supabase import create_client, Client

url = "https://knkmsszpwvyamvqqsana.supabase.co"
key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imtua21zc3pwd3Z5YW12cXFzYW5hIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTYxMjI1NTAsImV4cCI6MjA3MTY5ODU1MH0.hr2Op4urTZNhVG_fL1m8GRBt3HHiXI2ljXDVqWt9jzc"
supabase: Client = create_client(url, key)

def add_task(Title, Description, Status):
    data = {
        "Title": Title,
        "Description": Description,
        "Status": Status
    }
    response = supabase.table("ToDoss").insert(data).execute()
    return response

def get_tasks():
    response = supabase.table("ToDoss").select("*").execute()
    return response.data

def update_task(task_id, new_Status):
    response = supabase.table("ToDoss").update({"Status": new_Status}).eq("id", task_id).execute()  # fixed
    return response

def delete_task(task_id):
    response = supabase.table("ToDoss").delete().eq("id", task_id).execute()
    return response

