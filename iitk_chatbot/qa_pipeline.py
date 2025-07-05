from transformers import BertTokenizer, BertForQuestionAnswering
import torch
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

# Load models
tokenizer = BertTokenizer.from_pretrained("bert-large-uncased-whole-word-masking-finetuned-squad")
bert_model = BertForQuestionAnswering.from_pretrained("bert-large-uncased-whole-word-masking-finetuned-squad")
embedder = SentenceTransformer("all-MiniLM-L6-v2")


# Load and process data
def load_articles(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        raw_text = f.read()

    # Split on 'Title: ' and prepend it back to each chunk
    raw_chunks = raw_text.split("Title: ")
    articles = ["Title: " + chunk.strip() for chunk in raw_chunks if chunk.strip()]
    return articles

# Example usage
file_path = "/Users/sumath/Documents/iitk_chatbot/clean_data.txt"
passages = load_articles(file_path)

embeddings = embedder.encode(passages)
index = faiss.IndexFlatL2(embeddings[0].shape[0])
index.add(np.array(embeddings))


def retrieve(query, k=3):
    query_vec = embedder.encode([query])
    _, I = index.search(np.array(query_vec), k)
    return [passages[i] for i in I[0]]


def get_answer(query):
    contexts = retrieve(query)
    best_answer = ""
    best_score = float('-inf')

    for context in contexts:
        inputs = tokenizer.encode_plus(query, context, return_tensors="pt", truncation=True, max_length=512)
        input_ids = inputs["input_ids"]
        tokens = tokenizer.convert_ids_to_tokens(input_ids[0])

        with torch.no_grad():
            outputs = bert_model(**inputs)
            start_scores = outputs.start_logits
            end_scores = outputs.end_logits

        start_idx = torch.argmax(start_scores)
        end_idx = torch.argmax(end_scores) + 1
        score = start_scores[0][start_idx].item() + end_scores[0][end_idx - 1].item()

        if start_idx < end_idx and (end_idx - start_idx) < 1000:
            if score > best_score:
                best_score = score
                best_answer = tokenizer.convert_tokens_to_string(tokens[start_idx:end_idx])

    return best_answer.strip()