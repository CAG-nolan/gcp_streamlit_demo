import vertexai
from vertexai.preview.vision_models import ImageGenerationModel

vertexai.init(project="gcp-atcbld0004344", location="us-central1")

class GenImage:
    
    def __init__(self):
        self.model = ImageGenerationModel.from_pretrained("imagegeneration@005")
        
    def generate_image(self, prompt:str, save_image:bool=True):
        print(prompt)
        image = self.model.generate_images(
                prompt=prompt,
                number_of_images=1,
                negative_prompt="girl,anime,low quality,watermark,person,man,amature,bad quality"
            )
        if save_image:
            image[0].save(location=f"image.png")
        return image

