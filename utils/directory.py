import os 
import config

class directory:
    def __init__(self, query):
        self.query = query.replace(" ", "_")
        self.file_path = os.path.join(config.path, self.query)
        self.images_path = f"{self.file_path}/images/"

    # Creating Directory if it already doesn't exist 
    def create_directory(self):
        directory_path = os.path.dirname(self.images_path)
        if not os.path.exists(directory_path):
            os.makedirs(directory_path)

        print(f"Artifacts directory: {directory_path.absolute()}")

        # Verifica se o diretório existe e cria se não existir.
        if not directory_path.exists():
            print(f"Directory {directory_path.absolute()} does not exist. Creating it.")
            directory_path.mkdir(parents=True, exist_ok=True)

