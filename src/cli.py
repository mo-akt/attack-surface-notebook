import json
def load_openapi(path):
    with open(path, 'r', encoding='utf-8') as file:
         data = json.load(file)
         return data

def validate_openapi(data):
    """
    Validates that the provided dictionary contains the minimum required fields for an OpenAPI document.
    Raises ValueError with a specific message if a field is missing, otherwise returns True.
    """
    # Check if the root level fields exist
    if "info" not in data:
        raise ValueError("Missing required field: info")
        
    if "paths" not in data:
        raise ValueError("Missing required field: paths")
        
    # Check if nested required fields inside 'info' exist
    if "title" not in data["info"]:
        raise ValueError("Missing required field: info.title")
        
    if "version" not in data["info"]:
        raise ValueError("Missing required field: info.version")
        
    return True

def parse_endpoints(data):
    """
    Extracts all endpoints from OpenAPI data and returns them as a list of dictionaries.
    Each dictionary contains the HTTP method (uppercase) and the path.
    """
    endpoints = []
    HTTP_METHODS = {"get", "post", "put", "patch", "delete","head", "options", "trace"}
    for path, methods in data.get("paths", {}).items():
        for method in methods:
            if method.lower() in HTTP_METHODS:
                 endpoints.append({
                   "method": method.upper(),
                     "path": path
                              })
            
    return endpoints



def main():
    print("Attack Surface Notebook")
    print("Version: 0.1.0")

    path = input("Enter OpenAPI file path: ").strip()
    try:
        data=load_openapi(path)
        validate_openapi(data)

        title = data["info"]["title"]
        version = data["info"]["version"]
        endpoints=parse_endpoints(data)

        endpoints_count = len(endpoints)
        print(f"API Title : {title}")
        print(f"Version   : {version}")
        print(f"Endpoints : {endpoints_count}")
        for endpoint in endpoints:
            print(endpoint["method"], endpoint["path"])

    except FileNotFoundError:
        print("File not found.")
    except json.JSONDecodeError:
        print("JSON Decode Error.")
    except KeyError as e:
        print(f"Missing required field: {e}")
    except ValueError as e:
        print(e)




if __name__ == "__main__":
    main()
    
