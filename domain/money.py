import re

class moneychecker:
    @staticmethod
    def contains_money(text):
        # Create a pattern to run a search for Dollars, USD or $
        money_pattern = (
            r"\$(?:\d{1,3}(?:,\d{3})*|\d+)(?:\.\d+)?(?:\s(?:million|billion|trillion))?"  
            r"|\d+\s(?:dollars|USD)"  
        )
        return bool(re.search(money_pattern, text))
    
    @classmethod
    def check_data_for_money(cls, data):
        # Verify headings and paragraphs
        text_fields = data["newsData"]["headings"] + data["newsData"]["paragraphs"]
        return any(cls.contains_money(text) for text in text_fields)
