import chainlit as cl
import sys
import os

sys.path.append(os.path.abspath("src"))

import chainlit as cl
from chains.interview_chain import start_mock_interview, handle_user_answer
from api.dynamic_faqs import generate_faqs,generate_roadmap
from utils.logger import get_logger


logger = get_logger("mock_interview")
sessions = {}

@cl.on_message
async def main(message):
    logger.info(f"Received message from user: {message.author}, Content: {message.content}")

    if message.author not in sessions:
        # Send a welcome message
        await cl.Message(content="""
**Welcome to the AI Mock Interview Assistant!** 🤖

Here’s what you can do:
- 💬 **Mock Interview:** Type `Mock interview [topic]` to start a mock interview.
  *(Example: Mock interview Data Science)*
- 📚 **FAQs:** Type `FAQs for [topic]` to get frequently asked questions on a topic.
  *(Example: FAQs for Machine Learning)*
- 🎯 **Job Preparation:** Type `Prepare for [job role]` to get job-specific preparation tips.
  *(Example: Prepare for Data Scientist)*

Type one of the commands above to get started!
""").send()

        sessions[message.author] = {"status": "idle"}
        logger.info(f"Initialized session for user: {message.author}")
        return

    session_id = message.author
    user_input = message.content.strip().lower()

    if user_input == "end interview":
        if session_id in sessions and sessions[session_id]["status"] == "in_progress":
            session_data = sessions.pop(session_id, None)  # Remove session data
            if session_data:
                answers = session_data.get("answers", [])
                await cl.Message(content=f"""
                **Mock Interview Ended** 🛑
                You answered {len(answers)} question(s). Here's a summary of your session:
                """ + "\n".join(
                f"- Q: {item['question']}\n  A: {item['answer']}" for item in answers) + """ Thank you for participating in the mock interview! 🎉
                """).send()
            else:
                await cl.Message(content="No session data found. The mock interview has been ended.").send()
            logger.info(f"User {session_id} ended the mock interview.")
        else:
            await cl.Message(content="You are not in a mock interview. Start one by typing `Mock interview [topic]`.").send()
        return

    if user_input.startswith("mock interview"):
        topic = user_input[14:].strip()
        logger.info(f"User {session_id} requested a mock interview on: {topic}")
        questions = generate_faqs(topic)
        if not questions or "No FAQs found" in questions[0]:
            await cl.Message(content=f"No questions available for '{topic}'. Try another topic.").send()
            logger.warning(f"No FAQs found for topic: {topic}")
        else:
            first_question = start_mock_interview(session_id, questions)
            sessions[session_id] = {
                "status": "in_progress",
                "answers": []
            }
            await cl.Message(content=f"Starting mock interview on '{topic}'.\nFirst Question:\n{first_question}").send()

    elif session_id in sessions and sessions[session_id]["status"] == "in_progress":
        user_answer = message.content.strip()
        logger.info(f"User {session_id} answered: {user_answer}")
        feedback, next_question = handle_user_answer(session_id, user_answer)
        sessions[session_id]["answers"].append({
            "question": sessions[session_id]["questions"][sessions[session_id]["current_index"] - 1],
            "answer": user_answer
        })

        await cl.Message(content=f"**Feedback on your answer:**\n{feedback}").send()
        logger.info(f"Feedback provided to user {session_id}: {feedback}")

        if next_question != "The mock interview is complete. Thank you for participating!":
            await cl.Message(content=f"**Next Question:**\n{next_question}").send()
        else:
            sessions[session_id]["status"] = "complete"
            await cl.Message(content=next_question).send()
            logger.info(f"Mock interview completed for user {session_id}")

    elif user_input.startswith("faqs for"):
        topic = user_input[8:].strip()
        logger.info(f"User {session_id} requested FAQs for: {topic}")

        faqs = generate_faqs(topic)
        if not faqs or "No FAQs found" in faqs[0]:
            await cl.Message(content=f"No FAQs found for '{topic}'. Try another topic.").send()
            logger.warning(f"No FAQs found for topic: {topic}")
        else:
            await cl.Message(content=f"**FAQs for '{topic}':**\n" + "\n".join(f"- {faq}" for faq in faqs)).send()

    elif user_input.startswith("prepare for"):
        role = user_input[12:].strip()
        logger.info(f"User {session_id} requested a roadmap for: {role}")
        roadmap = generate_roadmap(role)
        if not roadmap or "No roadmap available" in roadmap[0]:
            await cl.Message(content=f"Sorry, I couldn't generate a roadmap for '{role}'. Try another role.").send()
            logger.warning(f"No roadmap found for role: {role}")
        else:
            await cl.Message(content=f"**Roadmap for '{role}':**\n" + "\n".join(roadmap)).send()
    else:
        await cl.Message(content="I didn't understand that. Please type one of the following commands:\n"
                                 "- `Mock interview [topic]`\n"
                                 "- `FAQs for [topic]`\n"
                                 "- `Prepare for [job role]`\n"
                                 "- `End interview` to stop an ongoing interview.").send()
        logger.warning(f"Invalid command from user {session_id}: {user_input}")