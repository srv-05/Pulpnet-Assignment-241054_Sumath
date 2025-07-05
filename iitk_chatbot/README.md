# IIT Kanpur Chatbot (Vox Populi)

This is a transformer-powered chatbot that answers user queries using content scraped from [Vox Populi](https://voxiitk.com), the student media body of IIT Kanpur. It combines semantic retrieval with BERT-based question answering.

---

## Features

- Crawls and cleans articles from Vox Populi
- Uses `MiniLM` for semantic similarity search
- Uses `BERT (fine-tuned on SQuAD)` for extractive QA
- Fully interactive UI via Streamlit

---

## Directory Structure

iitk_chatbot

├── app.py                 # Streamlit UI

├── qa_pipeline.py         # Retrieval + QA logic

├── scrape_iitk.py         # Vox Populi scraper

├── requirements.txt       # Python dependencies

├── README.md              # Project documentation

└── data/

└── cleaned_data.txt   # Scraped and cleaned paragraphs

---

## Setup Instructions

### 1. Clone the Repo

git clone https://github.com/yourusername/Pulpnet-Assignment-241054_Sumath/iitk_chatbot.git

cd Pulpnet-Assignment-241054_Sumath

cd iitk_chatbot

### 2.Install dependencies
pip install -r requirements.txt

### 4.Scrape Vox Populi Articles
python scrape_iitk.py

### 5.Run the Chatbot
streamlit run app.py
