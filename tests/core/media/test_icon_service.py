import shutil

from app.core.media.icon_service import IconService


async def test_generate_icon():
    icon_service = IconService()
    with open("c.svg", "w") as outfile:
        icon = await icon_service.generate_icon("CS GO")
        icon.seek(0)

    assert icon
