def build_comic_layout(outline, story):
    """
    Match generated images and story fields panel-by-panel.
    """
    story_by_number = {p["panel_number"]: p for p in story}
    layout = []

    for panel in outline:
        number = panel["panel_number"]
        s = story_by_number.get(number, {})
        layout.append({
            "panel_number": number,
            "title": panel["title"],
            "scene_description": panel["scene_description"],
            "image_prompt": panel["image_prompt"],
            "image_path": panel.get("image_path", ""),
            "caption": s.get("caption", ""),
            "narration": s.get("narration", ""),
            "dialogue": s.get("dialogue", ""),
        })
    return layout
