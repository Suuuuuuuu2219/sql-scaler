import os
import requests
import json
from openai import OpenAI

# Configuration
BASE_URL = "http://localhost:7860"
MODEL = "gpt-4o-mini"

# Initialize OpenAI client
# Expects OPENAI_API_KEY environment variable
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY", "sk-placeholder"))

def optimize_query(schema, query):
    """Call OpenAI to optimize the SQL query."""
    prompt = f"""
    Optimize the following SQL query for performance while preserving correctness.
    
    SCHEMA:
    {json.dumps(schema, indent=2)}
    
    QUERY:
    {query}
    
    Return ONLY the optimized SQL query. Do not include any explanations or markdown formatting.
    """
    
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": "You are an expert SQL performance engineer."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.0
    )
    
    return response.choices[0].message.content.strip()

def main():
    print("🚀 SQL Scaler: Baseline Inference")
    print(f"Connecting to environment at {BASE_URL}...")
    
    # 1. Reset
    try:
        reset_resp = requests.post(f"{BASE_URL}/reset")
        if reset_resp.status_code != 200:
            print(f"❌ Reset failed: {reset_resp.text}")
            return
            
        observation = reset_resp.json()
        print(f"✅ Reset successful. Current Task: {observation['difficulty']}")
        print(f"Original Query: {observation['query']}")
        
        # 2. Get Optimization from LLM
        print(f"🤖 Optimizing with {MODEL}...")
        optimized_sql = optimize_query(observation['schema'], observation['query'])
        print(f"Suggested Optimization: {optimized_sql}")
        
        # 3. Step
        step_payload = {"optimized_query": optimized_sql}
        step_resp = requests.post(f"{BASE_URL}/step", json=step_payload)
        
        if step_resp.status_code != 200:
            print(f"❌ Step failed: {step_resp.text}")
            return
            
        result = step_resp.json()
        print("\n--- 🏁 RESULT ---")
        print(f"Reward: {result['reward']}")
        print(f"Done: {result['done']}")
        print(f"Info: {json.dumps(result['info'], indent=2)}")
        
    except requests.exceptions.ConnectionError:
        print(f"❌ ERROR: Connection failed. Ensure the server is running at {BASE_URL}")

if __name__ == "__main__":
    main()
