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
def extract_security_schemes(data):
    schemes = data.get("components", {}).get("securitySchemes")
    
    if not schemes:
        return []
    
    results = []
    for name, details in schemes.items():
        scheme_type = details.get("type")
        
        if scheme_type == "http":
            results.append({
                "name": name,
                "type": "http",
                "scheme": details.get("scheme", "").lower()
            })
        elif scheme_type == "apiKey":
            results.append({
                "name": name,
                "type": "apiKey",
                "in": details.get("in"),
                "param_name": details.get("name")
            })
            
    return results

def get_operation_security(operation, global_security):
    if "security" in operation:
        return operation["security"]

    return global_security

def analyze_endpoint_security(data):
    global_security = data.get("security", [])
    results = []

    HTTP_METHODS = {
        "get", "post", "put", "patch",
        "delete", "head", "options", "trace"
    }

    for path, methods in data.get("paths", {}).items():
        for method, operation in methods.items():

            if method.lower() not in HTTP_METHODS:
                continue

            applied_security = get_operation_security(
                operation,
                global_security
            )

            security_names = []

            for requirement in applied_security:
                for scheme_name in requirement:
                    security_names.append(scheme_name)

            results.append({
                "method": method.upper(),
                "path": path,
                "security": security_names
            })

    return results
def extract_parameters(data):
    results = []

    HTTP_METHODS = {
        "get", "post", "put", "patch",
        "delete", "head", "options", "trace"
    }
    merged_parameters = {}

    for path, methods in data.get("paths", {}).items():
        path_parameters = methods.get("parameters", [])

        for method, operation in methods.items():
            if method.lower() not in HTTP_METHODS:
                continue
            operation_parameters = operation.get("parameters", [])
            merged_parameters = {}

            for parameter in path_parameters:
                key = (parameter.get("name"), parameter.get("in"))
                merged_parameters[key] = parameter

            for parameter in operation_parameters:
                key = (parameter.get("name"), parameter.get("in"))
                merged_parameters[key] = parameter

            all_parameters = list(merged_parameters.values())
            results.append({
                   "method": method.upper(),
                   "path": path,
                   "parameters": all_parameters
                   })
    return results

def tag_review_signals(method, path, parameters):
    signals = []

    normalized_path = path.lower()

    if "user" in normalized_path or "account" in normalized_path:
        signals.append("user-data")

    if "admin" in normalized_path:
        signals.append("admin-surface")

    auth_keywords = ["login", "auth", "token", "password"]

    if any(keyword in normalized_path for keyword in auth_keywords):
        signals.append("authentication-related")

    if method.upper() == "DELETE":
        signals.append("destructive-operation")

    sensitive_parameter_names = ["password","token","secret","api_key"]

    for parameter in parameters:
        parameter_name = parameter.get("name", "").lower()

        if parameter_name in sensitive_parameter_names:
            signals.append("sensitive-input")
            break

    return signals









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
        security_results = analyze_endpoint_security(data)
        for result in security_results:
            method = result.get("method", "")
            path = result.get("path", "")
            security_list = result.get("security", [])
            sec_str = ", ".join(security_list) if security_list else "No authentication requirement"
            print(f"{method} {path} -> {sec_str}")
        
        parameter_results = extract_parameters(data)

        print("=======================")
        print("Parameter Analysis")
        print("=======================")
        
        for result in parameter_results:
            method = result.get("method", "")
            path = result.get("path", "")
            parameter_list = result.get("parameters", [])
        
            print(f"{method} {path}")
        
            for parameter in parameter_list:
                name = parameter.get("name", "")
                location = parameter.get("in", "")
        
                if parameter.get("required", False):
                    required = "required"
                else:
                    required = "optional"
        
                print(f"- {name} [{location}] {required}")
                print()
        
        
        print("=======================")
        print("Review Signals")
        print("=======================")
        
        for result in parameter_results:
            method = result.get("method", "")
            path = result.get("path", "")
            parameter_list = result.get("parameters", [])
        
            signals = tag_review_signals(
                method,
                path,
                parameter_list
            )
            print()
            print(f"{method} {path}")
            
        
            if signals:
                for signal in signals:
                    print(f"- {signal}")
            else:
                print("- No review signals")
                


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
    
