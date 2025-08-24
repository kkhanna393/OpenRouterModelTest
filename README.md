# GenAI Application

A Django web application that allows users to interact with various AI models through the OpenRouter API. The application provides a simple interface for entering prompts, selecting AI models, and viewing both raw and formatted responses.

## 📋 Features

- **Prompt Input**: User-friendly text area for entering prompts or questions
- **Model Selection**: Dropdown menu to choose from a variety of AI models available through OpenRouter
- **Dual Output Display**: 
  - Raw Markdown output directly from the model (left panel)
  - Properly formatted HTML rendering of the response (right panel)
- **Demo Mode**: Fallback functionality when no API key is provided

## 🖼️ Screenshots

*(Add screenshots of your application here once it's running)*

## 🚀 Setup and Installation

### Prerequisites

- Python 3.8+ installed
- Internet connection (for API access)
- OpenRouter API key (for production use)

### Step-by-Step Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd GenAI
   ```

2. **Install required packages**
   ```bash
   pip install django requests
   ```

3. **Set up your OpenRouter API key**
   - Create an account at [OpenRouter](https://openrouter.ai/)
   - Get your API key from the dashboard
   - Set it as an environment variable:
     ```bash
     # For Windows Command Prompt
     set OPENROUTER_API_KEY=your_api_key_here
     
     # For Windows PowerShell
     $env:OPENROUTER_API_KEY = "your_api_key_here"
     
     # For Linux/Mac
     export OPENROUTER_API_KEY=your_api_key_here
     ```
   - Alternatively, you can add it to VS Code settings:
     Create a `.vscode/settings.json` file with:
     ```json
     {
         "terminal.integrated.env.windows": {
             "OPENROUTER_API_KEY": "your_api_key_here"
         }
     }
     ```

4. **Run database migrations**
   ```bash
   python manage.py migrate
   ```

5. **Start the development server**
   ```bash
   python manage.py runserver
   ```

6. **Access the application**
   - Open your browser and navigate to `http://127.0.0.1:8000/`

## 💻 Usage Guide

1. **Enter your prompt**
   - Type your question or instructions in the text area
   - Be as specific as possible for better results

2. **Select an AI model**
   - Choose from the dropdown list of available models
   - Different models have different capabilities and specialties

3. **Generate a response**
   - Click the "Generate Response" button
   - Wait for the API to process your request

4. **View the results**
   - The left panel shows the raw markdown output
   - The right panel shows the formatted HTML version
   - Both contain the same content but with different formatting

## 🏗️ Project Structure

```
GenAI/
├── GenAI/                  # Project configuration
│   ├── settings.py         # Django settings (including API key config)
│   ├── urls.py             # Project URL routing
│   └── ...                 # Other Django project files
├── application/            # Main Django app
│   ├── forms.py            # Form definitions for user input
│   ├── openrouter_client.py # OpenRouter API client
│   ├── views.py            # View functions handling requests
│   ├── urls.py             # App URL routing
│   ├── static/             # Static files (CSS, JS)
│   │   └── application/
│   │       └── css/
│   │           └── style.css # Application styling
│   └── templates/          # HTML templates
│       └── application/
│           └── index.html  # Main page template
├── manage.py               # Django management script
└── README.md               # This documentation file
```

## 🔍 Code Explanations

### Key Components

1. **OpenRouterClient (openrouter_client.py)**
   - Handles communication with the OpenRouter API
   - Fetches available models and generates completions
   - Includes demo mode for development without an API key
   - Contains a custom markdown-to-HTML converter

2. **PromptForm (forms.py)**
   - Defines the form for collecting user input
   - Dynamically populated with available models

3. **Views (views.py)**
   - Handles HTTP requests and responses
   - Processes form submissions
   - Coordinates between the form and API client

4. **Templates (index.html)**
   - Presents the user interface
   - Displays both raw and formatted outputs

## 📝 Technical Notes

- **API Usage**: This application uses OpenRouter to access various AI models from providers like OpenAI, Anthropic, Google, etc.
- **Rate Limits**: Be aware of rate limits and costs associated with your OpenRouter plan
- **Security**: Avoid hardcoding API keys in production; use environment variables instead
- **Formatting**: The application includes a custom markdown-to-HTML converter to avoid dependencies
- **Demo Mode**: The application works without an API key in demo mode, returning placeholder responses

## 🛠️ Customization Options

- Modify the CSS in `static/application/css/style.css` to change the appearance
- Add additional fields to the form in `forms.py` for more control options
- Extend the `OpenRouterClient` class to support more API features
- Add authentication to restrict access to the application

## 📄 License

*(Add your license information here)*

## 👥 Contributors

*(Add contributor information here)*

---

*This project was created as a demonstration of Django integration with AI APIs.*
