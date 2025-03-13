import spacy
nlp = spacy.load('en_core_web_sm')

class Chatbot:
    # other code no change

    def match_query(self, user_input):
        doc = nlp(user_input)
        keywords = [token.text for token in doc if token.pos_ in ['NOUN', 'VERB']]
        if 'event' in keywords or any([word in ['speech', 'tour', 'lunch'] for word in keywords]):
            return 'event_name'
        elif 'date' in keywords:
            return 'event_date'
        return None

    def handle_event_query(self, search_function, user_input, query_type):
        doc = nlp(user_input)
        search_key = ''.join([token.text for token in doc if token.pos_ in ['NOUN', 'VERB']]).lower().replace(query_type, '').strip()
        # other code no change
