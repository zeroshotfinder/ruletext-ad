from pathlib import Path
from typing import List, Tuple, Any, Dict
from pydantic_ai import BinaryContent
from agent import AnomalyDetectionAgent
from PIL import Image
from prompts import text_prompts, system_prompt, objects_description
import io
from typing import List, Dict, Any, Set, Tuple

def resize_image(binary: BinaryContent, down_factor=2) -> str:
    """Redimensiona a imagem e retorna uma string base64."""
    image = Image.open(io.BytesIO(binary.data))
    image = image.convert("RGB")
    width, height = image.size
    # Calcular novas dimensões (metade do tamanho original)
    new_size = (width // down_factor, height // down_factor)
    image = image.resize(new_size)
    # print(image.size)
    buffer = io.BytesIO()
    image.save(buffer, format="PNG")
    return BinaryContent(buffer.getvalue(), media_type='image/png')

def read_bytes_image(image_path: Path) -> BinaryContent:
    return BinaryContent(data=Path(image_path).read_bytes(), media_type='image/png')
