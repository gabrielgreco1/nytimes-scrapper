import pandas as pd
import os

class save:
    def __init__(self, excel_path):
        self.excel_path = excel_path
        
    def save_to_xlsx(self, data):
            # Sets the base text of the unwanted link for checking
            undesired_links_texts = [
                                    "https://www.nytimes.com/search?dropmab=false",
                                    "https://www.nytimes.com/topic/"
            ]        
            # Checks if any link in the list contains the base text
            if any(any(base_text in link for base_text in undesired_links_texts) for link in data["newsData"]["links"]):
                return
                    
            # Unpack the data
            news_data = data["newsData"]
            image_urls = data["imageUrls"]
            contains_money = 'T' if data["newsData"]["containsMoney"] else 'F'
            
            # Selects the second paragraph of "paragraphs" as specified
            selected_paragraph = news_data["paragraphs"][1] if len(news_data["paragraphs"]) > 1 else None
            
            # Preparing the data for DataFrame
            data_for_df = {
                "headings": [news_data["headings"][0]] if news_data["headings"] else [None],
                "date": [news_data["date"][0]] if news_data["date"] else [None],
                "paragraphs": [selected_paragraph],
                "links": [news_data["links"][0]] if news_data["links"] else [None],
                "image_urls": [image_urls[0]] if image_urls else "No image available",
                "imagefile_path":news_data["savePath"],
                "containsMoney": contains_money,
                "phraseCounter": news_data["phraseCounter"]
            }
            
            df = pd.DataFrame(data_for_df)
            
            # If the file already exists, load the existing DataFrame and append the new data
            if os.path.exists(self.excel_path):
                with pd.ExcelWriter(self.excel_path, engine="openpyxl", mode="a", if_sheet_exists="overlay") as writer:
                    # Reads existing Excel file and DataFrame of specific worksheet
                    try:
                        existing_data_df = pd.read_excel(self.excel_path, sheet_name="News Data")
                        # Attach the new data
                        updated_df = pd.concat([existing_data_df, df], ignore_index=True)
                        # Saves the updated DataFrame to the file, replacing the existing worksheet
                        updated_df.to_excel(writer, sheet_name="News Data", index=False)
                    except ValueError:
                        # If the spreadsheet doesn't exist, just write the new data
                        df.to_excel(writer, sheet_name="News Data", index=False)
            else:
                #  If the file does not exist, create a new one and save the data
                with pd.ExcelWriter(self.excel_path, engine="openpyxl") as writer:
                    df.to_excel(writer, sheet_name="News Data", index=False)