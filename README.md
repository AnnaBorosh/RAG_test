# Multimodal RAG System

A Retrieval-Augmented Generation (RAG) system that answers user queries using recent news articles from [The Batch](https://www.deeplearning.ai/the-batch/). It integrates text, images and Gemini’s LLM to provide informed responses in a UI.

## Project structure
```text
├── app.py                 # Main Streamlit app
├── scraping.py            # Article scraper
├── ingest.py              # Loads scraped data into Pinecone
├── data/
│   └── deeplearning_batch_301_to_305.json  # scraped data
├── requirements.txt       # Python dependencies
└── README.md              # Project overview and usage instructions
```

## Setup 
1. Clone the repo

        `git clone https://github.com/AnnaBorosh/RAG_test.git`

2. Install dependencies:

        `pip install -r requirements.txt`

3. Create a `.env` file:

        ```GEMINI_API_KEY=your-api-key-here
        PINECONE_API_KEY=your-pinecone-api-key-here```

4. Run the app:

        `streamlit run app.py`


## Tools used
- Google Gemini (1.5 Flash)
- Pinecone (integrated embedding, `llama-text-embed-v2`)
- Streamlit
- BeautifulSoup