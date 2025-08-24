import open_clip
import torch
from PIL import Image

class FashionCLIPModel:
    def __init__(self):
        # see if the device has gpu for faster inference
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model_name = 'hf-hub:Marqo/marqo-fashionCLIP'
        # load the default model, tokenizer and input pre-processor
        self.model, _, self.processor = open_clip.create_model_and_transforms(self.model_name)
        # load the text custom tokenizer
        self.tokenizer = open_clip.get_tokenizer(self.model_name)
        self.model.to(self.device)      # set the device mode
        self.model.eval()               # switch to inferencing mode rather than training

    def pre_process_inputs(self, image: Image.Image, texts: list[str]):
        assert type(image) == Image.Image, "Input image should be a PIL Image"
        image = self.processor(image).unsqueeze(0).to(self.device)
        texts = self.tokenizer(texts).to(self.device)
        return image, texts

    def classify(self, image: Image.Image, labels: list[str]):
        image, text = self.pre_process_inputs(image, labels)
        # run inference
        with torch.no_grad():
            # get the embeddings of the input and labels
            img_features = self.model.encode_image(image, normalize=True)
            text_features = self.model.encode_text(text, normalize=True)

            # run cosine similarity comparision on image with the labels and turn similarity scores into probability using softmax
            similarity = (img_features @ text_features.T).softmax(dim=-1)
        # get the tensor index with max similarity and convert it to using .item() for best matching label extraction
        best_label = labels[similarity.argmax().item()]
        return best_label