import re

import ollama
from cairosvg import svg2png


class SvgGenerator:
    def __init__(self) -> None:
        base_model_name = "codellama"
        ollama.pull(base_model_name)

        modelfile = f"""
FROM {base_model_name}
SYSTEM You create an SVG of the input. You only return the SVG.
        """
        print(modelfile)
        self.svg_model_name = "svg_maker"
        ollama.create(model=self.svg_model_name, modelfile=modelfile)

    def generate(self, input_message: str, output_name: str = "output.png"):
        result = ollama.chat(
            model=self.svg_model_name,
            messages=[{"role": "user", "content": input_message}],
        )

        print(result)

        # Example text with SVG elements
        text = result["message"]["content"].replace("\n", "")
        text = '<div><p>Hello, world!</p><svg width="100" height="100"><rect x="10" y="10" width="80" height="80" style="fill:rgb(0,0,255);stroke-width:3;stroke:rgb(0,0,0)"/></svg></div>'

        # Find all SVG elements in the text
        svg_code = re.findall(r"<svg.*?</svg>", text)[0]

        svg2png(bytestring=svg_code, write_to=output_name)


if __name__ == "__main__":
    svg_generator = SvgGenerator()
    svg_generator.generate("gear", "output.png")
