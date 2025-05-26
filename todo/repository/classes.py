import json
import os
import markdown
from dotenv import load_dotenv
from google import genai
from google.genai import types
from ..supabase_client import supabase
from ..schemas import Explaination, GuidedExplanation, PromptRequest, Step


load_dotenv()

GENAI_API_KEY = os.getenv("GENAI_API_KEY")
client = genai.Client(api_key=GENAI_API_KEY)


def create(data):
    # prompt = f"Write lecture notes and transcript to teach students who is preparing for {data.exam} exam, {data.subject}, {data.topic}. and also suject best resources. like a human teacher."
    # response = client.models.generate_content(
    #     model = 'gemini-2.0-flash',
    #     contents=prompt,
    #     config = {
    #         'response_mime_type': 'application/json',
    #         'response_schema': GuidedExplanation,
    #     }
    # )
    # steps_data = json.loads(response.text)
    # print(steps_data['steps'])
    # steps = [Step(**step) for step in steps_data['steps']]
    # print(GuidedExplanation(steps=steps))
    # print(response.topic)
    # print(response.content)
    # print(response)
    created_class = (
        supabase.table("classes")
        .insert({"exam": data.exam, "subject": data.subject, "topic": data.topic, "user": data.email, "progress": data.progress_percentage})
        .execute()
    )
    return created_class
    # return data.json()
    # content = json.loads(created_class.text)
    # print(content)
    # return {
    #    "content": markdown.markdown(content['content']),
    #    "explaination": markdown.markdown(content['explaination']),
    #    }
    # return True


def get_all(email):
    classes = (
        supabase.table("classes")
        .select("*").eq("user", email)
        .execute()
    )
    print(classes)
    return classes.data

def get_class(email, id):
    print(email, id)
    response = (
        supabase.table("course")
        .select("*").eq("user", email).eq("id", id)
        .execute()
    )
    return response.json()