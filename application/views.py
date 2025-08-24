from doctest import debug  # Imported for debugging, consider replacing with a simple boolean
from django.shortcuts import render
from django.conf import settings
from .forms import PromptForm
from .openrouter_client import OpenRouterClient
import os

# Initialize the OpenRouter client
def get_openrouter_client():
    """
    Creates and configures an OpenRouter client with appropriate API key.
    
    The function tries to get the API key from:
    1. Environment variables first (recommended for production)
    2. Django settings as a fallback (configured in settings.py)
    
    Returns:
        OpenRouterClient: Configured client instance ready to make API calls
    """
    # Get API key from environment variable or use a placeholder for development
    api_key = os.environ.get("OPENROUTER_API_KEY", "")
    
    # For development purposes, you could also add a key in settings.py
    if not api_key and hasattr(settings, 'OPENROUTER_API_KEY'):
        api_key = settings.OPENROUTER_API_KEY
        
    return OpenRouterClient(api_key=api_key)

def index(request):
    """
    Main view to handle the prompt form submission and display results.
    
    This view:
    1. Initializes the OpenRouter client
    2. Fetches available AI models
    3. Processes form submissions
    4. Generates AI completions when form is submitted
    5. Renders the template with form and results
    
    Args:
        request: Django HTTP request object
        
    Returns:
        HttpResponse: Rendered template with context
    """
    # Initialize OpenRouter client and get available models
    client = get_openrouter_client()
    model_choices = client.get_available_models()
    
    # Debug information - prints available models in a readable format
    if debug:
        print("Available models:", model_choices)
        print(type(model_choices))
        for model_id, model_description in model_choices:
            print(f"  - {model_id}: {model_description}")

    # Initialize result variables
    raw_output = ""
    formatted_output = ""
    selected_model = ""
    
    if request.method == 'POST':
        # Process form submission
        form = PromptForm(request.POST, model_choices=model_choices)
        
        if form.is_valid():
            # Extract validated data from the form
            prompt = form.cleaned_data['prompt']
            selected_model = form.cleaned_data['model']
            
            # Generate completion using OpenRouter
            result = client.generate_completion(prompt, selected_model)
            
            # Extract results for template rendering
            raw_output = result['raw_output']
            formatted_output = result['formatted_output']
    else:
        # Create a new form for GET requests
        form = PromptForm(model_choices=model_choices)
    
    # Prepare context dictionary for the template
    context = {
        'form': form,
        'raw_output': raw_output,
        'formatted_output': formatted_output,
        'selected_model': selected_model,
    }
    
    # Render the template with the context
    return render(request, 'application/index.html', context)
