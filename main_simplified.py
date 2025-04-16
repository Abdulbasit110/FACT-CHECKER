import streamlit as st
import speech_recognition as sr
import asyncio
from groq import AsyncGroq
from dotenv import load_dotenv
import os
import traceback
from web_search import EfficientWebSearch
from fact_checking import fact_check_with_groq, parse_fact_check_result
import plotly.graph_objs as go
import spacy
from utils import GROQ_API_KEY, SPACY_MODEL, sentiment_to_percentage, get_verification_counts
from context_builder import EnhancedContextBuilder

# Load environment variables
load_dotenv()

# Initialize components
groq_client = AsyncGroq(api_key=GROQ_API_KEY)
r = sr.Recognizer()
web_searcher = EfficientWebSearch()

# Initialize NLP models
try:
    nlp = spacy.load(SPACY_MODEL)
except:
    st.warning("Could not load spaCy model. Using simplified mode.")
    nlp = None

# Initialize context builder
context_builder = EnhancedContextBuilder()

# Streamlit page configuration
st.set_page_config(page_title="AI-Powered Fact-Checker", page_icon="🎙️", layout="wide")
st.title("AI-Powered Fact-Checker")
st.caption("This is a simplified version without speaker diarization")

# Initialize session state variables
if 'transcribed_text' not in st.session_state:
    st.session_state.transcribed_text = ""
if 'claims' not in st.session_state:
    st.session_state.claims = []
if 'fact_checks' not in st.session_state:
    st.session_state.fact_checks = []

async def transcribe_audio(audio_file):
    try:
        with sr.AudioFile(audio_file) as source:
            audio_data = r.record(source)
        text = r.recognize_google(audio_data)
        return text
    except Exception as e:
        st.error(f"Error transcribing audio: {str(e)}")
        return ""

async def extract_claims(text):
    prompt = f"""
    Given the following transcribed text, extract all clear and concise claims that can be fact-checked.
    Each claim should be a single sentence and should be something that can be verified.
    Do not include any additional commentary or notes about the claims.
    Format the output as a simple numbered list, with each claim on a new line.

    Transcribed text:
    {text}
    """
    
    try:
        response = await groq_client.chat.completions.create(
            messages=[
                {"role": "system", "content": "You are an AI assistant that extracts clear, concise, and fact-checkable claims from text."},
                {"role": "user", "content": prompt}
            ],
            model="llama-3.1-8b-instant",
            temperature=0.1,
            max_tokens=500,
            top_p=1,
        )
        claims = response.choices[0].message.content.split("\n")
        return [claim.strip().lstrip("0123456789. ") for claim in claims if claim.strip()]
    except Exception as e:
        st.error(f"Error extracting claims: {str(e)}")
        return []

async def categorize_claim(claim):
    if nlp:
        doc = nlp(claim)
        categories = [ent.label_ for ent in doc.ents]
        return list(set(categories))
    return []

# Simple sentiment analysis function
def analyze_sentiment(text):
    # Simple positive/negative word detection as fallback
    positive_words = ["good", "great", "excellent", "positive", "true", "correct", "fact", "proven"]
    negative_words = ["bad", "wrong", "false", "incorrect", "lie", "misleading", "fake"]
    
    text_lower = text.lower()
    positive_count = sum(1 for word in positive_words if word in text_lower)
    negative_count = sum(1 for word in negative_words if word in text_lower)
    
    if positive_count == negative_count:
        return 0
    return (positive_count - negative_count) / max(positive_count + negative_count, 1)

async def fact_check_claim(claim, web_results, context):
    categories = await categorize_claim(claim)
    sentiment = analyze_sentiment(claim)
    
    result = await fact_check_with_groq(groq_client, claim, context, web_results, categories, sentiment, None)
    parsed_result = parse_fact_check_result(result)
    
    parsed_result['Categories'] = categories
    parsed_result['Sentiment'] = sentiment
    return parsed_result

async def process_claims(claims, context):
    fact_checks = []
    
    try:
        for i, claim in enumerate(claims):
            st.write(f"Processing claim {i+1}/{len(claims)}: {claim}")
            web_results = await web_searcher.search(claim)
            context = context_builder.get_relevant_context(claim)
            result = await fact_check_claim(claim, web_results, context)
            
            # Use "Unknown" as the default speaker
            speaker = "Unknown"
            
            context_builder.add_statement(claim, speaker)
            fact_checks.append((claim, result, speaker))
    except Exception as e:
        st.error(f"Error processing claims: {str(e)}")
        st.error(f"Traceback: {traceback.format_exc()}")
    return fact_checks

