from web_crawler import fetch_web_results
from research_processor import summarize_research_results, generate_answer

if __name__ == "__main__":
    query = input("Enter your research query: ")
    
    # Step 1: Fetch web results
    print(f"\n🔍 Searching for '{query}'...\n")
    results = fetch_web_results(query, num_results=5)

    if results:
        print("\n✅ Extracted Results:\n")
        for idx, res in enumerate(results, start=1):
            print(f"{idx}. [{res['url']}]")

        print("\n📌 Summarizing research data...\n")
        
        # Step 2: Summarize research findings
        summary = summarize_research_results(results)

        print("\n✍️ Generating final answer...\n")
        
        # Step 3: Generate an answer using AI
        answer = generate_answer(summary)

        print("\n✅ Final Response:\n")
        print(answer)
    else:
        print("❌ No relevant data found. Try refining your query.")
