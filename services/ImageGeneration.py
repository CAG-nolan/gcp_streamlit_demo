""" 
This service will generate images based on the data that is fed to it. These images will be in three formats - these being:
1. An image of the food item in a consumer-ready package (i.e. pudding cup, frozen cup, etc.)
2. An image of the food item without a package, such that it appears to be a standalone food item.
3. An image of the packaging that the food can be in (such as a box of items or a bag of items).

Once these are created, they are served back to the frontend application to be displayed on the streamlit side.
"""
import json
import vertexai
from vertexai.preview.vision_models import ImageGenerationModel
from vertexai.preview.generative_models import GenerativeModel
import vertexai.preview.generative_models as generative_models
from string import Template

class ImageGeneration:
    vertexai.init(project="gcp-atcbld0004344", location="us-central1")
    PROJECT_ID = "gcp-atcbld0004344"
    MODEL = GenerativeModel("gemini-1.0-pro-001")
    PROMPT = """You are an innovative RD food scientist that needs to mass produce innovatively packaged or 
    flavored retail-ready food."""
    SOCIAL_TRENDS = """- 2023: The year of the Hot Pockets and Reheatable Food. """
    LIKES = """- crunchy"""
    DISLIKES = """- soggy"""
    FOOD_CATEGORIES = """
    - Breakfast Food
    """
    FOOD_FLAVORS = """
    - Sausage Egg Cheese
    - Peanut Butter and Grape Jelly
    """
    ADDITIONAL_TREND_DATA = """"""
    AGE_GROUP = """
    - {"ageGroup": "Adults Over 18", "preferredCookTime: [{"cookTime": "0-5", "percentage": ".35"}]}
    - {"ageGroup": "Children Under 18", "preferredCookTime: [{"cookTime": "0-5", "percentage": ".65"}]}
    """

    def generate(self, food_form: str, age_group: str = AGE_GROUP, food_flavors: str = FOOD_FLAVORS, likes: str = LIKES,
                 dislikes: str = DISLIKES, additional_trend_data: str = ADDITIONAL_TREND_DATA, social_trends: str = SOCIAL_TRENDS):
        # Categories and Food form will be hardcoded
        model = GenerativeModel("gemini-1.0-pro-001")
        prompt = f"""You are an innovative RD food scientist that needs to mass produce innovatively packaged or flavored retail-ready food.
            Generate 3 new products ideas based on the following:
            Food Form: {food_form}
            Customer Age Groups and preferred food cook times:
            {age_group}
            Categories:
            - Breakfast Food
            Food Attributes people like:
            {likes}
            Food Attributes people dislike:
            {dislikes}
            Popular Food Flavors:
            {food_flavors}
            Social Trends:
            {social_trends}
            Additional Information:
            {additional_trend_data}
        """
        prompt = Template(prompt).substitute(food_form=food_form, age_group=age_group, likes=likes, dislikes=dislikes,
                                             food_flavors=food_flavors, additional_trend_data=additional_trend_data,
                                             social_trends=social_trends)

        # Generate text responses
        responses = model.generate_content(prompt,
                                           generation_config={
                                               "max_output_tokens": 2048,
                                               "temperature": 0.9,
                                               "top_p": 1
                                           },
                                           safety_settings={
                                               generative_models.HarmCategory.HARM_CATEGORY_HATE_SPEECH: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
                                               generative_models.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
                                               generative_models.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
                                               generative_models.HarmCategory.HARM_CATEGORY_HARASSMENT: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
                                           },
                                           stream=True,
                                           )

        llm_response = ""

        # Print all responses
        for response in responses:
            llm_response += response.text

        return llm_response

    def generate_image_prompt(self, product):
        vertexai.init(project="gcp-atcbld0004344", location="us-central1")
        model = GenerativeModel("gemini-1.0-pro-001")
        response = model.generate_content(
            """You are an expert at creating image generation prompt for tools such as DALLE
            or Midjourney. You are given a description of a companies new food idea,
            and from that description you must generate a prompt for an image generation tool.
            The prompt should specify that the product is a consumer ready food, and it should be in the style of an advertisement.
            The description is: {}""".format(product),
            generation_config={
                "max_output_tokens": 1024,
                "temperature": 0.9,
                "top_p": 1
            },
            safety_settings={
                generative_models.HarmCategory.HARM_CATEGORY_HATE_SPEECH: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
                generative_models.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
                generative_models.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
                generative_models.HarmCategory.HARM_CATEGORY_HARASSMENT: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
            },
            stream=False,
        )

        return response.text

    def generate_image(
            output_file: str, prompt: str
    ) -> vertexai.preview.vision_models.ImageGenerationResponse:
        """Generate an image using a text prompt.
        Args:
          project_id: Google Cloud project ID, used to initialize Vertex AI.
          location: Google Cloud region, used to initialize Vertex AI.
          output_file: Local path to the output image file.
          prompt: The text prompt describing what you want to see."""

        model = ImageGenerationModel.from_pretrained("imagegeneration@005")

        images = model.generate_images(
            prompt=prompt,
            # Optional parameters
            seed=1,
            number_of_images=1,
        )

        images[0].save(location=output_file, include_generation_parameters=True)

        # Optional. View the generated image in a notebook.
        images[0].show()

        print(f"Created output image using {len(images[0]._image_bytes)} bytes")

        return images

    def show_images(self, output):
        for product in output:
            print(product['title'])
            image_prompt = self.generate_image_prompt(product['description'])
            print(f"Image Prompt: {image_prompt}")
            images = self.generate_image("{}.png".format(product['title']), "{}, 8k".format(image_prompt))
            images[0].show()

    def setup_output(self, age_group=AGE_GROUP, food_flavors=FOOD_FLAVORS, likes=LIKES, dislikes=DISLIKES,
                     additional_trend_data=ADDITIONAL_TREND_DATA, social_trends=SOCIAL_TRENDS):

        output = self.generate(food_form="Frozen Handhelds", age_group=age_group, food_flavors=food_flavors,
                               likes=likes, dislikes=dislikes, additional_trend_data=additional_trend_data,
                               social_trends=social_trends)
        print(output)

        output = json.loads(output)
