# Smart Search Agent

## Overview
A Streamlit-based web app that acts as an intelligent search assistant. It takes user questions and returns answers with source references, and supports downloading the answer as a PDF.

## Features
- User-friendly question input interface
- AI-powered search and answer retrieval
- Displays sources used for the answers
- Generates downloadable PDF reports of search results

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/kingRajper/smart-search-agent.git
   cd smart-search-agent
````

2. (Optional) Create and activate a virtual environment:

   ```bash
   python -m venv venv
   source venv/bin/activate   # On Windows use: venv\Scripts\activate
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Install `wkhtmltopdf` (required for PDF generation):

   * Download from [wkhtmltopdf.org](https://wkhtmltopdf.org/downloads.html)
   * Add to your system PATH

## Usage

Run the Streamlit app:

```bash
streamlit run streamlit_app.py
```

Open your browser at the URL shown in the terminal (usually `http://localhost:8501`).

## File Structure

* `streamlit_app.py`: Main Streamlit app
* `model.py`: Contains logic for querying the search model
* `requirements.txt`: Python dependencies

```

You can copy this directly into a `README.md` file in your repo root. Need help with that too?
```
