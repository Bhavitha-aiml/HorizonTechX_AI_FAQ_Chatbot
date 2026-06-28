import unittest

from chatbot import FAQChatbot


class FAQChatbotTests(unittest.TestCase):
    def setUp(self):
        self.chatbot = FAQChatbot()

    def test_finds_matching_faq_for_similar_query(self):
        response = self.chatbot.generate_response("How do I reset my password?")
        self.assertIn("password", response.lower())
        self.assertIn("reset", response.lower())

    def test_matches_support_query(self):
        response = self.chatbot.generate_response("How can I contact support?")
        self.assertIn("support", response.lower())

    def test_matches_exact_nlp_question(self):
        response = self.chatbot.generate_response("What is NLP?")
        self.assertIn("natural language processing", response.lower())

    def test_returns_fallback_for_unknown_query(self):
        response = self.chatbot.generate_response("What is the weather today?")
        self.assertIn("sorry", response.lower())


if __name__ == "__main__":
    unittest.main()
