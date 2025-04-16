FROM python:3.9-slim

WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install additional dependencies
RUN pip install --no-cache-dir numpy==1.24.3
RUN python -m spacy download en_core_web_sm

# Copy the rest of the application
COPY . .

# Expose the port Streamlit runs on
EXPOSE 8501

# Command to run the application
CMD ["python", "-m", "streamlit", "run", "main_simplified.py", "--server.port=8501", "--server.address=0.0.0.0"] 