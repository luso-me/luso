from app.core.media.icon_service import IconService


def test_generate_icon():
    icon_service = IconService()
    icon_service.generate_icon("C")
