from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate

def generate_faqs(topic):
    llm = ChatOpenAI(temperature=0.7)
    prompt = PromptTemplate(
        input_variables=["topic"],
        template="""
        You are an expert in {topic}. Generate a list of 5 frequently asked questions (FAQs)
        that people often ask about this topic. Provide them in bullet points.
        """
    )
    response = llm.predict(prompt.format(topic=topic))
    return response.split("\n")
def generate_roadmap(role):
    """Generate a detailed roadmap for a specific job role using OpenAI."""
    llm = ChatOpenAI(temperature=0.7)
    prompt = PromptTemplate(
        input_variables=["role"],
        template="""
        You are an expert career coach. Provide a detailed preparation roadmap for someone aspiring to become a {role}.
        The roadmap should include:
        1. Key skills to learn.
        2. Certifications or courses to pursue.
        3. Projects to work on.
        4. Common challenges and how to overcome them.
        5. Important industry trends to stay updated on.

        Make the roadmap actionable and realistic, dividing it into short-term (1-3 months), mid-term (4-6 months), and long-term (6+ months) goals.
        """
    )
    response = llm.predict(prompt.format(role=role))
    return response.split("\n")