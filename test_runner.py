import subprocess
import os

from code_generator import generate_test_code  # Import the missing function
# Assuming your Java project is structured correctly
JAVA_TEST_DIR = "/home/sanumenonmadhusoodanan/AgentAI/Eclipse/mvnProjectws/AIImplementation/src/test/java/AIImplementation/AIImplementation" # Adjust path
MAVEN_COMMAND = ["mvn", "test"] # Or ["gradle", "test"]

def run_java_test(java_code, test_class_name="SampleTestNgTest"):
    # Ensure the directory exists
    os.makedirs(JAVA_TEST_DIR, exist_ok=True)
    # Create the Java file
    file_path = os.path.join(JAVA_TEST_DIR, f"{test_class_name}.java")
    with open(file_path, "w") as f:
        # Add package and class declaration if missing in LLM output
        # Or refine LLM prompt to always include it
        full_code = f"package com.example.generated_tests;\n\n{java_code}"
        f.write(full_code)
        print(f"Generated test file: {file_path}")

        try:
            # Run Maven/Gradle test command
            result = subprocess.run(MAVEN_COMMAND, capture_output=True, text=True, check=True)
            print("Test Execution Output:\n", result.stdout)
            if result.stderr:
                print("Test Execution Errors:\n", result.stderr)
            return "PASS" if "BUILD SUCCESS" in result.stdout else "FAIL" # Simple check
        except subprocess.CalledProcessError as e:
            print(f"Test Execution Failed: {e.returncode}\n{e.stdout}\n{e.stderr}")
            return "FAIL"
        except FileNotFoundError:
            print(f"Maven/Gradle command not found. Make sure it's in your PATH. Command: {MAVEN_COMMAND}")
            return "ERROR"

# Example usage:
#generated_code = generate_test_code("Write a login test for Firefox using username 'test@example.com' and password 'password123' on a page with id='username', id='password', and id='submitBtn'") # Code from code_generator.py
#print(run_java_test(generated_code, "MyDynamicLoginTest"))
