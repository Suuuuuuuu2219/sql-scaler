import os
import requests
import json
from openai import OpenAI

# Configuration
API_URL = os.environ.get("OPENENV_API_URL", "http://localhost:7860")
MODEL = "gpt-4o-mini"

# Initialize OpenAI client
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY", "sk-placeholder"))

def optimize_sql(observation):
    """
    Agent logic to optimize the SQL query based on observation.
    """
    query = observation.get("query")
    schema = observation.get("schema")
    difficulty = observation.get("difficulty")
    
    prompt = f"""
    You are an expert SQL performance engineer.
    Your task is to optimize the following SQL query for performance while maintaining functional correctness.
    
    DIFFICULTY: {difficulty}
    
    SCHEMA:
    {json.dumps(schema, indent=2)}
    
    ORIGINAL QUERY:
    {query}
    
    STRICT RULE: Return ONLY the optimized SQL query. No markdown, no prefixes, no explanations. 
    If the query is already optimal, return it as is.
    """
    
    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": "You are a professional SQL optimizer."},
                {"role": "user", "content": prompt}
            ],
            temperature=0,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"❌ LLM Inference Error: {e}")
        return query # Fallback to original

def run_inference():
    print("🚀 Starting SQL Scaler Inference...")
    print(f"🔗 Target Environment: {API_URL}")
    
    try:
        # 1. Reset Environment
        print("🔄 Resetting environment...")
        reset_response = requests.post(f"{API_URL}/reset")
        reset_response.raise_for_status()
        obs = reset_response.json()
        
        print(f"📍 Task Level: {obs.get('difficulty').upper()}")
        print(f"📝 Original Query: {obs.get('query')}")
        
        # 2. Get Agent Action
        print("🤖 LLM is optimizing...")
        optimized_query = optimize_sql(obs)
        print(f"✨ Optimized Query: {optimized_query}")
        
        # 3. Step Environment
        print("👟 Stepping environment...")
        step_response = requests.post(
            f"{API_URL}/step", 
            json={"optimized_query": optimized_query}
        )
        step_response.raise_for_status()
        result = step_response.json()
        
        # 4. Show Results
        print("\n" + "="*40)
        print("📊 FINAL RESULTS")
        print("="*40)
        print(f"🏆 Reward: {result.get('reward')}")
        print(f"🏁 Done: {result.get('done')}")
        
        if 'metadata' in result:
             print(f"🔍 Grader Info: {json.dumps(result['metadata'], indent=2)}")
        elif 'info' in result:
             print(f"🔍 Info: {json.dumps(result['info'], indent=2)}")
             
        print("="*40)

    except requests.exceptions.ConnectionError:
        print(f"❌ Error: Could not connect to {API_URL}. Ensure the server is running.")
    except Exception as e:
        print(f"❌ Unexpected Error: {e}")

if __name__ == "__main__":
    if os.environ.get("OPENAI_API_KEY") == "sk-placeholder" or not os.environ.get("OPENAI_API_KEY"):
        print("⚠️  Warning: OPENAI_API_KEY not set. Using placeholder (will likely fail).")
    run_inference()
