import re

class phrase_counter: 
    @staticmethod
    def count_query_occurrences(text, query):
        # Conta quantas vezes a query aparece no texto
        return len(re.findall(re.escape(query), text, re.IGNORECASE))

    @classmethod
    def count_query_in_data(cls, data, query):
        count = 0
        # Verifica em headings e paragraphs
        text_fields = data["newsData"]["headings"] + data["newsData"]["paragraphs"]
        for text in text_fields:
            count += cls.count_query_occurrences(text, query)
        return count