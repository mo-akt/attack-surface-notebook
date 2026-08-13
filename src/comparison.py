from src.parser import parse_endpoints

def compare_api_versions(old_data, new_data):
    old_endpoint_list = parse_endpoints(old_data)
    new_endpoint_list = parse_endpoints(new_data)

    old_endpoints = {
        (endpoint["method"], endpoint["path"])
        for endpoint in old_endpoint_list
    }

    new_endpoints = {
        (endpoint["method"], endpoint["path"])
        for endpoint in new_endpoint_list
    }

    added = new_endpoints - old_endpoints
    removed = old_endpoints - new_endpoints
    unchanged = old_endpoints & new_endpoints

    added_results = [
        {"method": method, "path": path}
        for method, path in sorted(added)
    ]

    removed_results = [
        {"method": method, "path": path}
        for method, path in sorted(removed)
    ]

    unchanged_results = [
        {"method": method, "path": path}
        for method, path in sorted(unchanged)
    ]

    return {
        "added": added_results,
        "removed": removed_results,
        "unchanged": unchanged_results
    }