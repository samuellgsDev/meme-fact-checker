from PIL import Image
import io

def resize_image(image_bytes: bytes, max_dimension: int = 1024) -> bytes:
    """
    Resizes an image to a maximum dimension while maintaining aspect ratio.
    """
    img = Image.open(io.BytesIO(image_bytes))
    
    # Convert to RGB if necessary (e.g. for PNGs with transparency)
    if img.mode in ('RGBA', 'P'):
        img = img.convert('RGB')
        
    width, height = img.size
    if max(width, height) > max_dimension:
        scale_factor = max_dimension / max(width, height)
        new_width = int(width * scale_factor)
        new_height = int(height * scale_factor)
        img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
        
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format='JPEG', quality=85)
    return img_byte_arr.getvalue()
    
