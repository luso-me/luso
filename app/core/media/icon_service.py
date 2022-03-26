import hashlib
import random

import svgwrite


class IconService:
    def __init__(self):
        pass

    def _get_acronym(self, text: str):
        text_parts = text.split(" ")
        acronym = ""
        for part in text_parts:
            acronym += part[0].upper()

        return acronym

    def _generate_colour(self, text: str):

        hash_str = str(int(hashlib.sha1(text.encode("utf-8")).hexdigest(), 16))
        colour_str = hash_str[-9:]

        return tuple(int(colour_str[(3 * i) : (3 * (i + 1))]) % 255 for i in range(3))

    def generate_icon(self, text: str):
        if not text:
            raise ValueError("Text empty")
        colour = self._generate_colour(text)

        text = self._get_acronym(text)

        text_size = len(text)

        base_size = 40
        width = base_size * text_size
        height = base_size * 2

        dwg = svgwrite.Drawing("test.svg", (width, height), debug=True)
        dwg.add(
            dwg.rect(
                insert=(0, 0),
                size=(width, height),
                rx=0,
                ry=0,
                fill=f"rgb(255,255,255)",
                fill_opacity="0.1",
            )
        )
        dwg.add(
            dwg.text(
                text,
                ("50%", "50%"),
                font_size=20,
                text_anchor="middle",
                dy=[".33em"],
                fill=f"rgb({colour[0]},{colour[1]},{colour[2]})",
            )
        )

        dwg.save()
