import torch, torch.nn as nn
from transformers import AutoTokenizer, AutoModel, AutoImageProcessor, ViTModel

class TinyBaseline(nn.Module):
    def __init__(self, num_labels=3):
        super().__init__()
        self.tok = AutoTokenizer.from_pretrained("prajjwal1/bert-tiny")
        self.text = AutoModel.from_pretrained("prajjwal1/bert-tiny")
        self.imgp = AutoImageProcessor.from_pretrained("hf-internal-testing/tiny-random-vit")
        self.vision = ViTModel.from_pretrained("hf-internal-testing/tiny-random-vit")

        # freeze backbones
        for p in self.text.parameters(): p.requires_grad = False
        for p in self.vision.parameters(): p.requires_grad = False

        d_text = self.text.config.hidden_size      # ~128
        d_vis  = self.vision.config.hidden_size    # tiny (e.g., 32)
        self.proj_v = nn.Linear(d_vis, d_text)
        self.head = nn.Linear(d_text + d_text, num_labels)

    def encode_text(self, batch_text):
        enc = self.tok(batch_text, padding=True, truncation=True, return_tensors="pt")
        # use no_grad (not inference_mode) so outputs can be saved for backward in later layers
        with torch.no_grad():
            out = self.text(**enc).last_hidden_state[:, 0, :]  # [CLS]
        return out  # requires_grad=False, but a normal tensor

    def encode_img(self, imgs):
        pix = self.imgp(images=imgs, return_tensors="pt")
        with torch.no_grad():
            out = self.vision(**pix).last_hidden_state[:, 0, :]  # [CLS]
        return out  # requires_grad=False, but a normal tensor

    def forward(self, batch_text, imgs):
        t = self.encode_text(batch_text)           # (B, d_text)
        v = self.encode_img(imgs)                  # (B, d_vis)
        v = self.proj_v(v)                         # (B, d_text) — trainable
        z = torch.cat([t, v], dim=-1)              # (B, 2*d_text)
        return self.head(z)                        # (B, num_labels)
