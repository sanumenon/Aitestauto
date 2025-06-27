from rag_system import query_llm_with_rag

# Add env_domain as an argument to generate_test_code
def generate_test_code(natural_language_query, framework="Selenium Java TestNG", env_domain=None):
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
        
        # Pass env_domain to query_llm_with_rag
        response = query_llm_with_rag(system_prompt + "\nUser Query: " + full_query, env_domain=env_domain)

        # Extract code block
        if "```java" in response:
            code = response.split("```java")[1].split("```")[0].strip()
            return code
        return response