class User:
    def ask_question(self, chatbot):
        question = input(f"{self.user_name}: Please enter your question. For example, 'event Welcome Speech' or 'date 2025-03-01': ")
        response = chatbot.process_query(question)
        print(f"Chatbot: {response}")

class Chatbot:
    # other code no change

    def handle_event_query(self, search_function, user_input, query_type):
        if query_type == "date":
            try:
                search_key = datetime.strptime(search_key, "%Y-%m-%d").date().strftime("%Y-%m-%d")
            except ValueError:
                return "Sorry, the date format you entered is incorrect. Please use the format YYYY-MM-DD."
        # other code no change
