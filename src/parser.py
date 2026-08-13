def parse_endpoints(data):
    endpoints = []

    HTTP_METHODS = {
        "get", "post", "put", "patch",
        "delete", "head", "options", "trace"
    }

    for path, methods in data.get("paths", {}).items():
        for method in methods:
            if method.lower() in HTTP_METHODS:
                endpoints.append({
                    "method": method.upper(),
                    "path": path
                })

    return endpoints