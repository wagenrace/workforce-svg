import re

import ollama
import cairosvg


class SvgGenerator:
    def __init__(self) -> None:
        base_model_name = "codellama"
        ollama.pull(base_model_name)

        modelfile = f"""
FROM {base_model_name}
SYSTEM Improve the SVG based on the input. Only work with x and y coordinates. The width and height of the SVG should be 512x512. You only return the SVG.
        """
        print(modelfile)
        self.svg_model_name = "svg_maker"
        ollama.create(model=self.svg_model_name, modelfile=modelfile)

    def generate(self, input_message: str):
        result = ollama.chat(
            model=self.svg_model_name,
            messages=[{"role": "user", "content": input_message}],
        )

        print(result["message"]["content"])

        # Example text with SVG elements
        text = result["message"]["content"].replace("\n", "")

        # Find all SVG elements in the text
        try:
            svg_code = re.findall(r"<svg.*?</svg>", text)[0]
            # Convert SVG code to PNG image
            png_data = cairosvg.svg2png(bytestring=svg_code)
        except:
            print("Error in SVG code. Lets try again.")
            svg_code, png_data = self.generate(input_message)
        # Save the PNG image to a file
        return svg_code, png_data


if __name__ == "__main__":
    svg_generator = SvgGenerator()
    svg_code, png_data = svg_generator.generate(
        """
Draw a gear.
<svg xmlns="http://www.w3.org/2000/svg" version="1.1" width="512" height="512"></svg>
"""
    )
    print("\n===result===")
    print(svg_code)
    with open("output.png", "wb") as f:
        f.write(png_data)
