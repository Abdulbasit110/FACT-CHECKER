# User Guide: AI-Powered Fact-Checker

This guide will help you use the AI-Powered Fact-Checker to verify claims in text or audio.

## Starting the Application

1. Open your terminal/command prompt
2. Navigate to the project directory
3. Run the command: `python -m streamlit run main_simplified.py`
4. The application will open in your web browser

## Using the Application

### Step 1: Input Content for Analysis

You can provide content for fact-checking in two ways:

- **Enter text directly**: Type or paste text into the text area
- **Upload audio**: Upload a WAV file using the file uploader

![Input Screen](screenshot-localhost_8501-2024_09_23-21_02_18.png)

### Step 2: Process the Content

1. Click the "Process" button
2. The application will:
   - Transcribe audio (if uploaded)
   - Extract fact-checkable claims
   - Fact-check each claim

### Step 3: Review Results

#### Transcribed Text and Claims
- Review the transcribed text (from audio) or your entered text
- See the list of extracted claims

#### Fact-Check Results
For each claim, you'll see:
- Verification status (Verified, Partially Verified, Not Verified)
- Confidence level
- Explanation with supporting evidence
- Potential bias in the claim
- Sources used for verification
- Truth meter visualization showing sentiment/truthfulness rating

#### Overall Statistics
- View a pie chart showing the distribution of verified, partially verified, and not verified claims

#### Current Topics
- See a list of key topics identified in the content

## Tips for Best Results

1. **For text input**:
   - Use clear, concise statements
   - Include factual claims rather than opinions
   - Provide enough context for accurate fact-checking

2. **For audio files**:
   - Use high-quality recordings with clear speech
   - WAV format is required
   - Shorter clips (under 5 minutes) work best

3. **Reviewing results**:
   - Click on claim expanders to see detailed analysis
   - Check sources for additional verification
   - Consider the confidence level when evaluating results 