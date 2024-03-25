import os
import urllib.request

class downloads:
    def download_image(image_url, save_path):
        # Create the path if doesnt exists
        os.makedirs(os.path.dirname(save_path), exist_ok=True)

        # Using urllib.request.urlretrieve to download the image and save in the specified path
        urllib.request.urlretrieve(image_url, save_path)
        print(f"Imagem baixada com sucesso em: {save_path}")