from flask import Flask, jsonify, request
from layers.GenPrompt import GenPrompt
from layers.GenImage import GenImage
from vertexai.preview.vision_models import ImageGenerationResponse

app = Flask("ImageAPI")

@app.route("/api/prompt/generate", methods=['POST'])
def generate_product():
    """ Generate a prompt for the image generation service. """
    prompt_tooling = GenPrompt()
    if request.is_json:
        data = request.json
        # Process JSON data
        trends = data.get('trends')
        likes = data.get('likes')
        dislikes = data.get('dislikes')
        categories = data.get('categories')
        flavors = data.get('flavors')
        additional = data.get('additional')
        age = data.get('age')
        # Do something with the data
        product: dict = prompt_tooling.get_product(
            form='handheld',
            age=age,
            flavors=flavors,
            likes=likes,
            dislikes=dislikes,
            additional=additional,
            trends=trends
        )
        
        return jsonify(product)
        
@app.route("/api/prompt/chat", methods=['POST'])
def chat():
    """ Generate a prompt for the image generation service. """
    prompt_tooling = GenPrompt()
    if request.is_json:
        data = request.json
        # Process JSON data
        prompt = data.get('prompt')
        # Do something with the data
        response: dict = prompt_tooling.chat(
            prompt=f"{prompt}",
        )
        
        return response
        
    return {}

@app.route("/api/image/generate",  methods=['POST'])
def generate_image():
    """ Generate an image using a prompt provided by the user. This image is returned in
        a base64 format which can easily be displayed in any frontend application.
    
    args:
        request Request: HTTPRequest to the API.
        prompt String: The prompt used to generate the image.

    returns:
        image base64: The base64 image that was generated
    """

    prompt_tooling = GenPrompt()
    image_creator = GenImage()

    if request.is_json:
        data = request.json
        # Process JSON data
        title = data.get('title')
        description = data.get('description')
        additional = data.get('additional')
        prompt = f"{title} {additional}"
        
        # Do something with the data
        product: ImageGenerationResponse = image_creator.generate_image(
            prompt=prompt_tooling.get_image_prompt(prompt)
        )
        base = product.images[0]._as_base64_string()
        response = {"image": f"data:image/png;base64,{base}"}
        
        return jsonify(response)
    
    return {}

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=6969)