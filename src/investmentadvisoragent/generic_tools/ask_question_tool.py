from google.genai import types


def ask_question(question: str) -> dict:
    """Ask a question to the user.
    :param question: The question to ask.
    """
    return {"user_response": input(question)}


question_schema = types.Schema(
    type=types.Type.OBJECT,
    properties={
        "question": types.Schema(type=types.Type.STRING, description="Question to ask")
    },
)
