import jsonschema
from jsonschema import validate

SLIDES_SCHEMA = {
    "type": "object",
    "properties": {
        "slides": {
            "type": "array",
            "minItems": 7,
            "maxItems": 7,
            "prefixItems": [
                {  # Slide 1 (title slide)
                    "type": "object",
                    "properties": {
                        "title": {"type": "string"},
                        "bullets": {
                            "type": "array",
                            "items": {"type": "string"},
                            "minItems": 0
                        },
                        "image_url": {"type": "string"},
                    },
                    "required": ["title"],
                    "additionalProperties": True,
                }
            ] + [
                {  # Slides 2-7 (key slides)
                    "type": "object",
                    "properties": {
                        "title": {"type": "string"},
                        "bullets": {
                            "type": "array",
                            "items": {"type": "string"},
                            "minItems": 1,
                        },
                    },
                    "required": ["title", "bullets"],
                    "additionalProperties": True,
                }
            ] * 6,
            "items": False  # no additional items beyond prefixItems
        }
    },
    "required": ["slides"]
}


def validate_slides_json(data: dict) -> bool:
    try:
        validate(instance=data, schema=SLIDES_SCHEMA)
        slides = data.get("slides", [])
        for i, slide in enumerate(slides[1:], start=2):  # slides 2-7
            bullets = slide.get("bullets")
            if not isinstance(bullets, list) or len(bullets) == 0:
                return False
        return True
    except jsonschema.ValidationError:
        return False

def repair_slides_json(data: dict) -> dict:
    slides = data.get("slides", [])
    if len(slides) > 7:
        slides = slides[:7]
    while len(slides) < 7:
        slides.append({
            "title": f"Slide {len(slides) + 1}",
            "bullets": ["Content not provided"]
        })
    for i, slide in enumerate(slides):
        if "title" not in slide or not isinstance(slide["title"], str) or not slide["title"].strip():
            slide["title"] = f"Slide {i + 1}"
        bullets = slide.get("bullets")
        if i == 0 and bullets is None:
            slide["bullets"] = ["Introduction to the topic."]
        elif i > 0 and (not isinstance(bullets, list) or len(bullets) == 0):
            slide["bullets"] = ["Content not provided"]
    data["slides"] = slides
    return data

def safe_validate_and_repair(data: dict) -> dict:
    # Try to validate and repair as needed
    from rich.console import Console
    console = Console()
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
