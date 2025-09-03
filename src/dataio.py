import pandas as pd
from PIL import Image

class DemoDataset:
    def __init__(self, table_path):
        self.df = pd.read_parquet(table_path)
    def __len__(self):
        return len(self.df)
    def __getitem__(self, i):
        r = self.df.iloc[i]
        img = Image.open(r["image_path"]).convert("RGB")
        return {"text": r["text"], "target": r["target"], "image": img, "label": r["label"]}
