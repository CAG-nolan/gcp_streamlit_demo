import json
import re
import vertexai
from vertexai.preview.generative_models import GenerativeModel
import vertexai.preview.generative_models as generative_models

MODEL_SAFETY_SETTINGS = {
    generative_models.HarmCategory.HARM_CATEGORY_HATE_SPEECH: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
    generative_models.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
    generative_models.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
    generative_models.HarmCategory.HARM_CATEGORY_HARASSMENT: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE
    }

class GenPrompt:
    vertexai.init(project="gcp-atcbld0004344", location="us-central1") 
    def __init__(self):
        self.model = GenerativeModel("gemini-1.0-pro-001")
        self.generation_configuration: dict = {
                    "max_output_tokens": 512,
                    "temperature": 0.95,
                    "top_p": 1
                }


    def __fortify_image_prompt(self, prompt:str):
        fortified_prompter:str = f"You are an expert at making prompts for image generation tools such as DALLE and Midjourney. Never include people in the prompt. You must generate a description that will be used as a prompt for a similar image prompting service. You must align with the prompt themes, and you must always generate prompts that emphasize that the products are for a consumer food brand. The prompt must specify that the image is in the style of an advertisement photograph. Your prompt should always strive to produce the most realistic photos possible. You must always emphasize the positive attributes of the prompt, and use accurate descriptors in your response. YOU MUST ALWAYS RESPOND WITH A 2 or 3 SENTENCE IMAGE PROMPT!!! Given this information, create a prompt using the following description:\n{prompt}"
        fortified_response = self.model.generate_content(fortified_prompter, generation_config=self.generation_configuration, safety_settings=MODEL_SAFETY_SETTINGS, stream=False)
        print(fortified_response)
        return fortified_response.text       
         

    def get_image_prompt(self, product: str):
        self.generation_configuration: dict = {
                    "max_output_tokens": 5000,
                    "temperature": 0.45,
                    "top_p": 1
                }
        response = self.model.generate_content(
                    self.__fortify_image_prompt(product),
                    generation_config=self.generation_configuration,
                    safety_settings=MODEL_SAFETY_SETTINGS,
                    stream=False
                )
        return response.text

    def __validate(self, string:str):
        string = string.replace("```", "").replace("JSON", "").replace("json", "").replace("'", '"')
        print(string)
        if x:= re.search(r'\[(.*?)\]', string, re.DOTALL):
            return x.group(0)
        else:
            return string


    def get_product(self, form: str = "", age: str = "", flavors: str = "", likes: str = "",
                    dislikes: str = "", additional: str = "", trends: str = ""):
        
        prompt = f"You are a food design expert researcher who excels at creating new food products based on the current trends and data given to you. You are innovative, and you must create mass producable and retail-ready consumer food. You love to create products for companies that have a dominate place in the grocery store, and your primary focus is that food is innovative and easy to package and sell in high quantities.\n Based on the above criteria, produce an innovative food idea given the current information: Food Form: {form}\nCustomer Age Groups and preferred food cook times:{age}\nFood Attributes people like:{likes}\nFood Attributes people dislike:{dislikes}\nPopular Food Flavors:{flavors}\nSocial Trends:{trends}\nAdditional Information:{additional}.\n"

        prompt += "Produce a JSON output in the following format:\n{'title': '<the title of the new food>', 'reasoning': '<the reason why the food should go to market based on current trends>', 'description': '<a description of the new food idea'>}\nGiven this, generate a new food idea, ensuring that it is returned in the format specified above."

        self.generation_configuration: dict = {
                    "max_output_tokens": 5000,
                    "temperature": 0.90,
                    "top_p": 1
                }

        product = self.model.generate_content(
                    prompt,
                    generation_config=self.generation_configuration,
                    safety_settings=MODEL_SAFETY_SETTINGS,
                    stream=False
                )
 
        return json.loads(self.__validate(product.text))
    
    def chat(self, prompt: str):
        self.generation_configuration: dict = {
                    "max_output_tokens": 5000,
                    "temperature": 0.95,
                    "top_p": 1
                }
        response = self.model.generate_content(
                    prompt,
                    generation_config=self.generation_configuration,
                    safety_settings=MODEL_SAFETY_SETTINGS,
                    stream=False
                )
 
        return response.text