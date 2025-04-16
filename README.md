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

- Python 3.8+ (for local installation)
- Groq API key
- Internet connection for web searching
- Docker (optional, for containerized deployment)

### Option 1: Local Installation

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

4. Install spaCy language model:
   ```
   python -m spacy download en_core_web_sm
   ```

5. Run the application:
   ```
   python -m streamlit run main_simplified.py
   ```

### Option 2: Docker Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/AI-Powered-Debate-Fact-Checker.git
   cd AI-Powered-Debate-Fact-Checker
   ```

2. Create a `.env` file with your API key:
   ```
   GROQ_API_KEY=your_groq_api_key_here
   SPACY_MODEL=en_core_web_sm
   ```

3. Build and run with Docker Compose:
   ```
   docker-compose up -d
   ```

4. Access the application at http://localhost:8501

### Stopping the Docker Container

To stop the application:
```
docker-compose down
```

## How to Use

1. When the application starts, you'll see a web interface in your browser
2. Enter text directly or upload a WAV audio file
3. Click "Process" to start the analysis
4. Review the extracted claims and fact-check results
5. Explore the visualizations showing verification statistics

For more detailed instructions, see [USER_GUIDE.md](USER_GUIDE.md).

## Technologies Used

- Streamlit: Web interface
- Groq API: AI-powered text analysis
- spaCy: Natural language processing
- Plotly: Interactive visualizations
- Docker: Containerization


