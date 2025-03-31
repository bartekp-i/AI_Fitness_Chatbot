import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI(api_key=os.getenv("MY_KEY"))


def get_chat_response(user_message: str, conversation_history: list) -> (str, list):

    # 2. Greeting check
    greeting_keywords = ["hi", "hello", "hey", "good day"]
    if user_message.lower().strip() in greeting_keywords:
        greeting_response = "Hi! How can I help you with your fitness goals today?"
        conversation_history.append({"role": "assistant", "content": greeting_response})
        return greeting_response, conversation_history

    # 3. Call GPT
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a fitness expert. Respond only to fitness-related queries such as "
                        "workouts, nutrition, recovery, or similar topics. If the query is unrelated, "
                        "respond with: 'I'm sorry, I only provide advice related to fitness. Please ask "
                        "me questions about workouts, nutrition, recovery, or similar topics.' "
                        "Ensure your responses are plain text without any special formatting. "
                        "Use simple, friendly language and do not end a sentence in the middle."
                    )
                },
                {
                    "role": "user",
                    "content": user_message
                }
            ],
            max_tokens=140,
            temperature=0.7,
        )

        reply = response.choices[0].message.content.strip()
        conversation_history.append({"role": "assistant", "content": reply})
        return reply, conversation_history

    except Exception as e:
        # In case of error, we print the error for debugging and return a fallback message
        print("Error from OpenAI API:", e)
        error_message = (
            "I'm sorry, I only provide advice related to fitness. "
            "Please ask me questions about workouts, nutrition, recovery, or similar topics."
        )
        conversation_history.append({"role": "assistant", "content": error_message})
        return error_message, conversation_history
