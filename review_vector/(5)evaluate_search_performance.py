# Script đánh giá hiệu suất tìm kiếm dựa trên Precision@k, Recall@k, MRR

import json

# Load ground truth: danh sách sách mua kèm
with open('C:/Users/Nami/Desktop/DACS/co_purchased_items.json', 'r', encoding='utf-8') as f:
    co_purchased = json.load(f)

# Load kết quả tìm kiếm đã thêm user_id
with open('C:/Users/Nami/Desktop/DACS/search_results_fixed.json', 'r', encoding='utf-8') as f:
    search_results = json.load(f)

# Chuẩn bị map user_id -> danh sách itemid thực tế nên gợi ý
co_purchased_map = {user: set(item['item_id'] for item in items) for user, items in co_purchased.items()}

# Chuẩn bị map user_id -> danh sách itemid đã tìm kiếm được
retrieved_map = {}
for entry in search_results:
    user_id = entry.get('user_id')
    if not user_id:
        continue
    retrieved_map.setdefault(user_id, []).append(entry['id'])

precision_list = []
recall_list = []
mrr_list = []

top_k = 5  # số lượng top-k cần đánh giá

# Tính toán Precision@k, Recall@k, MRR cho từng user
for user_id, retrieved_items in retrieved_map.items():
    ground_truth = co_purchased_map.get(user_id, set())
    if not ground_truth:
        continue

    retrieved_topk = retrieved_items[:top_k]
    hits = [item for item in retrieved_topk if item in ground_truth]

    # Precision@k: số item đúng chia tổng số item được gợi ý
    precision_list.append(len(hits) / top_k)

    # Recall@k: số item đúng chia tổng số item cần tìm
    recall_list.append(len(hits) / len(ground_truth) if ground_truth else 0)

    # MRR: lấy vị trí đúng đầu tiên
    rr = 0
    for idx, item in enumerate(retrieved_topk, 1):
        if item in ground_truth:
            rr = 1 / idx
            break
    mrr_list.append(rr)

# Tính trung bình toàn bộ
mean_precision = sum(precision_list) / len(precision_list) if precision_list else 0
mean_recall = sum(recall_list) / len(recall_list) if recall_list else 0
mean_mrr = sum(mrr_list) / len(mrr_list) if mrr_list else 0

# In kết quả đánh giá
print(f"Mean Precision@{top_k}: {mean_precision:.4f}")
print(f"Mean Recall@{top_k}: {mean_recall:.4f}")
print(f"Mean MRR@{top_k}: {mean_mrr:.4f}")