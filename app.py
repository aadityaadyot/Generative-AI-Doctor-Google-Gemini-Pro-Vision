from dotenv import load_dotenv
load_dotenv()
import streamlit as st
import os
import google.generativeai as genai
from PIL import Image

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

## Function to load Gemini pro model and get response

model= genai.GenerativeModel("gemini-pro-vision")
def get_gemini_response(input, image, prompt):
    response = model.generate_content([input,image[0], prompt])
    return response.text

def input_image_setup(uploaded_file):
    # Check if a file has been uploaded
    if uploaded_file is not None:
        # Read the file into bytes
        bytes_data = uploaded_file.getvalue()

        image_parts = [
            {
                "mime_type": uploaded_file.type,  # Get the mime type of the uploaded file
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")
    
##initialize our streamlit app

st.set_page_config(page_title="Gemini Image Demo")

st.header("Gemini Application")
input=st.text_input("Input Prompt: ",key="input")
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
image=""   
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image.", use_column_width=True)


submit=st.button("Tell me about calories in the image")

input_prompt = """
               You are a nutritionist developing an innovative tool to assist individuals in tracking their calorie intake. Your goal is to create a system that can analyze images of various dishes or drinks and accurately estimate the calorie content of each component separately. The output should be presented in a particular format for easy understanding.

Your task is to write a program or algorithm that takes an image of a dish or drink as input and outputs the estimated calorie content of each food item or ingredient separately, in a structured format.

Here's an example format for the output:

---

**Estimated Calorie Content:**

- **Dish/Drink Name:**
  - **Ingredient 1:** [Calories]
  - **Ingredient 2:** [Calories]
  - **Ingredient 3:** [Calories]
  ...
  - **Total Calories:** [Total Calories]

---

Your solution should utilize advanced image processing techniques and machine learning models to accurately identify and analyze different food items or ingredients in the image. Additionally, it should consider portion sizes and variations in recipes to provide more precise calorie estimates.

Remember to optimize the program for both accuracy and efficiency to ensure real-time performance.

"""

## If ask button is clicked

if submit:
    image_data = input_image_setup(uploaded_file)
    response=get_gemini_response(input_prompt,image_data,input)
    st.subheader("The Response is")
    st.write(response)



