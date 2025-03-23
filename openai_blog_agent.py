# This is a simple tool to generate blog posts using GPT-3.5-turbo.
# To use this file, create an API key in OpenAI and add it to a secrets file.
# Then update the references below to match your API key name and path to the secrets file.
# If you are having trouble with the API key, please run OpenAI API Key.py to troubleshoot.
# Enjoy! - LC

# Import required packages
import streamlit as st
import os
import sys
from typing import Optional
import time
from openai import OpenAI

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'secrets')) #REPLACE WITH YOUR PATH
import my_secrets #REPLACE WITH YOUR SECRETS FILE NAME
# print("Available attributes in secrets:", dir(my_secrets)) #HELPS WITH DEBUGGING

# Setup OpenAI API
def setup_openai_api():
    try:
        api_key = my_secrets.openai_by #REPLACE WITH YOUR API KEY NAME IN SECRETS FILE
        return OpenAI(api_key=api_key)
    except Exception as e:
        st.error(f"Error setting up OpenAI API: {str(e)}")
        return None

def generate_blog_post(client: OpenAI, topic: str, max_retries: int = 3) -> Optional[str]:
    """
    Generate a blog post about the given topic using GPT-3.5-turbo
    
    Args:
        client: OpenAI client instance
        topic: The blog post topic
        max_retries: Maximum number of retries on API failure
    
    Returns:
        Generated blog post text or None if generation fails
    """
    if not topic.strip():
        st.error("Please enter a valid topic")
        return None
        
    system_prompt = """You are an expert blog writer. Write engaging, well-structured posts that include:
    1. A compelling headline
    2. An engaging introduction
    3. Well-organized main points with subheadings
    4. Relevant examples and evidence
    5. A strong conclusion
    
    Format the post with proper markdown for better readability."""
    
    for attempt in range(max_retries):
        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"Write a comprehensive blog post about {topic}."}
                ],
                temperature=0.7,
                max_tokens=2000,
                presence_penalty=0.6
            )
            return response.choices[0].message.content
            
        except Exception as e:
            if "Rate limit" in str(e) and attempt < max_retries - 1:
                time.sleep(20)  # Wait 20 seconds before retrying
                continue
            elif "Rate limit" in str(e):
                st.error("Rate limit exceeded. Please try again later.")
            elif "Authentication" in str(e):
                st.error("Authentication failed. Please check your API key.")
            else:
                st.error(f"Error generating blog post: {str(e)}")
            return None

def main():
    st.set_page_config(
        page_title="AI Blog Writing Assistant",
        page_icon="✍️",
        layout="wide"
    )
    
    st.title("✍️ AI Blog Writing Assistant")
    st.markdown("""
    Generate professional blog posts with the help of AI. 
    Enter a topic below and get a well-structured blog post in seconds!
    """)
    
    # Setup OpenAI API
    client = setup_openai_api()
    if not client:
        st.stop()
    
    # Create two columns for input
    col1, col2 = st.columns([3, 1])
    
    with col1:
        topic = st.text_input(
            "Enter your blog topic:",
            placeholder="e.g., The Future of AI in Business"
        )
    
    with col2:
        generate_button = st.button("Generate Blog Post", type="primary")
    
    if topic and generate_button:
        with st.spinner("Generating your blog post..."):
            blog_post = generate_blog_post(client, topic)
            
        if blog_post:
            st.success("Blog post generated successfully!")
            
            # Add copy button
            st.markdown("### Generated Blog Post")
            st.markdown(blog_post)
            
            # Download button
            st.download_button(
                label="Download Blog Post",
                data=blog_post,
                file_name=f"blog_post_{topic.lower().replace(' ', '_')}.md",
                mime="text/markdown"
            )
            
            # Display metadata
            st.sidebar.markdown("### Blog Post Details")
            st.sidebar.markdown(f"**Topic:** {topic}")
            st.sidebar.markdown(f"**Word Count:** {len(blog_post.split())}")
            st.sidebar.markdown(f"**Character Count:** {len(blog_post)}")

if __name__ == "__main__":
    main()