import os
import google.generativeai as genai
from dotenv import load_dotenv
load_dotenv()

# নিশ্চিত করুন যে API Key টি Environment Variable-এ সেট করা আছে
try:
    genai.configure(api_key=os.environ["GOOGLE_API_KEY"])
except ValueError:
    print("Error: GOOGLE_API_KEY is not set.")
    exit()

# অ্যাক্সেসযোগ্য মডেলগুলির তালিকা প্রিন্ট করুন
print("Available Models for your API Key:")
for model in genai.list_models():
    # শুধুমাত্র সেই মডেলগুলি দেখব যা টেক্সট তৈরি করতে পারে
    if 'generateContent' in model.supported_generation_methods:
        print(f"- {model.name}")