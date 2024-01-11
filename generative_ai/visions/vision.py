from pathlib import Path
from generative_ai.visions import init_vision_model


def _process_ocr(image_object: str | bytes, mime_type: str) -> str:
    model = init_vision_model()
    images = [
        {
            "mime_type": "image/jpeg",
            "data": image_object
        },
    ]
    prompt = [
        "Extract complete text in the image(s) below:\n"
    ]
    for image in images:
        prompt.append(image)
    prompt.append("\nResponse: ")
    response = model.generate_content(prompt)
    return response.text


def ocr_file(file_name: str) -> str:
    if not (img := Path(file_name)).exists():
        raise FileNotFoundError(f"Could not find image: {img}")
    return _process_ocr(image_object=img.read_bytes(), mime_type="image/jpeg")


def ocr(b64_string: str) -> str:
    splits = b64_string.split(";base64,")
    b64_str = splits[1]
    mine_type = splits[0].replace("data:", "")
    return _process_ocr(image_object=b64_str, mime_type=mine_type)
