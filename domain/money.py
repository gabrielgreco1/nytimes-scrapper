import re

class moneychecker:
    @staticmethod
    def contains_money(text):
        money_pattern = (
            r"\$(?:\d{1,3}(?:,\d{3})*|\d+)(?:\.\d+)?(?:\s(?:million|billion|trillion))?"  # $ format
            r"|\d+\s(?:dollars|USD)"  # dollars or USD format
        )
        return bool(re.search(money_pattern, text))
    
    @classmethod
    def check_data_for_money(cls, data):
        # Verifica em headings e paragraphs
        text_fields = data["newsData"]["headings"] + data["newsData"]["paragraphs"]
        return any(cls.contains_money(text) for text in text_fields)
