from rag_system import query_llm_with_rag
def generate_test_code(natural_language_query, framework="Selenium Java TestNG"):
        system_prompt = f"""You are an expert {framework} Test Automation Engineer.
        Generate a complete and runnable test case based on the user's request.
        Include necessary imports, class structure, and a single @Test method.
        Use explicit waits (WebDriverWait) for element interactions in Selenium/Playwright.
        Use standard assertion libraries (e.g., TestNG Assert).
        If the query mentions a browser, configure the WebDriver for that browser.
        If a locator type (id, xpath, css) is not specified, make a reasonable guess.
        Assume common test methods like 'driver.get()', 'driver.findElement()', 'sendKeys()', 'click()'.

        Provide the code strictly within a Java code block (```java ... ```).
        """
        full_query = f"{natural_language_query} using {framework}"
        response = query_llm_with_rag(system_prompt + "\nUser Query: " + full_query)

        # Extract code block
        if "```java" in response:
            code = response.split("```java")[1].split("```")[0].strip()
            return code
        return response # Return raw response if no code block found

# Test
#print(generate_test_code("Write a login test for Firefox using username 'test@example.com' and password 'password123' on a page with id='username', id='password', and id='submitBtn'"))
