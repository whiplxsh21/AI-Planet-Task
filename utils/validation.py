import jsonschema
from jsonschema import validate, ValidationError
from rich.console import Console

console = Console()

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
                {  # Slides 2-7 
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
        slide_num = len(slides) + 1
        if slide_num == 7:
            slides.append({
                "title": "Conclusion",
                "bullets": ["Content not provided"]
            })
        else:
            slides.append({
                "title": f"Slide {slide_num}",
                "bullets": ["Content not provided"]
            })

    if slides[6].get("title", "").lower() not in ["conclusion", "takeaways"]:
        slides[6]["title"] = "Conclusion"
        if not slides[6].get("bullets"):
            slides[6]["bullets"] = ["Content not provided"]


    for i, slide in enumerate(slides):
        if "title" not in slide or not isinstance(slide["title"], str) or not slide["title"].strip():
            slide["title"] = f"Slide {i + 1}"
        bullets = slide.get("bullets")
        if i == 0:
            if bullets is None:
                slide["bullets"] = ["Introduction to the topic."]
        else:
            if not isinstance(bullets, list) or len(bullets) == 0:
                slide["bullets"] = ["Content not provided"]

    data["slides"] = slides
    return data



def safe_validate_and_repair(data: dict) -> dict:
    """
    Validate slides JSON using jsonschema. If invalid or missing bullets, repair
    and return a guaranteed valid JSON as per your schema.
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
    except ValidationError as e:
        console.print(f"[yellow]JSON schema validation failed; repairing slides data...[/yellow]")
        repaired = repair_slides_json(data)
        validate(instance=repaired, schema=SLIDES_SCHEMA)
        assert validate_slides_json(repaired)
        return repaired
