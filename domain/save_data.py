import pandas as pd
import os

class save:
    def __init__(self, excel_path):
        self.excel_path = excel_path
        
    def save_to_xlsx(self, data):
            print('Saving to xlsx...')
            # Define o texto base do link indesejado para a verificação
            undesired_links_texts = [
                                    "https://www.nytimes.com/search?dropmab=false",
                                    "https://www.nytimes.com/topic/"
            ]        
            # Verifica se algum link na lista contém o texto base
            if any(any(base_text in link for base_text in undesired_links_texts) for link in data["newsData"]["links"]):
                print("Encontrado link com texto base indesejado, registro ignorado.")
                return
            
            # separar função
            
            # Desempacota os dados
            news_data = data["newsData"]
            image_urls = data["imageUrls"]
            
            # Seleciona o segundo parágrafo de "paragraphs", conforme especificado
            selected_paragraph = news_data["paragraphs"][1] if len(news_data["paragraphs"]) > 1 else None
            
            # Preparando os dados para DataFrame
            data_for_df = {
                "headings": [news_data["headings"][0]] if news_data["headings"] else [None],
                "date": [news_data["date"][0]] if news_data["date"] else [None],
                "paragraphs": [selected_paragraph],
                "links": [news_data["links"][0]] if news_data["links"] else [None],
                "image_urls": [image_urls[0]] if image_urls else "No image available",
                "imagefile_path":news_data["savePath"]
            }
            
            df = pd.DataFrame(data_for_df)
            
            # Se o arquivo já existe, carrega o DataFrame existente e anexa os novos dados
            if os.path.exists(self.excel_path):
                with pd.ExcelWriter(self.excel_path, engine="openpyxl", mode="a", if_sheet_exists="overlay") as writer:
                    # Lê o arquivo Excel existente e o DataFrame da planilha específica
                    try:
                        existing_data_df = pd.read_excel(self.excel_path, sheet_name="News Data")
                        # Anexa os novos dados
                        updated_df = pd.concat([existing_data_df, df], ignore_index=True)
                        # Salva o DataFrame atualizado no arquivo, substituindo a planilha existente
                        updated_df.to_excel(writer, sheet_name="News Data", index=False)
                    except ValueError:
                        # Se a planilha não existir, apenas escreve os novos dados
                        df.to_excel(writer, sheet_name="News Data", index=False)
            else:
                # Se o arquivo não existe, cria um novo e salva os dados
                with pd.ExcelWriter(self.excel_path, engine="openpyxl") as writer:
                    df.to_excel(writer, sheet_name="News Data", index=False)