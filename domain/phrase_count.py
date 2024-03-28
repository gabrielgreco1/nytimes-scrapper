import re

class phrase_counter: 
    @staticmethod
    def count_query_occurrences(text, query):
        # Counts how many times the query appears in the text
        return len(re.findall(re.escape(query), text, re.IGNORECASE))

    @classmethod
    def count_query_in_data(cls, data, query):
        count = 0
        # Check headings and paragraphs
        text_fields = data["newsData"]["headings"] + data["newsData"]["paragraphs"]
        for text in text_fields:
            count += cls.count_query_occurrences(text, query)
        return count