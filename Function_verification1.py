import json

def verification1(file_path):
    """
    Verifies that each DA Record in the given JSON file contains the required keys.
    Required keys: 'DA Record Summary', 'processRun', 'DID', 'DID_Key', 'Signed Credential'

    Args:
        file_path (str): Path to the AA-Log JSON file

    Returns:
        list of dict: List of validation results for each DA Record
    """
    required_keys = [
        "DA Record Summary",
        "processRun",
        "DID",
        "DID_Key",
        "Signed Credential"
    ]

    validation_results = []

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        for group_index, record_group in enumerate(data):
            if not isinstance(record_group, list):
                continue  # skip if not a list
            for record_index, entry in enumerate(record_group):
                if not isinstance(entry, dict) or "DA Record" not in entry:
                    continue
                da_record = entry["DA Record"]
                missing_keys = [key for key in required_keys if key not in da_record]
                validation_results.append({
                    "group": group_index,
                    "record": record_index,
                    "valid": not missing_keys,
                    "missing_keys": missing_keys
                })

    except Exception as e:
        print(f"❌ Error reading or parsing the file: {e}")
        return []

    return validation_results
