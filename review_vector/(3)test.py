# Script gửi query tìm kiếm tới API server và lưu kết quả tìm kiếm vào file JSON

import requests
import json

# Địa chỉ API server FastAPI
api_url = "http://localhost:8000/search"

# Tạo dữ liệu gửi lên server
query_text = "sách phát triển bản thân"
top_k = 5

# Gửi yêu cầu POST tới API
response = requests.post(
    api_url,
    json={"query": query_text, "top_k": top_k}
)

# Kiểm tra phản hồi
if response.status_code == 200:
    raw_results = response.json()
    output = {"results": raw_results}

    # Lưu kết quả tìm kiếm vào file
    with open("C:/Users/Nami/Desktop/DACS/search_results.json", "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    print("Search results saved successfully.")
else:
    print(f"Error: {response.status_code}")
