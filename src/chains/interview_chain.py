from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate


llm = ChatOpenAI(temperature=0.7)
mock_interview_memory = {}

def start_mock_interview(session_id, topic_questions):
    mock_interview_memory[session_id] = {
        "questions": topic_questions,
        "current_index": 0,
        "answers": []
    }
    return topic_questions[0]  

def handle_user_answer(session_id, user_answer):
    """
    Handle user's answer, provide feedback, and return the next question.
    """
    session = mock_interview_memory.get(session_id)
    if not session:
        return "Session not found. Please start a new mock interview."

    questions = session["questions"]
    current_index = session["current_index"]

   
    if current_index >= len(questions):
        return "The mock interview is complete. Thank you for participating!"

    current_question = questions[current_index]

    session["answers"].append({
        "question": current_question,
        "answer": user_answer
    })

    prompt = PromptTemplate(
        input_variables=["question", "answer"],
        template="""
        You are an interviewer. Evaluate the following question and answer:
        Question: {question}
        Answer: {answer}

        Provide detailed feedback, including strengths, weaknesses, and improvement suggestions.
        """
    )
    feedback = llm.predict(prompt.format(question=current_question, answer=user_answer))

    session["current_index"] += 1
    if session["current_index"] < len(questions):
        next_question = questions[session["current_index"]]
    else:
        next_question = "The mock interview is complete. Thank you for participating!"

    return feedback, next_question