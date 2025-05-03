import json
import re
import html
import numpy as np
from typing import List
from autocorrect import Speller
from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct
import warnings
warnings.filterwarnings('ignore')

# Load model embedding SentenceTransformer
model = SentenceTransformer('all-MiniLM-L6-v2')

# Kết nối đến server Qdrant local
qdrant_client = QdrantClient(host="localhost", port=6333)
collection_name = "reviews"

# Khởi tạo bộ sửa lỗi chính tả
spell = Speller(lang='en')

# Hàm tiền xử lý văn bản review
def clean_text(text: str) -> str:
    text = html.unescape(text)  # Giải mã ký tự HTML
    text = re.sub(r'<[^>]+>', ' ', text)  # Xóa thẻ HTML
    text = re.sub(r'[^\w\s.,!?-]', ' ', text)  # Xóa ký tự đặc biệt
    text = text.lower()  # Chuyển thành chữ thường
    text = re.sub(r'\s+', ' ', text)  # Chuẩn hóa khoảng trắng
    text = spell(text)  # Sửa lỗi chính tả nhẹ
    return text.strip()

# Tính độ tương đồng cosine giữa hai vector
def cosine_similarity(v1: List[float], v2: List[float]) -> float:
    v1, v2 = np.array(v1), np.array(v2)
    return np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))

# Kiểm tra comment có nói về giao hàng không
def contains_shipping_keywords(text: str) -> bool:
    return any(keyword in text for keyword in ["giao hàng", "ship", "nhận hàng", "đóng gói"])

# Kiểm tra comment có phải là random ký tự không
def is_random_text(text: str) -> bool:
    return len(text.split()) <= 2 and not any(char.isalpha() for char in text)

# Kiểm tra comment có hợp lệ để encode vector không
def is_valid_comment(comment: str, book_vector: List[float]) -> bool:
    if len(comment.split()) < 5:  # Quá ngắn
        return False
    if contains_shipping_keywords(comment):  # Nói về giao hàng
        return False
    if is_random_text(comment):  # Spam random ký tự
        return False
    comment_vector = model.encode(comment).tolist()
    if cosine_similarity(comment_vector, book_vector) < 0.3:  # Không liên quan sách
        return False
    return True

# Load thông tin sách để hỗ trợ kiểm tra độ liên quan
with open("C:/Users/Nami/Desktop/DACS/happylive_books.json", 'r', encoding='utf-8') as f:
    books = json.load(f)

book_vectors = {}
for book in books:
    itemid = book["item_id"]
    name = book.get("name", "")
    description = book.get("description", "")
    text = clean_text(f"{name}. {description}")
    book_vectors[itemid] = model.encode(text).tolist()

# Load đánh giá khách hàng
with open('C:/Users/Nami/Desktop/DACS/happylive_ratings.json', 'r', encoding='utf-8') as f:
    ratings = json.load(f)

points: List[PointStruct] = []

# Xử lý từng comment và encode thành vector
for rating in ratings:
    cmtid = rating["cmtid"]
    userid = rating.get("userid")
    itemid = rating.get("itemid")
    rating_star = rating.get("rating_star")
    comment = rating.get("comment", "")

    if not itemid or not comment:
        continue  # Thiếu thông tin, bỏ qua

    book_vector = book_vectors.get(itemid)
    if not book_vector:
        continue  # Không có vector sách, bỏ qua

    clean_comment = clean_text(comment)

    if is_valid_comment(clean_comment, book_vector):
        vector = model.encode(clean_comment).tolist()
        points.append(
            PointStruct(
                id=cmtid,
                vector=vector,
                payload={
                    "userid": userid,
                    "itemid": itemid,
                    "rating_star": rating_star,
                    "comment": comment
                }
            )
        )

# Xóa collection cũ và tạo mới trên Qdrant
qdrant_client.recreate_collection(
    collection_name=collection_name,
    vectors_config={"size": 384, "distance": "Cosine"}
)

# Upload các review vector hợp lệ lên Qdrant
qdrant_client.upload_points(
    collection_name=collection_name,
    points=points
)

print(f"Done! Uploaded {len(points)} valid review vectors to Qdrant.")