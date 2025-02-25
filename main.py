import os
import requests
from googlesearch import search
from google import genai
import concurrent.futures
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.table import Table, box
import trafilatura

console = Console()

# Prompt user for API key if not found in environment variables
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    GEMINI_API_KEY = console.input("[bold red]🚨 Enter your Gemini API Key: [/]")
    os.environ["GEMINI_API_KEY"] = GEMINI_API_KEY  # Store for current session

client = genai.Client(api_key=GEMINI_API_KEY)  # Initialize client

def perform_web_search(query, num_results=10):
    try:
        search_results_generator = search(query, num_results=num_results, advanced=True)
        valid_results = [
            result for result in search_results_generator
            if result.title and result.description and result.url
        ]
        return valid_results
    except Exception as e:
        console.print(f"[dim red]🔍 Search error: {e}[/]")
        return []

def get_web_content(url, timeout=10):
    """Fetch and extract content from a webpage using Trafilatura with timeout."""
    try:
        response = requests.get(url, timeout=timeout)
        response.raise_for_status()
        downloaded = response.text
        if downloaded:
            text = trafilatura.extract(downloaded)
            return text if text else f"[dim yellow]Trafilatura could not extract text from {url} 🚫[/]"
        else:
            return f"[dim yellow]Trafilatura could not download content from {url} 🚫[/]"
    except requests.exceptions.Timeout:
        return f"[dim yellow]Request timed out for {url} after {timeout} seconds ⏳[/]"
    except requests.exceptions.RequestException as e:
        return f"[dim yellow]Error fetching content from {url}: {e} ⚠️[/]"
    except Exception as e:
        return f"[dim yellow]Error processing content from {url}: {e} ⚠️[/]"

def summarize_content(text, max_length=2000):
    return text[:max_length] + ("..." if len(text) > max_length else "") if text else "No content available."

def generate_system_prompt(query, search_results, website_contents):
    search_results_formatted = "\n".join(
        f"[{i+1}] {result.title}\n{result.description}\n{result.url}"
        for i, result in enumerate(search_results)
    )

    website_contents_formatted = "\n".join(
        f"[Content {i+1}]\n{summarize_content(content)}"
        for i, content in enumerate(website_contents) if not content.startswith("[dim yellow]")
    )

    return f"""User's Query: {query}
Query's Search Results: {search_results_formatted}
Website Contents: {website_contents_formatted}
"""

def main():
    console.print(Panel(f"[bold cyan]🚀 Perplexity CLI[/] ✨\n🤖 Simple search and AI tool."))

    while True:
        query = console.input("[bold yellow]🤔 Query: [/]")
        if not query:
            continue
        if query.lower() == "exit":
            console.print("👋 Exiting... 👋")
            break

        with console.status("[bold blue]🔍 Searching the web..."):
            search_results = perform_web_search(query, num_results=10)

        if not search_results:
            console.print("[dim yellow]🚫 No search results found. Please try a different query. 🧐[/]")
            continue

        results_table = Table(show_header=True, box=box.ROUNDED)
        results_table.add_column("#", style="cyan", width=3)
        results_table.add_column("Title", style="bold")
        results_table.add_column("URL", style="blue")
        for i, result in enumerate(search_results[:10]):
            results_table.add_row(str(i+1), result.title, result.url)
        console.print(Panel(results_table, title="🔍 Search Results", border_style="blue", padding=1))

        top_website_urls = [result.url for result in search_results[:3] if result.url]
        website_contents = []
        fetched_count = 0
        max_fetch_attempts = 3

        with console.status("[bold blue]🌍 Fetching website content..."):
            with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
                future_to_url = {executor.submit(get_web_content, url): url for url in top_website_urls}
                for future in concurrent.futures.as_completed(future_to_url):
                    if fetched_count >= max_fetch_attempts:
                        break
                    url = future_to_url[future]
                    try:
                        content = future.result()
                        if not content.startswith("[dim yellow]"):
                            website_contents.append(content)
                            fetched_count += 1
                        else:
                            website_contents.append(content)
                    except Exception as exc:
                        website_contents.append(f"Error fetching {url}: {exc}")

        if fetched_count == 0:
            console.print("[dim yellow]⚠️ Failed to fetch website content within timeout. Proceeding with search results only. ⏳[/]")
            prompt = generate_system_prompt(query, search_results[:10], [])
        else:
            prompt = generate_system_prompt(query, search_results[:3], website_contents)

        with console.status("[bold blue]🧠 Generating AI response..."):
            try:
                sys_instruct = (
                    "You are a genius AI search assistant. You can answer user queries concisely and accurately "
                    "using the provided user's local search results and website content. Format your responses in Markdown "
                    "for terminal output, using bullet points or numbered lists to organize information. Cite sources using "
                    "markdown links like for example: Your response: The current local time in New Delhi, India is "
                    "[12:07 PM](time.is) on [Tuesday, February 18, 2025](url2)."
                )
                response = client.models.generate_content(
                    model="gemini-2.0-flash-lite-preview-02-05",
                    config=genai.types.GenerateContentConfig(system_instruction=sys_instruct),
                    contents=[prompt]
                )
                ai_response_text = response.text if response and response.text else "[dim yellow]⚠️ AI Response was empty.[/dim yellow] Please try again."
            except Exception as e:
                ai_response_text = f"[dim red]🤖 AI Response Error:[/dim red] {e} ⚠️"

        console.print(Panel(Markdown(ai_response_text), title="💡 AI Response", border_style="green", padding=1))
        console.print("-- ✨ --" * (console.width // 8))

if __name__ == "__main__":
    main()
