import ollama


class ObjectDescriber:
    def __init__(self) -> None:
        base_model_name = "llava"
        ollama.pull(base_model_name)

        modelfile = f"""
FROM {base_model_name}
SYSTEM How can we modify the design of the image to make it resemble the input? Give your result as a list of commands.
        """
        print(modelfile)
        self.model_name = "object_describer"
        ollama.create(model=self.model_name, modelfile=modelfile)

    def generate_feedback(self, input_message: str, image_path: str):
        result = ollama.chat(
            model=self.model_name,
            messages=[
                {
                    "role": "user",
                    "content": f"How to make this image look more like {input_message}",
                    "images": [image_path],
                }
            ],
        )

        return result["message"]["content"]


if __name__ == "__main__":
    object_describer = ObjectDescriber()
    feedback = object_describer.generate_feedback("Gear", "circle.png")
    print(feedback)