async def main():
    st.markdown("## 🎯 AI-Powered Fact-Checker")
    st.caption("Verify claims from audio or text in real-time using AI + Web Search")

    with st.sidebar:
        st.header("⚙️ Settings")
        st.markdown("Customize fact-checking behavior below.")
        sentiment_display = st.checkbox("Show Sentiment Meter", value=True)

    tab1, tab2, tab3 = st.tabs(["🔊 Input", "📋 Claims", "✅ Fact Check Results"])

    with tab1:
        st.subheader("📥 Upload Audio or Enter Text")
        text_input = st.text_area("Or paste your text here:", height=150)

        uploaded_file = st.file_uploader("Upload a WAV audio file", type="wav")
        if uploaded_file is not None:
            st.audio(uploaded_file, format='audio/wav')

        if st.button("🔍 Analyze Now"):
            with st.spinner("Transcribing and extracting claims..."):
                if uploaded_file:
                    st.session_state.transcribed_text = await transcribe_audio(uploaded_file)
                    st.success("✅ Audio transcribed successfully!")
                elif text_input:
                    st.session_state.transcribed_text = text_input
                else:
                    st.error("❗ Please upload audio or enter some text.")
                    return

                if st.session_state.transcribed_text:
                    st.session_state.claims = await extract_claims(st.session_state.transcribed_text)
                    st.session_state.fact_checks = await process_claims(st.session_state.claims, st.session_state.transcribed_text)
                    st.success("🎉 Fact-checking complete!")

    with tab2:
        if st.session_state.transcribed_text:
            st.subheader("📝 Transcribed Text")
            st.text_area("Transcribed Text", st.session_state.transcribed_text, height=150)

        if st.session_state.claims:
            st.subheader("📋 Extracted Claims")
            for idx, claim in enumerate(st.session_state.claims):
                st.markdown(f"**{idx+1}.** {claim}")

    with tab3:
        if st.session_state.fact_checks:
            st.subheader("✅ Fact Check Results")
            for i, (claim, result, speaker) in enumerate(st.session_state.fact_checks):
                with st.expander(f"Claim {i+1}: {claim}", expanded=True):
                    verification = result.get("Verification", "N/A")
                    confidence = result.get("Confidence", "N/A")
                    explanation = result.get("Explanation", "N/A")
                    bias = result.get("Bias", "N/A")
                    sources = result.get("Sources", "N/A")
                    categories = result.get("Categories", [])
                    sentiment = result.get("Sentiment", 0)

                    color_icon = ":green_circle:" if verification == "Verified" else ":orange_circle:" if verification == "Partially Verified" else ":red_circle:"
                    st.markdown(f"**Verification:** {color_icon} {verification}")
                    st.markdown(f"**Confidence:** `{confidence}`")
                    st.markdown(f"**Explanation:** {explanation}")
                    st.markdown(f"**Potential Bias:** `{bias}`")
                    st.markdown(f"**Sources:** {sources}")
                    if categories:
                        st.markdown(f"**Categories:** `{', '.join(categories)}`")

                    if sentiment_display:
                        st.markdown("#### 🧠 Sentiment-Based Truth Meter")
                        fig = go.Figure(go.Indicator(
                            mode="gauge+number",
                            value=sentiment_to_percentage(sentiment),
                            title={'text': "Truth Meter"},
                            gauge={
                                'axis': {'range': [0, 100]},
                                'bar': {'color': "green" if sentiment > 0.6 else "orange" if sentiment > 0.3 else "red"},
                                'steps': [
                                    {'range': [0, 33], 'color': "lightgray"},
                                    {'range': [33, 66], 'color': "gray"},
                                    {'range': [66, 100], 'color': "darkgray"},
                                ],
                                'threshold': {
                                    'line': {'color': "red", 'width': 4},
                                    'thickness': 0.75,
                                    'value': 50
                                }
                            }
                        ))
                        st.plotly_chart(fig, key=f"truth_meter_{i}0")

            # Overall stats
            st.markdown("---")
            st.subheader("📊 Summary Statistics")
            verified_count, partially_verified_count, not_verified_count = get_verification_counts(st.session_state.fact_checks)
            st.markdown("**Verification Breakdown**")
            fig = go.Figure(data=[
                go.Pie(labels=['Verified', 'Partially Verified', 'Not Verified'],
                       values=[verified_count, partially_verified_count, not_verified_count],
                       marker=dict(colors=["#28a745", "#ffc107", "#dc3545"]))
            ])
            st.plotly_chart(fig, key="verification_stats_pie1")

            st.subheader("🔍 Detected Topics")
            current_topics = context_builder.get_current_topics()
            if current_topics:
                st.markdown(f"**Topics:** `{', '.join(current_topics)}`")
            else:
                st.info("No topics detected yet.")


    # st.header("1. Upload Audio or Enter Text")
    
    # # Text input option
    # text_input = st.text_area("Or enter text directly:", height=150)
    
    # # Audio upload option
    # uploaded_file = st.file_uploader("Choose a WAV file", type="wav")
    # if uploaded_file is not None:
    #     st.audio(uploaded_file, format='audio/wav')
    
    # if st.button("Process"):
    #     with st.spinner("Processing..."):
    #         # Determine the source of text
    #         if uploaded_file is not None:
    #             st.session_state.transcribed_text = await transcribe_audio(uploaded_file)
    #             st.write("Audio transcribed successfully!")
    #         elif text_input:
    #             st.session_state.transcribed_text = text_input
            
    #         if st.session_state.transcribed_text:
    #             st.session_state.claims = await extract_claims(st.session_state.transcribed_text)
    #             st.session_state.fact_checks = await process_claims(st.session_state.claims, st.session_state.transcribed_text)
    #             st.success("Analysis complete!")
    #         else:
    #             st.error("No text to analyze. Please upload an audio file or enter text.")

    if st.session_state.transcribed_text:
        st.header("2. Transcribed Text and Claims")
        st.text_area("Text", st.session_state.transcribed_text, height=150)
        st.write("Extracted claims:", st.session_state.claims)

    if st.session_state.fact_checks:
        st.header("3. Fact-Check Results")
        for i, (claim, result, speaker) in enumerate(st.session_state.fact_checks):
            with st.expander(f"Claim {i+1}: {claim}", expanded=True):
                verification = result.get("Verification", "N/A")
                confidence = result.get("Confidence", "N/A")
                explanation = result.get("Explanation", "N/A")
                bias = result.get("Bias", "N/A")
                sources = result.get("Sources", "N/A")
                categories = result.get("Categories", [])
                sentiment = result.get("Sentiment", 0)

                st.write(f"**Verification:** {verification}")
                st.write(f"**Confidence:** {confidence}")
                st.write(f"**Explanation:** {explanation}")
                st.write(f"**Potential Bias:** {bias}")
                st.write(f"**Sources:** {sources}")
                if categories:
                    st.write(f"**Categories:** {', '.join(categories)}")
                
                # Truth meter visualization
                fig = go.Figure(go.Indicator(
                    mode = "gauge+number",
                    value = sentiment_to_percentage(sentiment),
                    title = {'text': "Truth Meter"},
                    gauge = {'axis': {'range': [0, 100]},
                            'bar': {'color': "darkblue"},
                            'steps' : [
                                {'range': [0, 33], 'color': "lightgray"},
                                {'range': [33, 66], 'color': "gray"},
                                {'range': [66, 100], 'color': "darkgray"}],
                            'threshold': {
                                'line': {'color': "red", 'width': 4},
                                'thickness': 0.75,
                                'value': 50}}))
                st.plotly_chart(fig, key=f"truth_meter_{i}1")

        # Overall statistics
        st.header("4. Overall Statistics")
        verified_count, partially_verified_count, not_verified_count = get_verification_counts(st.session_state.fact_checks)
        
        fig = go.Figure(data=[go.Pie(labels=['Verified', 'Partially Verified', 'Not Verified'], 
                                    values=[verified_count, partially_verified_count, not_verified_count])])
        st.plotly_chart(fig, key="verification_stats_pie2")

        # Display current topics
        st.header("5. Current Topics")
        current_topics = context_builder.get_current_topics()
        st.write("Current topics:", ", ".join(current_topics))

if __name__ == "__main__":
    asyncio.run(main()) 