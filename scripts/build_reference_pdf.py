from pathlib import Path

from PIL import Image
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas


ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"
OUTPUT = ROOT / "output" / "pdf" / "reference-paper.pdf"


def main() -> None:
    page_images = [ASSETS / f"reference-paper-page-{index}.png" for index in range(1, 7)]
    missing = [str(path) for path in page_images if not path.is_file()]
    if missing:
        raise FileNotFoundError(f"Missing reference paper pages: {missing}")

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    pdf = canvas.Canvas(str(OUTPUT), pageCompression=1)

    for image_path in page_images:
        with Image.open(image_path) as image:
            width, height = image.size
        pdf.setPageSize((width, height))
        pdf.drawImage(ImageReader(str(image_path)), 0, 0, width=width, height=height)
        pdf.showPage()

    pdf.save()
    print(f"Created {OUTPUT}")


if __name__ == "__main__":
    main()
