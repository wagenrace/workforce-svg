from object_describer import ObjectDescriber
from svg_creator import SvgGenerator
from pathlib import Path

output_dir = Path("output")
output_dir.mkdir(exist_ok=True)


def save_output(svg_code, image, i):
    output_dir_with_index = output_dir / f"output_{str(i).zfill(3)}"
    if i > 0:
        prev_page_url = output_dir / f"output_{str(i - 1).zfill(3)}" / "index.html"
    else:
        prev_page_url = "/"
    next_page_url = output_dir / f"output_{str(i + 1).zfill(3)}" / "index.html"
    output_dir_with_index.mkdir(exist_ok=True)

    with open(output_dir_with_index / "index.html", "w") as f:
        f.write(
            f"""
    <!DOCTYPE html>
    <body>
        {svg_code}
        <button onclick="window.location.href = '{prev_page_url}';">Previous</button>
        <button onclick="window.location.href = '{next_page_url}';">Next</button>
    </body>
    """
        )

    image_path = output_dir_with_index / "output.png"
    with open(image_path, "wb") as f:
        f.write(image)

    return image_path


object_describer = ObjectDescriber()
svg_generator = SvgGenerator()

object_target = "Gear"
svg_code, png_image = svg_generator.generate(
    f"""
Draw a {object_target}.
<svg xmlns="http://www.w3.org/2000/svg" version="1.1" width="512" height="512"></svg>
"""
)

for i in range(1):
    image_path = save_output(svg_code, png_image, i)

    feedback = object_describer.generate_feedback(object_target, image_path)
    print(feedback)
