import streamlit as st
from web_crawler import fetch_web_results
from research_processor import summarize_research_results, generate_answer

def main():
    st.title("🔍 Deep Research AI Agent")
    st.write("Enter your research query below and let the AI gather and analyze data for you.")

    query = st.text_input("Enter your research topic:")
    if st.button("Search & Analyze") and query:
        
        # Step 1: Fetch web results
        results = fetch_web_results(query, num_results=5)
        
        if results:
            # Step 2: Summarize research findings
            summary = summarize_research_results(results)

            # Step 3: Generate AI answer
            answer = generate_answer(summary)
            
            st.write(answer)
            
            # Display further reading links
            st.subheader("Further Reading")
            for idx, res in enumerate(results, start=1):
                st.markdown(f"{idx}. [Read more]({res['url']})")
        else:
            st.error("❌ No relevant data found. Try refining your query.")

if __name__ == "__main__":
    main()
