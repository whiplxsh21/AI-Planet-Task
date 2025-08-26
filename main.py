from dotenv import load_dotenv
load_dotenv()

import os
from rich.console import Console
from api_clients.web_search import search_web
from api_clients.image_search import search_unsplash_image, download_image
from api_clients.llm_client import generate_slide_content
from utils.validation import safe_validate_and_repair
from slide_generator.pptx_builder import create_presentation, get_style_dict

def main():
    console = Console()
    styles = get_style_dict()
    console.print("[bold]Available styles:[/bold]")
    for k in styles:
        console.print(f"- {k}")
    chosen_style = input("Choose a style: ").strip().lower()
    if chosen_style not in styles:
        chosen_style = "blue"

    topic = input("Enter a topic for your presentation: ").strip()

    # Fetch and download image for the title slide
    image_url = search_unsplash_image(topic)
    image_path = None
    if image_url:
        os.makedirs("output", exist_ok=True)
        image_path = f"output/title_image.jpg"
        download_image(image_url, image_path)

    # Web search and LLM slide content generation
    snippets = search_web(topic)
    slides_json = generate_slide_content(topic, snippets)

    # Defensive check if generation failed
    if slides_json is None:
        console.print("[red]Failed to generate slide content. Exiting.[/red]")
        return

    # Validate and repair slide JSON to match schema
    slides_json = safe_validate_and_repair(slides_json)

    # Prepare output file path
    safe_topic = topic.replace(" ", "_")
    output_file = f"output/{safe_topic}.pptx"

    # Create and save the PowerPoint presentation with chosen style and image
    create_presentation(slides_json, output_file, chosen_style, title_image_path=image_path)

    console.print(f"[green]Slide deck saved: {output_file}[/green]")

if __name__ == "__main__":
    main()
