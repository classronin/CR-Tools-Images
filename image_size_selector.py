import torch
import numpy as np
from PIL import Image

class 图像尺寸选择器:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "宽度": ("INT", {"default": 320, "min": 16, "max": 2048}),
                "高度": ("INT", {"default": 704, "min": 16, "max": 2048}),
                "图像尺寸选择器": ("BOOLEAN", {
                "default": True,
                "label_on": "启用",
                "label_off": "禁用"
            }),
                "预设尺寸": ([
                    "320x704",
                    "384x640",
                    "448x576",
                    "512x512",
                    "576x448",
                    "640x384",
                    "704x320"
                ], {"default": "320x704"}),
            },
            "optional": {
                "图像": ("IMAGE",), 
            }
        }

    RETURN_TYPES = ("INT", "INT")
    RETURN_NAMES = ("宽度", "高度")
    FUNCTION = "get_dimensions"
    CATEGORY = "⚙️CR工具"

    def get_dimensions(self, 宽度, 高度, 图像尺寸选择器, 预设尺寸, 图像=None):

        if 图像 is not None and len(图像) > 0:
            h = 图像.shape[1]
            w = 图像.shape[2]
            return (w, h)

        if 图像尺寸选择器:
            ratio_map = {
                "320x704": (320, 704),
                "384x640": (384, 640),
                "448x576": (448, 576),
                "512x512": (512, 512),
                "576x448": (576, 448),
                "640x384": (640, 384),
                "704x320": (704, 320)
            }
            preset_width, preset_height = ratio_map.get(预设尺寸, (宽度, 高度))
            return (preset_width, preset_height)
        else:
            return (宽度, 高度)

NODE_CLASS_MAPPINGS = {
    "📋图像尺寸选择器": 图像尺寸选择器,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "📋图像尺寸选择器": "图像尺寸选择器"
}