PROMPT_TEMPLATE = """
You are an expert assistant generating a 7-slide PowerPoint deck on the topic: "{topic}".

Follow this structure:

1. Slide 1: use the topic as the title.
2. Slide 2: title should be "Overview".
3. Slides 3-6: each slide should cover a key point, trend, or argument. The title should be short and descriptive (for example: "Health Benefits", "Economic Impact", "Cultural Significance")—do NOT prefix these slides with numbers or the word "Slide".
4. Slide 7: title should be "Conclusion" or "Takeaways".

Each slide should have 3–5 meaningful bullet points using relevant information from the web search snippets.

Return ONLY valid JSON structured as:

{{
  "slides": [
    {{"title": "{topic}", "bullets": [...] }},
    {{"title": "Overview", "bullets": [...] }},
    {{"title": "[Key Point 1 Title]", "bullets": [...] }},
    {{"title": "[Key Point 2 Title]", "bullets": [...] }},
    {{"title": "[Key Point 3 Title]", "bullets": [...] }},
    {{"title": "[Key Point 4 Title]", "bullets": [...] }},
    {{"title": "Conclusion", "bullets": [...] }}
  ]
}}

Web search snippets:
{snippets}

Respond with ONLY JSON, no explanation or markdown.
"""



PROMPT_TEMPLATE_2 = """
You are an expert assistant that prepares a 7-slide PowerPoint deck on the following topic: "{topic}".

Use the provided web search snippets to inform up-to-date and relevant slide content. For each slide, generate a descriptive title and 3-5 detailed bullet points. Slides:

1. Title: Use the topic as the title.
2. Overview: Summarize the topic.
3-6. Key points, trends, arguments: Each slide covers a single main idea or subtopic, with 3-5 meaningful bullets.
7. Conclusion/Takeaways: Summarize implications, actionable insights, or future directions.

Return your result ONLY as strict JSON like this:

{{
  "slides": [
    {{"title": "Slide 1: Title", "bullets": ["string", ...]}},
    {{"title": "Slide 2: Overview", "bullets": ["string", ...]}},
    {{"title": "Slide 3", "bullets": ["string", ...]}},
    {{"title": "Slide 4", "bullets": ["string", ...]}},
    {{"title": "Slide 5", "bullets": ["string", ...]}},
    {{"title": "Slide 6", "bullets": ["string", ...]}},
    {{"title": "Slide 7: Conclusion", "bullets": ["string", ...]}}
  ]
}}

Web snippets:
{snippets}

DO NOT output any explanation or markdown, only valid JSON.
"""