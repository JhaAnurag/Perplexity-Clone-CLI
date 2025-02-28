# Perplexity-Clone-CLI

A powerful command-line search and AI assistant inspired by Perplexity AI. This tool fetches relevant web search results, extracts content from top pages, and generates AI-powered summaries in Markdown format using Gemini AI.

## Features 🚀
- 🔍 **Web Search:** Fetches top search results for your query.
- 🌍 **Website Content Extraction:** Retrieves and summarizes content from top sources.
- 🤖 **AI-Powered Answers:** Uses Gemini AI to generate concise, well-structured responses.
- 🔑 **Secure API Usage:** Prompts for an API key instead of hardcoding it.

## Installation 📥
### **Prerequisites**
- Python 3.8+
- Pip
- A Gemini AI API Key (Get one from Google)

### **Setup**
```sh
# Clone the repository
git clone https://github.com/JhaAnurag/Perplexity-Clone-CLI.git
cd Perplexity-Clone-CLI

# Install dependencies
pip install -r requirements.txt
```

## Usage 🛠️
### **Run the CLI**
```sh
python main.py
```

### **Example Workflow**
1. **Enter your Gemini API Key** when prompted.
2. **Enter a search query** (e.g., `Latest AI trends`)
3. **View search results** fetched from the web.
4. **See AI-generated summaries** based on fetched data.
5. **Enjoy clean, structured Markdown output in your terminal!**

## Dependencies 📦
- `requests` - Fetch web pages
- `googlesearch-python` - Perform Google searches
- `trafilatura` - Extract text from web pages
- `google-generativeai` - Interface with Gemini AI

## API Key Setup 🔑
- The script will **prompt you** for an API key on first run.
- You can also set it manually as an environment variable:
  ```sh
  export GEMINI_API_KEY="your_api_key_here"
  ```

## Contribution 🤝
Feel free to fork, contribute, or submit issues!

## Todo
- agentic back and forth behaviour
- multiple gpt
- deep research?
- gui

## License 📜
MIT License
