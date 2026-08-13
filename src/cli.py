import json
from src.database import (
    connect_database,
    create_tables,
    save_analysis_result,)
from src.report import (
    generate_markdown_report,
    save_markdown_report,
    generate_comparison_section,)
from src.parser import parse_endpoints
from src.comparison import compare_api_versions

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

def build_analysis_results(data):
    endpoints = parse_endpoints(data)
    security_results = analyze_endpoint_security(data)
    parameter_results = extract_parameters(data)

    security_map = {
        (result["method"], result["path"]): result.get("security", [])
        for result in security_results
    }

    parameter_map = {
        (result["method"], result["path"]): result.get("parameters", [])
        for result in parameter_results
    }

    results = []

    for endpoint in endpoints:
        method = endpoint["method"]
        path = endpoint["path"]
        key = (method, path)

        security = security_map.get(key, [])
        parameters = parameter_map.get(key, [])

        signals = tag_review_signals(
            method,
            path,
            parameters
        )

        results.append({
            "method": method,
            "path": path,
            "security": security,
            "parameters": parameters,
            "signals": signals
        })

    return results
def run_comparison_mode():
    try:
        old_path = input("Enter old OpenAPI file path: ").strip()
        new_path = input("Enter new OpenAPI file path: ").strip()

        old_data = load_openapi(old_path)
        new_data = load_openapi(new_path)

        validate_openapi(old_data)
        validate_openapi(new_data)

        comparison_result = compare_api_versions(
            old_data,
            new_data
        )

        comparison_markdown = generate_comparison_section(
            comparison_result
        )

        save_markdown_report(
            comparison_markdown,
            "api_comparison_report.md"
        )

        print("Comparison report saved to api_comparison_report.md")

    except FileNotFoundError:
        print("File not found.")

    except json.JSONDecodeError:
        print("JSON Decode Error.")

    except KeyError as e:
        print(f"Missing required field: {e}")

    except ValueError as e:
        print(e)

def run_analysis_mode():
    try:
        data = load_openapi(path)
        validate_openapi(data)

        title = data["info"]["title"]
        version = data["info"]["version"]

        endpoints = parse_endpoints(data)
        endpoints_count = len(endpoints)

        print(f"API Title : {title}")
        print(f"Version   : {version}")
        print(f"Endpoints : {endpoints_count}")

        print("=======================")
        print("Endpoints")
        print("=======================")

        for endpoint in endpoints:
            print(endpoint["method"], endpoint["path"])

        security_results = analyze_endpoint_security(data)

        print("=======================")
        print("Authentication Analysis")
        print("=======================")

        for result in security_results:
            method = result.get("method", "")
            path = result.get("path", "")
            security_list = result.get("security", [])

            sec_str = (
                ", ".join(security_list)
                if security_list
                else "No authentication requirement"
            )

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

            print(f"{method} {path}")

            if signals:
                for signal in signals:
                    print(f"- {signal}")
            else:
                print("- No review signals")

            print()

        # Build unified analysis results
        analysis_results = build_analysis_results(data)

        # Save results to SQLite
        conn = connect_database("attack_surface.db")
        cursor = conn.cursor()

        create_tables(cursor)

        for result in analysis_results:
            save_analysis_result(cursor, result)

        conn.commit()
        conn.close()

        print("=======================")
        print("Persistence")
        print("=======================")
        print("Analysis saved to attack_surface.db")
        report_text = generate_markdown_report(title,version,analysis_results)
        save_markdown_report(report_text,"attack_surface_report.md")
        print("Report saved to attack_surface_report.md")

    except FileNotFoundError:
        print("File not found.")

    except json.JSONDecodeError:
        print("JSON Decode Error.")

    except KeyError as e:
        print(f"Missing required field: {e}")

    except ValueError as e:
        print(e)


def main():
    print("Attack Surface Notebook")
    print("Version: 0.1.0")
    print()
    print("Choose mode:")
    print("1. Analyze API")
    print("2. Compare API versions")

    choice = input("Choose mode: ").strip()

    if choice == "1":
        run_analysis_mode()
    elif choice == "2":
        run_comparison_mode()
    else:
        print("Invalid choice.")

if __name__ == "__main__":
    main()
    
