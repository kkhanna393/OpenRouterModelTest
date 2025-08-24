import requests
import json
import os
from typing import Dict, List, Tuple, Any
import re

class OpenRouterClient:
    """
    Client for interacting with the OpenRouter API.
    
    OpenRouter is a unified API that provides access to various AI models from
    different providers like OpenAI, Anthropic, Google, etc. This client handles
    authentication, model listing, and generating completions.
    
    Attributes:
        BASE_URL (str): Base URL for the OpenRouter API
        MODELS_ENDPOINT (str): Endpoint for listing available models
        COMPLETIONS_ENDPOINT (str): Endpoint for generating completions
        api_key (str): API key for authentication
        demo_mode (bool): Whether to use demo mode (no API calls)
        headers (dict): HTTP headers for API requests
    """
    
    BASE_URL = "https://openrouter.ai/api/v1"
    MODELS_ENDPOINT = f"{BASE_URL}/models"
    COMPLETIONS_ENDPOINT = f"{BASE_URL}/chat/completions"
    
    def __init__(self, api_key=None):
        """
        Initialize the OpenRouter client with the provided API key or from environment.
        
        Args:
            api_key (str, optional): API key for OpenRouter. If not provided,
                                     will try to get from environment variable.
        """
        self.api_key = api_key or os.environ.get("OPENROUTER_API_KEY", "")
        
        if self.api_key:
            print(f"OpenRouter API key: {self.api_key}")
        else:
            print("No OpenRouter API key provided.")

        # For demo purposes, allow initialization without an API key
        if not self.api_key:
            print("Warning: No OpenRouter API key provided. Using demo mode.")
            self.demo_mode = True
        else:
            self.demo_mode = False
        
        # Set up headers for API requests
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
    
    def get_available_models(self) -> List[Tuple[str, str]]:
        """
        Fetch available models from OpenRouter API.
        
        Returns:
            List[Tuple[str, str]]: List of tuples containing model ID and description
                                  in format [(model_id, model_description), ...]
        """
        # In demo mode, just return the default model list
        if hasattr(self, 'demo_mode') and self.demo_mode:
            return [
                ("anthropic/claude-3-opus", "Claude 3 Opus - Anthropic's most powerful model"),
                ("anthropic/claude-3-sonnet", "Claude 3 Sonnet - Balanced model"),
                ("anthropic/claude-3-haiku", "Claude 3 Haiku - Fast model"),
                ("openai/gpt-4o", "GPT-4o - OpenAI's latest model"),
                ("openai/gpt-4-turbo", "GPT-4 Turbo - Powerful model"),
                ("openai/gpt-3.5-turbo", "GPT-3.5 Turbo - Fast and efficient"),
                ("google/gemini-pro", "Gemini Pro - Google's flagship model"),
                ("meta-llama/llama-3-70b-instruct", "Llama 3 70B - Meta's large model"),
            ]
            
        try:
            # Make API request to get available models
            response = requests.get(self.MODELS_ENDPOINT, headers=self.headers)
            response.raise_for_status()  # Raise exception for HTTP errors
            
            # Parse response JSON
            models_data = response.json().get("data", [])
            
            # Format for Django form choices: [(id, display_name), ...]
            model_choices = [(model["id"], f"{model['name']} - {model.get('description', 'No description')}") 
                             for model in models_data]
            
            return model_choices
        except requests.RequestException as e:
            print(f"Error fetching models: {e}")
            # Return a default list if API fails
            return [
                ("anthropic/claude-3-opus", "Claude 3 Opus - Anthropic's most powerful model"),
                ("anthropic/claude-3-sonnet", "Claude 3 Sonnet - Balanced model"),
                ("anthropic/claude-3-haiku", "Claude 3 Haiku - Fast model"),
                ("openai/gpt-4o", "GPT-4o - OpenAI's latest model"),
                ("openai/gpt-4-turbo", "GPT-4 Turbo - Powerful model"),
                ("openai/gpt-3.5-turbo", "GPT-3.5 Turbo - Fast and efficient"),
                ("google/gemini-pro", "Gemini Pro - Google's flagship model"),
                ("meta-llama/llama-3-70b-instruct", "Llama 3 70B - Meta's large model"),
            ]
    
    def generate_completion(self, prompt: str, model_id: str) -> Dict[str, Any]:
        """
        Generate a completion using the specified model.
        
        Args:
            prompt (str): The user's input prompt
            model_id (str): The ID of the model to use
            
        Returns:
            Dict[str, Any]: Dictionary containing:
                - raw_output: The unprocessed markdown response
                - formatted_output: HTML-formatted version of the response
        """
        # In demo mode, return a sample response
        if hasattr(self, 'demo_mode') and self.demo_mode:
            # Generate a demo response without making an API call
            raw_output = self._get_demo_response(prompt, model_id)
            formatted_output = self.simple_markdown_to_html(raw_output)
            
            return {
                "raw_output": raw_output,
                "formatted_output": formatted_output
            }
        
        # Prepare request data for the OpenRouter API
        data = {
            "model": model_id,
            "messages": [{"role": "user", "content": prompt}]
        }
        
        try:
            # Make API request to generate completion
            response = requests.post(
                self.COMPLETIONS_ENDPOINT, 
                headers=self.headers,
                json=data
            )
            response.raise_for_status()  # Raise exception for HTTP errors
            
            # Parse response JSON
            result = response.json()
            raw_output = result.get("choices", [{}])[0].get("message", {}).get("content", "No response")
            
            # Format the markdown output using basic HTML conversion
            formatted_output = self.simple_markdown_to_html(raw_output)
            
            return {
                "raw_output": raw_output,
                "formatted_output": formatted_output
            }
        except requests.RequestException as e:
            # Handle API errors
            error_message = f"Error generating completion: {str(e)}"
            return {
                "raw_output": error_message,
                "formatted_output": f"<p>{error_message}</p>"
            }
            
    def _get_demo_response(self, prompt: str, model_id: str) -> str:
        """
        Generate a demo response when no API key is available.
        
        Args:
            prompt (str): The user's input prompt
            model_id (str): The ID of the model requested
            
        Returns:
            str: A markdown-formatted demo response
        """
        # Get the model name from the model ID
        model_name = next((name for id, name in self.get_available_models() if id == model_id), model_id)
        
        # Create a formatted demo response
        response = f"""# Response from {model_name}

This is a demo response since no OpenRouter API key was provided. In a production environment, this would be an actual response from the selected AI model.

## About Your Prompt

You asked:

> {prompt}

## Sample Response

Here's how the AI might respond to your prompt:

1. First point about your query
2. Second point with more details
3. Third point with some analysis

### Code Example

```python
def example_function():
    print("This is just a demonstration")
    return "No actual API call was made"
```

**Important note:** To get real responses from AI models, you'll need to:

- Create an account at [OpenRouter](https://openrouter.ai/)
- Get an API key
- Set it as an environment variable or in your settings

*This is just placeholder text to demonstrate formatting.*
"""
        return response
    
    def simple_markdown_to_html(self, text: str) -> str:
        """
        Convert markdown text to HTML without external dependencies.
        
        This is a simplified markdown parser that handles common markdown elements:
        - Headers (h1-h4)
        - Lists (ordered and unordered)
        - Code blocks
        - Bold and italic text
        - Links
        
        Args:
            text (str): Markdown text to convert
            
        Returns:
            str: HTML-formatted version of the input
        """
        # Split text into lines for processing
        lines = text.split('\n')
        in_code_block = False
        result = []
        
        i = 0
        while i < len(lines):
            line = lines[i]
            
            # Handle code blocks
            if line.startswith('```'):
                if not in_code_block:
                    # Start of code block
                    language = line[3:].strip()
                    result.append('<pre><code class="language-{0}">'.format(language))
                    in_code_block = True
                else:
                    # End of code block
                    result.append('</code></pre>')
                    in_code_block = False
                i += 1
                continue
            
            # Inside code block - escape HTML characters
            if in_code_block:
                line = line.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
                result.append(line)
                i += 1
                continue
            
            # Headers
            if line.startswith('# '):
                result.append('<h1>{0}</h1>'.format(line[2:]))
            elif line.startswith('## '):
                result.append('<h2>{0}</h2>'.format(line[3:]))
            elif line.startswith('### '):
                result.append('<h3>{0}</h3>'.format(line[4:]))
            elif line.startswith('#### '):
                result.append('<h4>{0}</h4>'.format(line[5:]))
            
            # Unordered lists
            elif line.startswith('- '):
                # Check if this is the start of a list
                if i == 0 or not lines[i-1].startswith('- '):
                    result.append('<ul>')
                
                result.append('<li>{0}</li>'.format(line[2:]))
                
                # Check if this is the end of a list
                if i == len(lines) - 1 or not lines[i+1].startswith('- '):
                    result.append('</ul>')
            
            # Ordered lists
            elif line.strip() and line[0].isdigit() and line[1:].startswith('. '):
                # Check if this is the start of a list
                if i == 0 or not (lines[i-1].strip() and lines[i-1][0].isdigit() and lines[i-1][1:].startswith('. ')):
                    result.append('<ol>')
                
                result.append('<li>{0}</li>'.format(line[line.find('.')+2:]))
                
                # Check if this is the end of a list
                if i == len(lines) - 1 or not (lines[i+1].strip() and lines[i+1][0].isdigit() and lines[i+1][1:].startswith('. ')):
                    result.append('</ol>')
            
            # Regular text with potential inline formatting
            else:
                # Process inline formatting
                formatted_line = line
                
                # Bold text
                formatted_line = formatted_line.replace('**', '<strong>', 1)
                formatted_line = formatted_line.replace('**', '</strong>', 1)
                
                # Italic text
                formatted_line = formatted_line.replace('*', '<em>', 1)
                formatted_line = formatted_line.replace('*', '</em>', 1)
                
                # Links - using regex to match [text](url) pattern
                formatted_line = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2">\1</a>', formatted_line)
                
                # Empty lines become paragraph breaks
                if not line.strip():
                    result.append('<br>')
                else:
                    # Wrap non-empty, non-special lines in paragraph tags
                    if not any(tag in formatted_line for tag in ['<h1>', '<h2>', '<h3>', '<h4>', '<ul>', '<ol>', '<li>']):
                        formatted_line = '<p>' + formatted_line + '</p>'
                    
                    result.append(formatted_line)
            
            i += 1
        
        # Close any unclosed code blocks
        if in_code_block:
            result.append('</code></pre>')
        
        # Join all processed lines into a single HTML string
        return '\n'.join(result)
