import jsonschema
from jsonschema import validate
from rich.console import Console

console = Console()

# Modified schema: 'bullets' is optional (not required) for all slides
SLIDES_SCHEMA = {
    "type": "object",
    "properties": {
        "slides": {
            "type": "array",
            "minItems": 7,
            "maxItems": 7,
            "items": {
                "type": "object",
                "properties": {
                    "title": {"type": "string"},
                    "bullets": {
                        "type": "array",
                        "items": {"type": "string"}
                        # Removed minItems here to allow empty or missing bullets
                    }
                },
                "required": ["title"],  # Only require title, bullets optional here
                "additionalProperties": True
            }
        }
    },
    "required": ["slides"]
}

def validate_slides_json(data: dict) -> bool:
    """
    Returns True if JSON passes schema validation and bullets present on slides 2-7.
    """
    try:
        validate(instance=data, schema=SLIDES_SCHEMA)
        slides = data.get("slides", [])
        # Custom check: slides 2-7 must have at least one bullet
        for i, slide in enumerate(slides[1:], start=2):  # Ignore slide 1 (title slide)
            bullets = slide.get("bullets")
            if not isinstance(bullets, list) or len(bullets) == 0:
                return False
        return True
    except jsonschema.ValidationError:
        return False

def repair_slides_json(data: dict) -> dict:
    """
    Attempts to repair slide JSON:
    - Ensures exactly 7 slides, each with title.
    - Adds placeholder bullets if missing or empty.
    - Adds placeholder title if missing or empty.
    """
    slides = data.get("slides", [])

    # Truncate if more than 7 slides
    if len(slides) > 7:
        slides = slides[:7]

    # Add placeholder slides if fewer than 7
    while len(slides) < 7:
        slides.append({
            "title": f"Slide {len(slides) + 1}",
            "bullets": ["Content not provided"]
        })

    # Ensure all slides have title and bullets (except bullets can be empty on slide 1)
    for i, slide in enumerate(slides):
        if "title" not in slide or not isinstance(slide["title"], str) or not slide["title"].strip():
            slide["title"] = f"Slide {i + 1}"
        bullets = slide.get("bullets")
        if i == 0:
            # Slide 1 (title): allow empty bullets; add placeholder if None type
            if bullets is None:
                slide["bullets"] = ["Introduction to the topic."]
        else:
            # Slides 2-7: ensure non-empty bullets list
            if not isinstance(bullets, list) or len(bullets) == 0:
                slide["bullets"] = ["Content not provided"]

    data["slides"] = slides
    return data

def safe_validate_and_repair(data: dict) -> dict:
    """
    Validates against schema and custom bullet checks.
    Repairs JSON if invalid, then validates repaired JSON before returning.
    """
    try:
        validate(instance=data, schema=SLIDES_SCHEMA)
        if validate_slides_json(data):
            return data
        else:
            console.print("[yellow]Bullets missing in some slides; repairing slides data...[/yellow]")
            repaired = repair_slides_json(data)
            assert validate_slides_json(repaired)
            return repaired
    except jsonschema.ValidationError:
        console.print("[yellow]JSON schema validation failed; repairing slides data...[/yellow]")
        repaired = repair_slides_json(data)
        validate(instance=repaired, schema=SLIDES_SCHEMA)
        assert validate_slides_json(repaired)
        return repaired
