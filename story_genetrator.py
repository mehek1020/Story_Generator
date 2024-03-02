import streamlit as st
from openai import OpenAI

# Set the OpenAI API key
openai_api_key = 'Your Openai key'
client = OpenAI(api_key=openai_api_key)

def generate_story_and_images(prompt, text_model='gpt-3.5-turbo', image_model='dall-e-2'):
    # Truncate or reduce the length of the prompt if needed
    prompt = prompt[:500]  # Adjust the length as needed

    # Generate story using text model
    response_text = client.chat.completions.create(
        model=text_model,
        temperature=0,
        messages=[
            {"role": "system", "content": "You only generate stories based on the prompt provided."},
            {"role": "user", "content": prompt}
        ]
    )
    story = response_text.choices[0].message.content

    # Generate images related to the story using DALL-E model
    response_image = client.images.generate(
        model=image_model,
        prompt=f"{"Generate an photorealistic, anime and detailed image for "} {prompt}",  # Combine user input and generated story as a prompt
        size="1024x1024",
        quality="hd",
        n=1,
    )
    image_url = response_image.data[0].url

    return [(story, image_url)]  # Return a list with one tuple

# Streamlit app
st.title('Story Generator with Image')

# User input
prompt = st.text_input('Enter a prompt for your story:')

def capitalize_first_letter(input_string):
    if not input_string:
        return input_string
    result_string = input_string[0].capitalize() + input_string[1:]
    return result_string 

# Generate button
if st.button('Generate Story and Image'):
    with st.spinner('Generating...'):
        generated_results = generate_story_and_images(prompt)

        # Display the generated stories and images
        for story, image_url in generated_results:
            st.write(story)
            st.subheader("Generated Image:")
            st.image(image_url, caption=capitalize_first_letter(prompt), use_column_width=True)