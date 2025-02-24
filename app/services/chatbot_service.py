import openai


def chatbot_query(user_message: str, conversation_history: list) -> str:
    """
    Takes the user's message and a list of past messages,
    returns the LLM response.
    Each message in conversation_history is a dict with keys 'role' and 'content'.
    """
    conversation_history.append({"role": "user", "content": user_message})

    # Call the LLM
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=conversation_history,
        temperature=0.7,
    )
    answer = response.choices[0].message["content"]

    # Add assistant response to the conversation
    conversation_history.append({"role": "assistant", "content": answer})
    return answer
