import random


def chatbot_response(user_input):
    """Provide answers to orientation event-related questions."""
    responses = {
        "schedule": "The orientation schedule includes a welcome speech at 9 AM, campus tour at 11 AM, and networking lunch at 1 PM.",
        "location": "The orientation events will take place in the JCU, Room A208.",
        "activities": "Orientation includes interactive sessions, ice-breaking games, and faculty introductions.",
        "contact": "You can contact the Student Affairs Office at (123) 456-7890 for more information."
    }

    for key in responses:
        if key in user_input.lower():
            return responses[key]

    return "I'm sorry, I don't have that information. Please check the official website or contact Student Affairs."


def main():
    print(
        "Welcome to the Orientation Chatbot! Ask me about the orientation schedule, location, activities, or contact info.")
    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit"]:
            print("Goodbye! Have a great orientation.")
            break
        response = chatbot_response(user_input)
        print("Chatbot:", response)


if __name__ == "__main__":
    main()
