import re
from typing import List, Tuple


class FAQChatbot:
    def __init__(self):
        self.faqs = [
            ("How do I reset my password?", "You can reset your password by clicking 'Forgot Password' on the login page and following the email instructions."),
            ("How can I update my profile?", "You can update your profile by opening Settings and selecting Edit Profile."),
            ("What are your support hours?", "Our support team is available Monday to Friday from 9 AM to 6 PM."),
            ("How do I contact support?", "You can contact support through the help center or by emailing support@example.com."),
            ("What is AI?", "AI, or Artificial Intelligence, is the field of creating systems that can perform tasks that typically require human intelligence such as learning, reasoning, and problem-solving."),
            ("What is data science?", "Data science is the study of extracting useful insights and knowledge from data using statistics, programming, and machine learning."),
            ("What is machine learning?", "Machine learning is a subset of AI where systems learn patterns from data to make predictions or decisions without being explicitly programmed for every case."),
            ("What is the difference between AI and data science?", "AI focuses on building intelligent systems, while data science focuses on analyzing data to discover insights and build predictive models."),
            ("What is NLP?", "NLP, or Natural Language Processing, is a branch of AI that helps computers understand, interpret, and generate human language."),
            ("What is an AI chatbot?", "An AI chatbot is a software application that uses AI to understand questions and provide human-like responses."),
        ]
        self.faq_lookup = {self.preprocess(question): answer for question, answer in self.faqs}
        self.stopwords = {
            "a", "an", "and", "are", "can", "do", "for", "from", "how", "i", "is", "my", "on",
            "or", "please", "the", "to", "what", "your"
        }

    def preprocess(self, text: str) -> str:
        text = text.lower()
        text = re.sub(r"[^a-z0-9\s]", " ", text)
        text = re.sub(r"\s+", " ", text).strip()
        return text

    def _tokenize(self, text: str) -> List[str]:
        tokens = self.preprocess(text).split()
        return [token for token in tokens if token not in self.stopwords]

    def _similarity(self, query: str, faq: str) -> float:
        q_tokens = self._tokenize(query)
        f_tokens = self._tokenize(faq)
        if not q_tokens or not f_tokens:
            return 0.0

        q_set = set(q_tokens)
        f_set = set(f_tokens)
        overlap = len(q_set & f_set)
        if overlap == 0:
            return 0.0

        precision = overlap / len(q_set)
        recall = overlap / len(f_set)
        return (precision + recall) / 2

    def find_best_match(self, query: str) -> Tuple[str, str] | None:
        best_match = None
        best_score = 0.0

        for question, answer in self.faqs:
            score = self._similarity(query, question)
            if score > best_score:
                best_score = score
                best_match = (question, answer)

        if best_match and best_score >= 0.2:
            return best_match
        return None

    def generate_response(self, query: str) -> str:
        if not query or not query.strip():
            return "Please enter a question so I can help you."

        exact_key = self.preprocess(query)
        if exact_key in self.faq_lookup:
            return self.faq_lookup[exact_key]

        match = self.find_best_match(query)
        if match:
            return match[1]
        return "Sorry, I couldn't find an answer to that. Please contact support for further help."


if __name__ == "__main__":
    chatbot = FAQChatbot()
    print("FAQ Chatbot is ready. Type 'exit' to quit.")
    while True:
        user_input = input("You: ").strip()
        if user_input.lower() in {"exit", "quit"}:
            print("Goodbye!")
            break
        print("Bot:", chatbot.generate_response(user_input))
