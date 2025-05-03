import json

# Load original mapping of item_id → user_id
with open("C:/Users/Nami/Desktop/DACS/co_purchased_items.json", "r", encoding="utf-8") as f:
    original_results = json.load(f)

# Load fixed search results (without user_id)
with open("C:/Users/Nami/Desktop/DACS/search_results_fixed.json", "r", encoding="utf-8") as f:
    fixed_results = json.load(f)
item_to_user = {entry["id"]: entry["user_id"] for entry in fixed_results}

# Inject user_id based on item_id
updated_results = []
missing_ids = []

for item in fixed_results:
    item_id = item["id"]
    user_id = item_to_user.get(item_id)

    if user_id:
        item["user_id"] = user_id
    else:
        item["user_id"] = None
        missing_ids.append(item_id)

    updated_results.append(item)

# Save updated results
with open("search_results_fixed.json", "w", encoding="utf-8") as f:
    json.dump(updated_results, f, indent=2, ensure_ascii=False)

# Log missing mappings (if any)
if missing_ids:
    print(f"[WARNING] Missing user_id for {len(missing_ids)} items:")
    print(missing_ids[:5], "...")  # show sample
else:
    print("[SUCCESS] All user_ids mapped correctly.")