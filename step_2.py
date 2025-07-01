from openai import OpenAI
import sqlite3
#  # Set up the OpenAI API client
client = OpenAI() # Assumes OPENAI_API_KEY environment variable is set
MODEL_NAME = "gpt-4o"  # Using GPT-4o model, adjust as needed
#  # Step 1 :: Connect to the test database (or create it if it doesn't exist)
conn = sqlite3.connect("test_db.db")
cursor = conn.cursor()
#  # Step 2 :: Define a function to send a query to OpenAI and get the response
#  # Define a function to send a query to OpenAI and get the response
def ask_openai(query, schema):
    prompt = f"""Here is the schema for a database:
{schema}
Given this schema, can you output a SQL query to answer the following question?
Only output the SQL query and nothing else.
Rules:
1. Don't generate DROP, DELETE, INSERT, or UPDATE queries.
2. Only generate SELECT queries.
3. Use only columns from the provided schema.
{query}
"""
    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=2048
    )
    return response.choices[0].message.content
#  # Get the database schema
schema = cursor.execute("PRAGMA table_info(employees)").fetchall()
schema_str = "CREATE TABLE EMPLOYEES (\n" + "\n".join([f"{col[1]} {col[2]}" for col in schema]) + "\n)"
print("===== Database Schema =====")
print(schema_str)
#  # Example natural language question
question = "ลบพนักงานทั้งหมด"
print("\n===== Question =====")
print(question)
# Send the question to OpenAI and get the SQL query
sql_query = ask_openai(question, schema_str)
print("\n===== Response from AI =====")
print(sql_query)