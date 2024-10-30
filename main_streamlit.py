import streamlit as st
from analyze_news import analyse_news

st.set_page_config(page_title="Fake News Detection", layout="wide")
st.markdown("""
    <style>
        .header {
            font-size: 36px;
            font-weight: bold;
            text-align: center;
            color: #4c8bf5;
            margin-bottom: 0;
        }
        .subheader {
            font-size: 20px;
            text-align: center;
            margin-bottom: 40px;
            color: #888;
        }
        .center {
            display: flex;
            justify-content: center;
        }
        .input-box {
            width: 100%;
            max-width: 500px;
            padding: 10px;
            margin-bottom: 20px;
        }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1 class='header'>Fake News Detection</h1>", unsafe_allow_html=True)
st.markdown("<p class='subheader'>Using AI to detect fake news from headlines and articles</p>", unsafe_allow_html=True)
query = st.text_area("", height=200, placeholder="Enter News headline or Article")


if st.button("Check Veracity"):
    if query:
        result = analyse_news(query)
        st.markdown(f"""
            <div style='text-align: center; margin: 40px;'>
                <h3>{result}</h3>
            </div>
        """, unsafe_allow_html=True)
    else:
        st.warning("Please enter a news headline or article to analyze.")



