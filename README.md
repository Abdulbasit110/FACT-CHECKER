# AI-Powered Fact-Checker

A streamlined tool for fact-checking claims in text or audio debates using AI.

## Features

- **Text & Audio Processing**: Upload WAV files or enter text directly
- **Automated Claim Extraction**: AI identifies fact-checkable claims from text
- **AI-Powered Fact-Checking**: Uses Groq API for intelligent verification
- **Interactive Visualizations**: Truth meters and verification statistics
- **Web Search Integration**: Gathers supporting information for fact-checking

## Getting Started

### Prerequisites

- Python 3.8+
- Groq API key
- Internet connection for web searching

### Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/AI-Powered-Debate-Fact-Checker.git
   cd AI-Powered-Debate-Fact-Checker
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Set up your API keys in a `.env` file:
   ```
   GROQ_API_KEY=your_groq_api_key_here
   SPACY_MODEL=en_core_web_sm
   ```

### Running the Application

Run the simplified version of the application:
```
python -m streamlit run main_simplified.py
```

## How to Use

1. When the application starts, you'll see a web interface in your browser
2. Enter text directly or upload a WAV audio file
3. Click "Process" to start the analysis
4. Review the extracted claims and fact-check results
5. Explore the visualizations showing verification statistics

## Technologies Used

- Streamlit: Web interface
- Groq API: AI-powered text analysis
- spaCy: Natural language processing
- Plotly: Interactive visualizations

