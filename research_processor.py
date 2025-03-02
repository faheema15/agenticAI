import os
import re
from dotenv import load_dotenv
from langchain_huggingface import HuggingFaceEndpoint
from langchain.chains.summarize import load_summarize_chain
from langchain_core.documents import Document  
from langchain_core.prompts import PromptTemplate
from huggingface_hub import InferenceClient

# Load environment variables
load_dotenv()
HUGGINGFACEHUB_API_TOKEN = os.getenv("HUGGINGFACEHUB_API_TOKEN")

llm = HuggingFaceEndpoint(
    repo_id="mistralai/Mistral-7B-Instruct-v0.3",
    temperature=0.3,
    huggingfacehub_api_token=HUGGINGFACEHUB_API_TOKEN
)

def clean_text(text):
    """Cleans text by removing duplicate lines, excessive whitespace, and non-printable characters."""
    if isinstance(text, dict):  
        text = text.get("text", "")  

    # Remove duplicate lines
    lines = text.split("\n")
    seen = set()
    unique_lines = []
    for line in lines:
        clean_line = line.strip()
        if clean_line and clean_line not in seen:
            seen.add(clean_line)
            unique_lines.append(clean_line)

    text = "\n".join(unique_lines)

    # Normalize spaces and remove non-printable characters
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'[^\x20-\x7E]', '', text)  # Keep only printable ASCII

    return text.strip()


def summarize_research_results(results):
    """
    Summarizes research results using Mistral-7B LLM.
    Returns a structured, detailed summary.
    """
    if not results:
        return "No research data available to summarize."

    # Create documents from search results
    documents = [Document(page_content=result["content"]) for result in results if "content" in result]

    # Use map_reduce for better summarization
    summary_chain = load_summarize_chain(llm, chain_type="map_reduce")
    summary_output = summary_chain.invoke(documents)

    # Ensure summary is a string
    if isinstance(summary_output, dict) and "text" in summary_output:
        summary_text = summary_output["text"]
    elif isinstance(summary_output, str):
        summary_text = summary_output
    else:
        summary_text = "Summarization failed."

    cleaned_summary = clean_text(summary_text)

    # Format in a structured manner
    structured_summary = f"""
📌 Research Summary on {results[0].get('title', 'AI in Medicine')}

🔹 Overview:
{cleaned_summary}

🔹 Key Findings:
- {results[0].get("content", "N/A")}
- {results[1].get("content", "N/A")}
- {results[2].get("content", "N/A")}
- {results[3].get("content", "N/A")}
- {results[4].get("content", "N/A")}

🔹 Further Reading:
1. [Read more]({results[0].get('url', '#')})
2. [Read more]({results[1].get('url', '#')})
3. [Read more]({results[2].get('url', '#')})
4. [Read more]({results[3].get('url', '#')})
5. [Read more]({results[4].get('url', '#')})

"""

    return structured_summary

client = InferenceClient(
    model="mistralai/Mistral-7B-Instruct-v0.3",
    token=HUGGINGFACEHUB_API_TOKEN
)

import re

def generate_answer(summary):
    """
    Generates a structured response with proper paragraph spacing and list formatting.
    """
    if not summary:
        return "No sufficient data to generate an answer."

    structured_prompt = f"""
    You are an expert AI researcher. Based on the following research summary, generate a structured response with the following sections:

    Introduction
    Applications
    Challenges and Limitations
    Future Potential
    Conclusion

    Ensure:
    - Proper paragraph spacing (one blank line between sections)
    - Numbered and bulleted lists formatted correctly

    Research Summary:
    {summary}
    """

    response = client.chat_completion(messages=[{"role": "user", "content": structured_prompt}], max_tokens=1000)

    answer_text = response["choices"][0]["message"]["content"]

    # Ensure consistent spacing with two newlines before each section
    formatted_answer = re.sub(r'(\n\s*){2,}', '\n\n', answer_text.strip())  # Normalize multiple newlines
    formatted_answer = re.sub(r'(Introduction|Applications|Challenges and Limitations|Future Potential|Conclusion):', r'\n\n\1:\n', formatted_answer)  # Ensure section separation

    # Ensure proper spacing for lists (bullets and numbered)
    formatted_answer = re.sub(r'(\n)(\d+\.)', r'\1\n\2', formatted_answer)  # Add blank lines before numbered lists
    formatted_answer = re.sub(r'(\n)(- )', r'\1\n\2', formatted_answer)  # Add blank lines before bulleted lists

    return formatted_answer.strip()