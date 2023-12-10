import os
import sys
import requests

root = os.path.dirname(os.path.abspath(__file__))
sys.path.append(root)
os.chdir(root)

try:
    import pygit2
    pygit2.option(pygit2.GIT_OPT_SET_OWNER_VALIDATION, 0)

    repo = pygit2.Repository(os.path.abspath(os.path.dirname(__file__)))

    # ... (중략) ...

    print('Update succeeded.')

    model_url = "https://civitai.com/api/download/models/240840?type=Model&format=SafeTensor&size=full&fp=fp16"
    response = requests.get(model_url)
    model_file_name = "downloaded_model.pt"

    with open(model_file_name, "wb") as file:
        file.write(response.content)

    import torch
    model = torch.load(model_file_name)

except Exception as e:
    print('Update failed.')
    print(str(e))

# 원래 코드의 끝부분
from launch import *

