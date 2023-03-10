import torch
import torchvision
import torchvision.transforms as transforms
import torch.nn as nn
import torch.nn.functional as F
import torchvision.models as models
from urllib.request import urlopen
from PIL import Image
import numpy as np
import json
import sys

from torchvision.models import ResNet18_Weights


def model():
    model = models.resnet18(weights=ResNet18_Weights.DEFAULT)
    model.eval()
    return model


def process(model, url):
    try:
        img = Image.open(url)
        img_tensor = transforms.ToTensor()(img).unsqueeze_(0)
        outputs = model(img_tensor)
        _, predicted = torch.max(outputs.data, 1)
        with open('./imagenet-labels.json') as f:
            labels = json.load(f)
        result = labels[np.array(predicted)[0]]
        img_name = url.split("/")[-1]
        save_name = f"{img_name},{result}"
        return json.dumps({"Key": img_name, "Result": result}), True
    except Exception as e:
        print(e)
        return e, False


if __name__ == "__main__":
    model = model()
    url = str(sys.argv[1])
    print(process(model, url))
