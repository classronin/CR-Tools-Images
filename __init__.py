import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

from .image_scale_keep_aspect import NODE_CLASS_MAPPINGS as IMAGE_RESIZE_MAPPINGS
from .image_size_selector import NODE_CLASS_MAPPINGS as ASPECT_RATIO_MAPPINGS

NODE_CLASS_MAPPINGS = {
    **IMAGE_RESIZE_MAPPINGS,
    **ASPECT_RATIO_MAPPINGS,
}

NODE_DISPLAY_NAME_MAPPINGS = {}
NODE_DISPLAY_NAME_MAPPINGS.update(getattr(IMAGE_RESIZE_MAPPINGS, 'NODE_DISPLAY_NAME_MAPPINGS', {}))
NODE_DISPLAY_NAME_MAPPINGS.update(getattr(ASPECT_RATIO_MAPPINGS, 'NODE_DISPLAY_NAME_MAPPINGS', {}))

__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS']