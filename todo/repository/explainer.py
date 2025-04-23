import os
import base64
from fastapi import HTTPException
from dotenv import load_dotenv
from google import genai
from google.genai import types
from PIL import Image
from io import BytesIO
import markdown
import json
from ..schemas import Explaination, GuidedExplanation, PromptRequest, Step


load_dotenv()


GENAI_API_KEY = os.getenv("GENAI_API_KEY")
client = genai.Client(api_key=GENAI_API_KEY)


def generate_steps(request):
    """
    Generates guided explanation steps from a prompt using Gemini API.
    """
    # steps = [Step(id=1, title='Step 1', description='hello', imageUrl='https://media.istockphoto.com/id/505221662/photo/elephants-in-river.jpg?s=1024x1024&w=is&k=20&c=6H1PzDPfOlCwJQZ8XSUQlkNKBgILDmig7RVqD9utJEY=', order=1)] # corrected, steps needs to be a list.
    # return GuidedExplanation(steps=steps)
    topic = request.prompt
    print(topic)
    # prompt = """Create a step-by-step guided explanation based on the following: {topic}. Each step should have a title, description, and an order. Return the answer as a JSON array of objects. Do not include any text outside the JSON. Example of a step object: {{'title': 'Step 1', 'description': 'Do this...', 'order': 1}}. If an image url is needed, include it as 'imageUrl' key. If there are no images needed, leave the 'imageUrl' key as an empty string."""
    
    prompt = f"""
        You are an expert at creating step-by-step guided explanations, and creating SVG code for {topic}.

        Based on the following topic: {topic}, generate a structured JSON array of objects, where each object represents a step in the explanation.

        Each step object must have the following keys:

        * "id" (integer): A unique numerical identifier for the step, starting from 1.
        * "title" (string): A concise title for the step.
        * "description" (string): A detailed description of the step.
        * "svg_code" (string): A valid, simple inline SVG code snippet relevant to the step. If no SVG is needed, provide an empty string ("").
        * "order" (integer): The sequential order of the step, starting from 1.

        The JSON array must be formatted strictly as follows, with no additional text or formatting outside the JSON:

        [
          {{
            "id": 1,
            "title": "...",
            "description": "...",
            "svg_code": "<svg>...</svg>",
            "order": 1
          }},
          {{
            "id": 2,
            "title": "...",
            "description": "...",
            "svg_code": "<svg>...</svg>",
            "order": 2
          }},
          ...
        ]

        Provide only the JSON.
        """
    response = client.models.generate_content(
        model='gemini-2.0-flash',
        contents=prompt,
        config={
            'response_mime_type': 'application/json',
            'response_schema': GuidedExplanation,
            },
        )
    
    steps_data = json.loads(response.text)
    print(steps_data['steps'])
    steps = [Step(**step) for step in steps_data['steps']]
    print(GuidedExplanation(steps=steps))
    return steps_data

    # try:
    #     # response = client.generate_content(model='gemini-2.0-flash', contents = prompt)
    #     response = client.models.generate_content(
    #         model='gemini-2.0-flash',
    #         contents=prompt,
    #         config={
    #             'response_mime_type': 'application/json',
    #             'response_schema': GuidedExplanation,
    #         },
    #     )
    #     content = response.text

        # Basic JSON parsing (you might need more robust error handling)
    #     import json

    #     try:
    #         steps_data = json.loads(content)
    #         if not isinstance(steps_data, list):
    #             raise ValueError("Gemini API did not return a JSON array.")

    #         steps = [Step(**step) for step in steps_data]
    #         print(steps)
    #         steps.sort(key=lambda x: x.order) # Sort steps by order.
    #         return GuidedExplanation(steps=steps)

    #     except json.JSONDecodeError:
    #         raise HTTPException(status_code=500, detail="Gemini API returned invalid JSON.")
    #     except ValueError as e:
    #         raise HTTPException(status_code=500, detail=str(e))
    #     except TypeError as e:
    #         raise HTTPException(status_code=500, detail=f"Type error during step creation: {e}, Content: {content}")
    #     except Exception as e:
    #         raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {e}, Content: {content}")

    # except Exception as e:
    #     raise HTTPException(status_code=500, detail=f"Error generating steps: {e}")


def explain(request):
    prompt = f"""
    Create an educational lesson about {request.topic} for 12th students.

    The lesson should include:
    - A clear and concise explanation of the topic.
    - A html iframe or imageor gif of simple simulation or interactive activity from phET or similer resources.
    - A list of relevant resources (websites, videos, books).
    """
    # prompt = f"""
    # Create an educational lesson about {request.topic} for 12th students.

    # The lesson should include:
    # - A clear and concise explanation of the topic.
    # - An idea for a simple simulation or interactive activity.
    # - A list of relevant resources (websites, videos, books).
    # - A description of a simple image that would visually represent the topic.

    # Structure the output as a JSON object with the following keys:
    # {{
    #     "explanation": "...",
    #     "simulation_idea": "...",
    #     "resources": ["...", "..."],
    #     "image_description": "..."
    # }}
    # """
    # response = client.models.generate_content(
    #     model="gemini-2.0-flash", contents=prompt,
    #     config={
    #     'response_mime_type': 'application/json',
    #     'response_schema': list[Recipe],
    # },
    #     )
    response = client.models.generate_content(
    model='gemini-2.0-flash',
    contents=prompt,
    config={
        'response_mime_type': 'application/json',
        'response_schema': Explaination,
    },
)
    content = json.loads(response.text)
    # res = {
    #    "topic": markdown.markdown(content['topic']),
    #    "explaination": markdown.markdown(content['explaination']),
    #    "simulation": markdown.markdown(content['simulation']),
    #    "resources": markdown.markdown(content['resources']),
    # }
    return {
       "explaination": markdown.markdown(content['explaination']),
       "simulation": markdown.markdown(content['simulation']),
    #    "resources": markdown.markdown(content['resources']),
       }


def imagine(request):
   response = client.models.generate_images(
      model='imagen-3.0-generate-002',
      prompt=request.topic,
      config=types.GenerateImagesConfig(
         number_of_images= 1,
        )
    )
   
   for generated_image in response.generated_images:
      image = Image.open(BytesIO(generated_image.image.image_bytes))
      buffered = BytesIO()
      image.save(buffered, format="PNG")
      img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
      print(img_str)
      return {"image": img_str}