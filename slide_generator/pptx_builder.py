from pptx import Presentation
from pptx.util import Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
import os

def get_style_dict():
    return {
        "blue":  {"color": RGBColor(54, 95, 145), "font": "Calibri"},
        "green": {"color": RGBColor(34, 177, 76), "font": "Arial"},
        "orange": {"color": RGBColor(237, 125, 49), "font": "Tahoma"}
    }

def create_presentation(slides_json, output_file, style_name="blue", title_image_path=None):
    style = get_style_dict().get(style_name, get_style_dict()["blue"])
    prs = Presentation()
    title_slide_layout = prs.slide_layouts[0]
    content_slide_layout = prs.slide_layouts[1]

    for i, slide in enumerate(slides_json.get("slides", [])):
        if i == 0:
            sldr = prs.slides.add_slide(title_slide_layout)
            sldr.shapes.title.text = slide.get("title", "")
            title_shape = sldr.shapes.title

            # Add image under title if provided
            if title_image_path and os.path.exists(title_image_path):
                left = title_shape.left
                top = title_shape.top + title_shape.height + Pt(20)
                width = Pt(400)
                height = Pt(250)
                sldr.shapes.add_picture(title_image_path, left, top, width, height)
        else:
            sldr = prs.slides.add_slide(content_slide_layout)
            sldr.shapes.title.text = slide.get("title", "")
            content_placeholder = None
            for shape in sldr.shapes:
                if shape.is_placeholder and shape.has_text_frame and shape != sldr.shapes.title:
                    content_placeholder = shape
                    break
            if content_placeholder:
                tf = content_placeholder.text_frame
                tf.clear()
                for bullet in slide.get("bullets", []):
                    p = tf.add_paragraph()
                    p.text = bullet
                    p.font.size = Pt(18)
                    p.font.name = style["font"]
                    p.font.color.rgb = style["color"]
    prs.save(output_file)
