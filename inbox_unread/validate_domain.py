import sys
import json

# 未知数とその定義域（Domain）の定義
DOMAIN_SCHEMA = {
    "variable_x": {
        "description": "レイテンシの許容定義域 (0〜500ms)",
        "type": "number",
        "min": 0,
        "max": 500
    },
    "variable_y": {
        "description": "ステータスの定義域 (離散値)",
        "type": "enum",
        "allowed": ["PASS", "FLAGGED", "PENDING"]
    }
}

def validate_input(data):
    results = {}
    
    # variable_x の検証 (数値範囲)
    val_x = data.get("x")
    schema_x = DOMAIN_SCHEMA["variable_x"]
    if isinstance(val_x, (int, float)) and schema_x["min"] <= val_x <= schema_x["max"]:
        results["x"] = {"value": val_x, "in_domain": True}
    else:
        results["x"] = {"value": val_x, "in_domain": False, "reason": "OUT_OF_RANGE_OR_TYPE_MISMATCH"}

    # variable_y の検証 (離散値)
    val_y = data.get("y")
    schema_y = DOMAIN_SCHEMA["variable_y"]
    if val_y in schema_y["allowed"]:
        results["y"] = {"value": val_y, "in_domain": True}
    else:
        results["y"] = {"value": val_y, "in_domain": False, "reason": "NOT_IN_ALLOWED_ENUM"}

    return results

def main():
    raw = sys.stdin.read().strip()
    if not raw:
        print(json.dumps({"error": "No input provided"}, indent=2))
        return

    try:
        input_data = json.loads(raw)
    except json.JSONDecodeError:
        print(json.dumps({"error": "Invalid JSON input"}, indent=2))
        return

    validation_results = validate_input(input_data)
    
    output = {
        "domain_validation_summary": {
            "status": "COMPLETED",
            "schema_used": DOMAIN_SCHEMA,
            "results": validation_results
        }
    }
    
    print(json.dumps(output, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()
