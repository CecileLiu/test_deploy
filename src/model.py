# from turtle import back
from typing import Union, List, Dict
from tqdm import tqdm
import torch
from transformers import (
    pipeline,
    TFAutoModelForSequenceClassification,
    AutoTokenizer,
    AutoModelForSequenceClassification,
)
from preprocessing import preprocess



class TextClassifier:
    def __init__(self, model_path: str):
        """Text classification inference for pretrained transformers models

        Args:
            model_path (str): path to model. e.g.
            backend (str, optional): model backend, available options are "pt" or "tf". Defaults to "pt".
        """

        self.model = AutoModelForSequenceClassification.from_pretrained(model_path)
        self.tokenizer = AutoTokenizer.from_pretrained(model_path)
        self.pipeline = pipeline(
            "text-classification",
            model=self.model,
            tokenizer=self.tokenizer,
            return_all_scores=True,
            device=0 if torch.cuda.is_available() else -1,
        )

    @staticmethod
    def _batch(text: List[str], bs: int = 64) -> Dict[str, List[str]]:
        l = len(text)
        for ndx in range(0, l, bs):
            yield text[ndx : min(ndx + bs, l)]

    def predict(self, text: Union[str, List[str]], bs: int = 64) -> List[Dict]:
        if isinstance(text, str):
            text = preprocess(text)
            try:
                return self.pipeline(text)
            except:
                return [{"label": "unknown", "score": 0.0}]
        else:
            text = list(map(preprocess, text))
            result = []
            for batch in tqdm(self._batch(text, bs)):
                try:
                    out = self.pipeline(batch)
                    result.extend(out)
                except:
                    # potential special characters may break the pipeline.
                    # skip the batch for now
                    pass
            return result
