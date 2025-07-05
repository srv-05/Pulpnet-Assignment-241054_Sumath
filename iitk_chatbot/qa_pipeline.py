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

    # Split the text into sentences
    raw_sentences = raw_text.split('.')
    sentences = [sentence.strip() + '.' for sentence in raw_sentences if sentence.strip()]
    return sentences

# Example usage
file_path = "/Users/sumath/Documents/iitk_chatbot/clean_data.txt"
passages = load_articles(file_path)

embeddings = embedder.encode(passages)
index = faiss.IndexFlatL2(embeddings[0].shape[0])
index.add(np.array(embeddings))


def retrieve(query, k=200):
    query_vec = embedder.encode([query])
    _, I = index.search(np.array(query_vec), k)
    return [passages[i] for i in I[0]]

def get_answer(query):
    words=query.split()
    contexts = retrieve(query)
    sentence_candidates = []

    for context in contexts:
        inputs = tokenizer.encode_plus(query, context, return_tensors="pt", truncation=True, max_length=512)
        input_ids = inputs["input_ids"]
        tokens = tokenizer.convert_ids_to_tokens(input_ids[0])

        with torch.no_grad():
            outputs = bert_model(**inputs)
            start_scores = outputs.start_logits
            end_scores = outputs.end_logits

        max_answer_len = 50
        best_score = float("-inf")
        for start_idx in range(len(start_scores[0])):
            for end_idx in range(start_idx, min(start_idx + max_answer_len, len(end_scores[0]))):
                score = start_scores[0][start_idx].item() + end_scores[0][end_idx].item()
                if score > best_score:
                    best_score = score

        sentence_candidates.append((best_score, context.strip()))

    sorted_sentences = sorted(set(sentence_candidates), key=lambda x: x[0], reverse=True)
    top_sentences = [sent for _, sent in sorted_sentences[:5]]
    new=[]
    if 'Dhobi' in words:
        for i in top_sentences:
            if 'Written' in i:
                continue
            if any(word.lower() in i.lower() for word in words):
                new.append(i)
        return new
    return top_sentences

