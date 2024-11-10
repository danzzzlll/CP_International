import logging
from .model import ClassificationModel
from .keywords import KeyWords
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

model_name = "deepvk/USER-bge-m3"

class TypeBert:
    def __init__(self, mode="type"): # 2 mode "type", "stop_dot"
        self.model = SentenceTransformer(model_name)
        logger.info("Model Loaded!!!")
        if mode == "type":
            self.keywords = KeyWords.type_keywords
        else:
            self.keywords = KeyWords.stop_dot_keywords
        logger.info(f'Use {mode} keywords')

    def make_keywords_embed(self):
        type_keywords_embedded = {}
        for key in self.keywords.keys():
            type_keywords_embedded[key] = [self.model.encode(self.keywords[key])]
        return type_keywords_embedded
    
    def make_text_embed(self, text):
        return self.model.encode([text], normalize_embeddings=True)

    def find_nearest(self, text):
        element = self.make_text_embed(text=text)
        max_sim = 0
        ans = ''
        type_keywords_embedded = self.make_keywords_embed()
        for key in type_keywords_embedded.keys():
            sim = cosine_similarity(type_keywords_embedded[key][0], element).flatten()
            if sim[0] > max_sim:
                ans = key
                max_sim = sim[0]
        return ans
    
    def __call__(self, text):
        return self.find_nearest(text=text)