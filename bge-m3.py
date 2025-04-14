from sentence_transformers import SentenceTransformer
import torch

model = SentenceTransformer("AITeamVN/Vietnamese_Embedding")
model.max_seq_length = 2048
sentences_1 = ["Trí tuệ nhân tạo là gì"]
doc_embeddings = model.encode(sentences_1)
print(doc_embeddings)