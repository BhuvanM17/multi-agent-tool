from agent import run_agent

def test_queries():
    queries = [
        "How much is a trip to Malleshwaram?",
        "What's the weather like in Indiranagar?",
        "What's the cheapest destination and what's the weather there?",
        "Book a trip from Malleshwaram to Hebbal for Bhuvan",
        "What's the temperature in Koramangala?"
    ]
    
    for query in queries:
        print(f"\n" + "="*50)
        print(f"Testing Query: {query}")
        print("="*50)
        response = run_agent(query)
        print(f"\nFinal Response: {response}")

if __name__ == "__main__":
    test_queries()
