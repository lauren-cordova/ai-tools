# This is a simple test page to validate OpenAI API integration.
# It makes a minimal API call to check accessand displays the response and token usage.
# It also shows any errors if the API call fails.
# To use this file, create an API key in OpenAI and add it to a secrets file.
# Then update the references below to match your API key name and path to the secrets file.
# Enjoy! - LC

import streamlit as st
import openai
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'secrets')) #REPLACE WITH YOUR PATH
import my_secrets #REPLACE WITH YOUR SECRETS FILE NAME
# print("Available attributes in secrets:", dir(my_secrets)) #HELPS WITH DEBUGGING

# Set page config
st.set_page_config(page_title="OpenAI API Test", layout="wide")
st.title("OpenAI API Integration Test")

# Initialize OpenAI client
api_key = my_secrets.openai_by #REPLACE WITH YOUR API KEY NAME IN SECRETS FILE
client = openai.OpenAI(api_key=api_key)

# Add a button to test the API
if st.button("Test OpenAI API"):
    with st.spinner("Testing API connection..."):
        try:
            # Make a minimal test call
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": "Say 'Hello'"}],
                max_tokens=1
            )
            
            # Display success message and response
            st.success("API connection successful!")
            st.write("Response:", response.choices[0].message.content)
            
            # Display token usage
            st.info(f"Tokens used: {response.usage.total_tokens}")
            
        except Exception as e:
            st.error(f"Error testing API: {str(e)}")

# Add some helpful information
with st.expander("About"):
    st.write("""
    This is a simple test page to validate OpenAI API integration.
    - Makes a minimal API call with 1 token
    - Displays the response and token usage
    - Shows any errors if the API call fails
    """)