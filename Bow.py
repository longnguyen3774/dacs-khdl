from collections import Counter
import string

class BagOfWords:
    def __init__(self, documents=None, vocab_file=None, max_vocab_size=None):
        self.documents = documents
        self.max_vocab_size = max_vocab_size
        if vocab_file:
            self.vocabulary = self._load_vocabulary_from_file(vocab_file)
        else:
            self.vocabulary = self._build_vocabulary()
    
    def _preprocess(self, text):
        text = text.lower()
        text = text.translate(str.maketrans("", "", string.punctuation))
        tokens = text.split()
        return tokens
    
    def _build_vocabulary(self):
        vocab_counter = Counter()
        
        for doc in self.documents:
            tokens = self._preprocess(doc)
            vocab_counter.update(tokens)
        
        most_common_words = vocab_counter.most_common(self.max_vocab_size)
        vocab = [word for word, _ in most_common_words]
        
        return sorted(vocab)
    
    def _load_vocabulary_from_file(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            vocab = f.read().splitlines()
        
        if self.max_vocab_size:
            vocab = vocab[:self.max_vocab_size]
        
        return sorted(list(set(vocab))) 
    
    def create_bow_vector(self, document):
        tokens = self._preprocess(document)
        vector = [0] * len(self.vocabulary)
        
        word_counts = Counter(tokens)
        
        for word, count in word_counts.items():
            if word in self.vocabulary:
                idx = self.vocabulary.index(word)  
                vector[idx] = count                
        
        return vector
    
    def transform_documents(self, documents):
        bow_vectors = [self.create_bow_vector(doc) for doc in documents]
        return bow_vectors
    



