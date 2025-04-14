import torch
from transformers import AutoModel, AutoTokenizer

class PhoBERTEmbedding:
    def __init__(self, model_name="vinai/phobert-base-v2", max_seq_length=256):
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModel.from_pretrained(model_name)
        self.max_seq_length = max_seq_length
        print("Mô hình PhoBERT đã được tải thành công!")

    def encode(self, sentence):

        input_ids = torch.tensor([self.tokenizer.encode(sentence, max_length=self.max_seq_length, truncation=True)])
        with torch.no_grad():
            features = self.model(input_ids)

        return features.last_hidden_state.squeeze(0)

    def batch_encode(self, sentences):
        embeddings = []
        
        for sentence in sentences:
            embedding = self.encode(sentence)
            embeddings.append(embedding.mean(dim=0))  # Lấy trung bình các token trong câu
        
        return torch.stack(embeddings)



model = PhoBERTEmbedding()
sentence = "Xin chào bạn"
embedding = model.encode(sentence)
print(embedding)