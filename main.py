import os
from dotenv import load_dotenv
from api_clients.web_search import search_web
from api_clients.llm_client import generate_slide_content
from slide_generator.pptx_builder import create_presentation
from utils.validation import validate_slides_json
from rich.prompt import Prompt
from rich.console import Console

import sys

print("Current working directory:", os.getcwd())
print("sys.path:", sys.path)


load_dotenv()
console = Console()


print("TAVILY_API_KEY:", os.getenv("TAVILY_API_KEY"))
print("OPENROUTER_API_KEY:", os.getenv("OPENROUTER_API_KEY"))

def main():
    console.print("[bold blue]Welcome to Auto Slide Deck Generator[/bold blue]")
    topic = Prompt.ask("Enter a topic for your presentation")
    console.print(f"[green]Searching the web for latest info on:[/green] {topic}")

    snippets = search_web(topic)
    if not snippets:
        console.print("[red]No search results found. Exiting.[/red]")
        return

    console.print(f"[green]Generating slide content using LLM...[/green]")
    slides_json = generate_slide_content(topic, snippets)

    if not slides_json:
        console.print("[red]Failed to generate slide content or invalid format returned.[/red]")
        return

    valid = validate_slides_json(slides_json)
    if not valid:
        console.print("[red]Generated slide content JSON did not pass validation.[/red]")
        return

    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)
    filename = f"{topic.replace(' ', '_')}.pptx"
    output_path = os.path.join(output_dir, filename)

    create_presentation(slides_json, output_path)
    console.print(f"[bold green]Slide deck created successfully at:[/bold green] {output_path}")


if __name__ == "__main__":
    main()
