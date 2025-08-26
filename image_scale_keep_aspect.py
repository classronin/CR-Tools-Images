import torch
import numpy as np
from PIL import Image
import comfy.utils

class 图像等比缩放器:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "图像": ("IMAGE",),
                "宽度": ("INT", {"default": 0, "min": 0}),
                "高度": ("INT", {"default": 0, "min": 0}),
            },
            "optional": {
                "遮罩": ("MASK",), 
            }
        }

    RETURN_TYPES = ("IMAGE", "MASK")
    RETURN_NAMES = ("图像", "遮罩")
    FUNCTION = "resize_image"
    CATEGORY = "⚙️CR工具"

    def resize_image(self, 图像, 宽度, 高度, 遮罩=None):
        if 宽度 == 0 and 高度 == 0:
            return (图像, 遮罩)

        orig_h = 图像.shape[1]
        orig_w = 图像.shape[2]

        if 宽度 == 0:
            scale = 高度 / orig_h
            new_w = int(orig_w * scale)
            new_h = 高度
        elif 高度 == 0:
            scale = 宽度 / orig_w
            new_w = 宽度
            new_h = int(orig_h * scale)
        else:
            scale_w = 宽度 / orig_w
            scale_h = 高度 / orig_h
            scale = min(scale_w, scale_h)
            new_w = int(orig_w * scale)
            new_h = int(orig_h * scale)

        if new_w <= 0 or new_h <= 0:
            raise ValueError("调整后的宽度和高度必须大于0")

        pil_images = []
        for img in 图像:
            img_np = img.cpu().numpy()
            if img_np.dtype != np.uint8:
                img_np = (img_np * 255).astype(np.uint8)
            pil_img = Image.fromarray(img_np, mode='RGB')
            pil_resized = pil_img.resize((new_w, new_h), Image.LANCZOS) # 或者 Image.BILINEAR
            pil_images.append(pil_resized)

        output_images = []
        for pil_img in pil_images:
            img_array = np.array(pil_img).astype(np.float32) / 255.0
            output_images.append(torch.from_numpy(img_array))

        if output_images:
            final_image = torch.stack(output_images, dim=0)
        else:
            final_image = 图像 

        final_mask = 遮罩
        if 遮罩 is not None:
            try:
                mask_pils = []
                for m in 遮罩:
                    m_np = m.cpu().numpy()
                    if m_np.dtype != np.uint8:
                        m_np = (m_np * 255).astype(np.uint8)
                    mask_pil = Image.fromarray(m_np.squeeze(), mode='L') 
                    mask_resized = mask_pil.resize((new_w, new_h), Image.NEAREST)
                    mask_pils.append(mask_resized)

                mask_arrays = []
                for mask_pil in mask_pils:
                    mask_array = np.array(mask_pil).astype(np.float32) / 255.0
                    mask_arrays.append(torch.from_numpy(mask_array).unsqueeze(0)) 

                if mask_arrays:
                    final_mask = torch.cat(mask_arrays, dim=0)
                else:
                    final_mask = 遮罩
            except Exception as e:
                print(f"调整遮罩尺寸时出错: {e}")
                pass

        return (final_image, final_mask)

NODE_CLASS_MAPPINGS = {
    "🖼️图像等比缩放器": 图像等比缩放器,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "🖼️图像等比缩放器": "图像等比缩放器"
}