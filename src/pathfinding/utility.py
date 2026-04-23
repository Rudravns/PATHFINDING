import pygame
from typing import Optional, Tuple

def quick_quit():
    pygame.quit()
    exit()

_font_cache = {}
def render_text(
        text: str,
        position,
        size: int = 50,
        color = "#FFFFFFFF",
        font: Optional[pygame.font.Font] = None,
        bold: bool = False,
        italic: bool = False,
        underline: bool = False,
        draw: bool = True,
        surface: Optional[pygame.Surface] = None,
        center: bool = False,
) -> Tuple[pygame.Surface, pygame.Rect]:
    """Render text to the active display surface."""

    if surface:
        screen = surface
    else:
        screen = pygame.display.get_surface()

    if screen is None and draw:
        raise RuntimeError("Display surface not initialized. Call pygame.display.set_mode().")

    # Create font if none provided
    if font is None:
        key = ("Arial", int((size)))
        if key not in _font_cache:
            _font_cache[key] = pygame.font.SysFont("Arial", int((size)))
        font = _font_cache[key]

    # Convert color string to pygame.Color
    if isinstance(color, str):
        color = pygame.Color(color)  # type: ignore

    # Apply font styles
    font.set_bold(bold) # pyright: ignore[reportOptionalMemberAccess]
    font.set_italic(italic) # pyright: ignore[reportOptionalMemberAccess]
    font.set_underline(underline)   # pyright: ignore[reportOptionalMemberAccess]

    # Render text
    text_surface = font.render(str(text), True, color) # pyright: ignore[reportOptionalMemberAccess]
    text_rect = text_surface.get_rect(topleft=(position)) if not center else text_surface.get_rect(center=(position))

    if draw:
        screen.blit(text_surface, text_rect) # pyright: ignore[reportOptionalMemberAccess]

    return text_surface, text_rect
