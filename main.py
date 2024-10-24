import streamlit as st
from pyabsa.tasks.AspectTermExtraction.prediction.aspect_extractor import AspectExtractor as ATEPC
import os
from CheckpointLoader import download_model
from Examples import Examples


# load model
@st.cache_resource
def load_model(file_name):
    print('Loading model...')
    Model = ATEPC.AspectExtractor(file_name)
    return Model


# download model
file_name = download_model()
# load model
model = load_model(file_name)

# Title
st.title("Aspect Extraction")
# get text
option = None
text_input = None
custom = st.toggle("custom")
if not custom:
    option = st.selectbox(
        "Examples:",
        Examples,
    )
else:
    text_input = st.text_input("Input Text:",
                               help="ex: 'The restaurant had amazing food, but the service wasn't that great.'")
run = st.button('Predict')

if run:
    if not custom:
        output = model.predict(option)
    else:
        output = model.predict(text_input)
    tokens = output['tokens']
    aspects = output['aspect']
    positions = output['position']
    sentiments = output['sentiment']

    output_text = """
    <style>
    r { color: Red }
    o { color: Orange }
    g { color: Green }
    </style>
    
    """
    for i in range(len(positions)):
        position = positions[i]
        sentiment = sentiments[i]
        for id in position:
            if sentiment == 'Positive':
                tokens[id] = f"<g>{tokens[id]}</g>"
            if sentiment == 'Negative':
                tokens[id] = f"<r>{tokens[id]}</r>"
            if sentiment == 'Neutral':
                tokens[id] = f"<o>{tokens[id]}</o>"

    output_text += " ".join(tokens)
    # print(tokens[positions[0]])
    # return output
    st.subheader("Output:")
    st.markdown(output_text, unsafe_allow_html=True)
    st.subheader("Output details:")
    st.markdown(output, unsafe_allow_html=True)
