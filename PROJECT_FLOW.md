# ComicCraft Project Flow

1. User opens `/`.
2. `index.html` collects:
   - Story Prompt
   - Character Name
   - Setting
   - Story Tone
   - Art Style
3. POST `/generate` receives form data.
4. `gemini_flash.generate_outline()` creates exactly five panels.
5. `gemini_pro.generate_story()` adds caption, narration and dialogue.
6. `image_generator.generate_image()` creates/saves one image for each panel.
7. `layout_builder.build_comic_layout()` matches text and images.
8. `exporters.save_pdf()` creates a multi-page PDF using FPDF.
9. `comic_preview.html` displays the generated comic.
10. User downloads the PDF.
11. `export_success.html` confirms completion.

## API JSON example

POST `/generate-comic/json`

```json
{
  "story_prompt": "A brave fox explores an enchanted forest.",
  "character_name": "Luna",
  "setting": "enchanted forest",
  "tone": "dramatic",
  "art_style": "comic book"
}
```
