from django import forms

class PromptForm(forms.Form):
    """
    Form for collecting user input for AI model interaction.
    
    This form has two main fields:
    1. prompt - A text area for the user to enter their prompt/question
    2. model - A dropdown to select which AI model to use
    
    The available models are dynamically populated from the OpenRouter API.
    """
    
    # Text area for prompt input
    prompt = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',  # Bootstrap styling
            'rows': 5,                # Height of the text area
            'placeholder': 'Enter your question or prompt here...'
        }),
        label='Enter your prompt',
        required=True,
        help_text='Type your question or instructions for the AI model'
    )
    
    # Dropdown for model selection
    model = forms.ChoiceField(
        widget=forms.Select(attrs={
            'class': 'form-control'   # Bootstrap styling
        }),
        label='Select AI Model',
        required=True,
        choices=[],  # Empty initially, populated dynamically in __init__
        help_text='Choose which AI model will process your prompt'
    )
    
    def __init__(self, *args, **kwargs):
        """
        Custom initialization to dynamically set available models.
        
        Args:
            *args: Variable length argument list
            **kwargs: Arbitrary keyword arguments, including 'model_choices'
                      which should contain the list of available models
        """
        # Extract model_choices from kwargs, defaulting to empty list if not provided
        model_choices = kwargs.pop('model_choices', [])
        
        # Call parent class __init__
        super(PromptForm, self).__init__(*args, **kwargs)
        
        # Update the model field's choices with the available models
        if model_choices:
            self.fields['model'].choices = model_choices
