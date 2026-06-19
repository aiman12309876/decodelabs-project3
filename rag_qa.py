import google.generativeai as genai

genai.configure(api_key="YOUR_API_KEY_HERE")

def create_context():
    context = """
    DecodeLabs is a technology training and internship platform based in Lucknow, India. 
    It was founded in 2022 by a team of experienced software engineers and educators. 
    The company offers internship programs in various domains including Artificial Intelligence, 
    Machine Learning, Data Science, Web Development, Cloud Computing, Cybersecurity, and DevOps.
    
    DecodeLabs has trained over 5,000 students across India and Pakistan. 
    The internship duration ranges from 1 to 3 months depending on the program. 
    All interns receive a certificate of completion and a letter of recommendation upon successful 
    completion of their projects.
    
    The company has partnerships with over 50 tech companies for placement assistance. 
    DecodeLabs is headquartered in Greater Lucknow, India, with remote teams working globally.
    """
    return context

def ask_question(question, reference_text, model_name="gemini-1.5-pro"):
    prompt = f"""
You are a strict, closed-book question-answering assistant. Your task is to answer questions using ONLY the reference text provided below.

IMPORTANT RULES:
1. You MUST ONLY use information from the reference text.
2. Do NOT use any outside knowledge, assumptions, or guesses.
3. If the answer is NOT present in the reference text, reply with: "Information Not Found"
4. For every claim you make, cite the exact sentence or paragraph from the reference text.
5. Do not add any conversational filler or extra text.

REFERENCE TEXT:
{reference_text}

QUESTION: {question}

YOUR RESPONSE:
"""

    model = genai.GenerativeModel(
        model_name,
        generation_config={
            "temperature": 0.0,
            "top_p": 1.0,
        }
    )

    response = model.generate_content(prompt)
    return response.text.strip()

def main():
    print("\n" + "=" * 60)
    print("   CONTEXT-ANCHORED ANSWERING (RAG BASICS)")
    print("=" * 60)

    reference_text = create_context()
    
    print("\n📄 Reference Text Loaded:")
    print("-" * 60)
    print(reference_text)
    print("-" * 60)

    questions = [
        "Where is DecodeLabs headquartered?",
        "When was DecodeLabs founded?",
        "How many students has DecodeLabs trained?",
        "Does DecodeLabs offer internships in blockchain?",
        "What is the duration of the internship?",
        "What is the name of the CEO of DecodeLabs?",
        "Does DecodeLabs provide placement assistance?"
    ]

    print("\n📋 Questions & Answers:")
    print("=" * 60)

    for i, question in enumerate(questions, 1):
        print(f"\n[{i}] Q: {question}")
        answer = ask_question(question, reference_text)
        print(f"   A: {answer}")

    print("\n" + "=" * 60)
    print("   RAG QA COMPLETE")
    print("=" * 60)

if __name__ == "__main__":
    main()