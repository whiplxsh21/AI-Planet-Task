from pptx import Presentation
from pptx.util import Pt

def create_presentation(slides_json, output_file):
    prs = Presentation()
    title_slide_layout = prs.slide_layouts[0]
    content_slide_layout = prs.slide_layouts[1]

    for i, slide in enumerate(slides_json.get("slides", [])):
        if i == 0:
            sldr = prs.slides.add_slide(title_slide_layout)
            sldr.shapes.title.text = slide.get("title", "")
        else:
            sldr = prs.slides.add_slide(content_slide_layout)
            sldr.shapes.title.text = slide.get("title", "")

            # Find the first placeholder with a text frame (usually for content)
            content_placeholder = None
            for shape in sldr.shapes:
                if shape.is_placeholder and shape.has_text_frame and shape != sldr.shapes.title:
                    content_placeholder = shape
                    break

            # Fall back to the first shape with a text frame if placeholder not found
            if content_placeholder is None:
                for shape in sldr.shapes:
                    if shape.has_text_frame and shape != sldr.shapes.title:
                        content_placeholder = shape
                        break

            if content_placeholder:
                tf = content_placeholder.text_frame
                tf.clear()
                for bullet in slide.get("bullets", []):
                    p = tf.add_paragraph()
                    p.text = bullet
                    p.font.size = Pt(18)
            else:
                # If all else fails, add a box somewhere
                left, top, width, height = Pt(50), Pt(150), Pt(800), Pt(400)
                txBox = sldr.shapes.add_textbox(left, top, width, height)
                tf = txBox.text_frame
                for bullet in slide.get("bullets", []):
                    p = tf.add_paragraph()
                    p.text = bullet
                    p.font.size = Pt(18)

    prs.save(output_file)
