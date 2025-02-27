import json
from datetime import datetime


class Event:
    """Represents a specific event with details for a given date."""

    def __init__(self, event_name, event_date, location, description):
        self.event_name = event_name
        self.event_date = event_date
        self.location = location
        self.description = description

    def __str__(self):
        return f"{self.event_name} on {self.event_date} at {self.location}. Description: {self.description}"


class EventDatabase:
    """A class to manage events and their data."""

    def __init__(self, json_file="events.json"):
        self.json_file = json_file
        self.events = self.load_events()

    def load_events(self):
        """Load events from a JSON file, or create sample data if not found."""
        try:
            with open(self.json_file, "r") as file:
                data = json.load(file)
                return [Event(**event) for event in data]
        except (FileNotFoundError, json.JSONDecodeError):
            print("Event data not found or corrupted. Creating new event data.")
            return self.create_sample_events()

    def create_sample_events(self):
        """Create sample events and save them to a JSON file."""
        events = [
            Event("Welcome Speech", "2025-03-01", "JCU Auditorium",
                  "An introductory speech to kick off the orientation program."),
            Event("Campus Tour", "2025-03-01", "Campus Grounds",
                  "A guided tour of the campus to help new students get familiar."),
            Event("Networking Lunch", "2025-03-01", "Student Center",
                  "A chance to meet and connect with fellow students and faculty.")
        ]
        self.save_events(events)
        return events

    def save_events(self, events):
        """Save events to the JSON file."""
        with open(self.json_file, "w") as file:
            json.dump([event.__dict__ for event in events], file, indent=4)

    def get_event_by_date(self, date):
        """Get events by the specified date."""
        return [event for event in self.events if event.event_date == date]

    def get_event_by_name(self, name):
        """Get event by name."""
        return next((event for event in self.events if event.event_name.lower() == name.lower()), None)


class Chatbot:
    """The Chatbot responds to questions about events based on user input."""

    def __init__(self, event_database):
        self.event_database = event_database

    def process_query(self, user_input):
        """Process the user's query and provide an appropriate response."""
        key = self.match_query(user_input)
        if key == "event_name":
            return self.handle_event_query(self.event_database.get_event_by_name, user_input, "event")
        elif key == "event_date":
            return self.handle_event_query(self.event_database.get_event_by_date, user_input, "date")
        return "I'm sorry, I couldn't understand your query. Could you please rephrase?"

    def match_query(self, user_input):
        """Match user input to event queries like event name or event date."""
        lower_input = user_input.lower()
        if "event" in lower_input:
            return "event_name"
        elif "date" in lower_input:
            return "event_date"
        return None

    def handle_event_query(self, search_function, user_input, query_type):
        """Handle both event name and date queries to avoid redundancy."""
        search_key = user_input.lower().replace(query_type, "").strip()

        if query_type == "date":
            try:
                search_key = datetime.strptime(search_key, "%Y-%m-%d").date().strftime("%Y-%m-%d")
            except ValueError:
                return "Sorry, I couldn't understand the date format. Please use YYYY-MM-DD."

        result = search_function(search_key)
        if result:
            return result if isinstance(result, str) else "\n".join(map(str, result))
        return f"Sorry, I couldn't find any results for '{search_key}'. Please try again."


class User:
    """Represents a user who interacts with the chatbot."""

    def __init__(self, user_name):
        self.user_name = user_name

    def ask_question(self, chatbot):
        """Allow the user to ask a question to the chatbot."""
        question = input(f"{self.user_name}: ")
        response = chatbot.process_query(question)
        print(f"Chatbot: {response}")


def main():
    user_name = input("Please enter your name: ")

    event_database = EventDatabase()
    chatbot = Chatbot(event_database)

    user = User(user_name=user_name)

    print("\nChatbot: Welcome to the Orientation Chatbot!")
    print("You can ask about events in the following ways:")
    print(" - 'event [event name]' to ask about a specific event (e.g., 'event Welcome Speech')")
    print(" - 'date [YYYY-MM-DD]' to ask about events on a specific date (e.g., 'date 2025-03-01')")

    while True:
        user.ask_question(chatbot)
        if input("Do you have another question? (yes/no): ").lower() != "yes":
            print("Chatbot: Goodbye! Have a great orientation!")
            break


if __name__ == "__main__":
    main()