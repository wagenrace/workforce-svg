import re

import ollama
import cairosvg


class SvgGenerator:
    def __init__(self) -> None:
        base_model_name = "codellama"
        ollama.pull(base_model_name)

        modelfile = f"""
FROM {base_model_name}
SYSTEM You create an SVG of the input. The width and height of the SVG should be 512x512. You only return the SVG. The SVG should be valid and not contain any malicious code.
        """
        print(modelfile)
        self.svg_model_name = "svg_maker"
        ollama.create(model=self.svg_model_name, modelfile=modelfile)

    def generate(self, input_message: str, output_name: str = "output.png"):
        result = ollama.chat(
            model=self.svg_model_name,
            messages=[{"role": "user", "content": input_message}],
        )

        print(result["message"]["content"])

        # Example text with SVG elements
        text = result["message"]["content"].replace("\n", "")

        # Find all SVG elements in the text
        svg_code = re.findall(r"<svg.*?</svg>", text)[0]
        # Convert SVG code to PNG image
        png_data = cairosvg.svg2png(bytestring=svg_code)

        # Save the PNG image to a file
        with open(output_name, "wb") as f:
            f.write(png_data)


if __name__ == "__main__":
    svg_generator = SvgGenerator()
    svg_generator.generate("gear", "output.png")
