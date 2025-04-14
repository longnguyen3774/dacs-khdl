import gensim
import numpy as np

class LoadsWord2VecModel:
    def __init__(self, model_path):
        self.model_path = model_path
        self.model = None
        self.load_model()

    def load_model(self):
        try:
            print("Đang tải mô hình Word2Vec...")
            self.model = gensim.models.KeyedVectors.load_word2vec_format(self.model_path, binary=True)
            print("Mô hình đã được tải thành công!")
        except Exception as e:
            print(f"Lỗi khi tải mô hình: {e}")
            self.model = None

    def get_sentence_vector(self, sentence):
        if not self.model:
            print("Mô hình chưa được tải.")
            return None
        
        words = sentence.split() 
        word_vectors = []
        
        for word in words:
            if word in self.model:
                word_vectors.append(self.model[word])
        
        if len(word_vectors) > 0:
            return np.mean(word_vectors, axis=0)
        else:
            return None
    
    def get_full_doc_vector(self, documents):
        if not self.model:
            print("Mô hình chưa được tải.")
            return None
        
        doc_vectors = []
        
        for doc in documents:
            words = doc.split() 
            word_vectors = []
            
            for word in words:
                if word in self.model:
                    word_vectors.append(self.model[word])
            
            if len(word_vectors) > 0:
                doc_vectors.append(np.mean(word_vectors, axis=0))
            else:
                doc_vectors.append(None)
        
        return doc_vectors
        


model_path = '/home/ngan/dacs-khdl/weight/model.bin'
word2vec_model = LoadsWord2VecModel(model_path)
sentence = "Xin chào bạn"
vector = word2vec_model.get_sentence_vector(sentence)
print(vector)