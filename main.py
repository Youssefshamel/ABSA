import streamlit as st
from pyabsa import AspectTermExtraction as ATEPC
import os
from CheckpointLoader import download_model


# load model
@st.cache_resource
def load_model():
    Model = ATEPC.AspectExtractor("fast_lcf_atepc_my_dataset_cdw_apcacc_83.5_apcf1_78.89_atef1_64.24")
    return Model

# download model
download_model()
# load model
model = load_model()

# Title
st.title("Aspect Extraction")
# get text
text_input = st.text_input("input text:", help="ex: 'The restaurant had amazing food, but the service wasn't that great.'")
run = st.button('Predict')
if run:
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

