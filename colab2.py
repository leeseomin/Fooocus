import os
import sys

# 라이브러리 설치 여부를 검사합니다
try:
    import pygit2
    import torch
    import requests
except ImportError as e:
    print(f"필요한 라이브러리가 설치되지 않았습니다: {e}")
    sys.exit(1)

root = os.path.dirname(os.path.abspath(__file__))
sys.path.append(root)
os.chdir(root)

try:
    pygit2.option(pygit2.GIT_OPT_SET_OWNER_VALIDATION, 0)
    repo = pygit2.Repository(os.path.abspath(os.path.dirname(__file__)))

    branch_name = repo.head.shorthand
    remote_name = 'origin'
    remote = repo.remotes[remote_name]
    remote.fetch()

    local_branch_ref = f'refs/heads/{branch_name}'
    local_branch = repo.lookup_reference(local_branch_ref)
    remote_reference = f'refs/remotes/{remote_name}/{branch_name}'
    remote_commit = repo.revparse_single(remote_reference)

    merge_result, _ = repo.merge_analysis(remote_commit.id)

    if merge_result & pygit2.GIT_MERGE_ANALYSIS_UP_TO_DATE:
        print("Already up-to-date")
    elif merge_result & pygit2.GIT_MERGE_ANALYSIS_FASTFORWARD:
        local_branch.set_target(remote_commit.id)
        repo.head.set_target(remote_commit.id)
        repo.checkout_tree(repo.get(remote_commit.id))
        repo.reset(local_branch.target, pygit2.GIT_RESET_HARD)
        print("Fast-forward merge")
    elif merge_result & pygit2.GIT_MERGE_ANALYSIS_NORMAL:
        print("Update failed - Did you modified any file?")
    
    print('Update succeeded.')

    # 모델 다운로드 부분
    model_url = "https://civitai.com/api/download/models/240840?type=Model&format=SafeTensor&size=full&fp=fp16"
    response = requests.get(model_url)

    if response.status_code == 200:
        model_file_name = "downloaded_model.pt"
        with open(model_file_name, "wb") as file:
            file.write(response.content)

        try:
            model = torch.load(model_file_name)
        except Exception as e:
            print(f"모델 로딩 중 오류 발생: {e}")
    else:
        print(f"모델 다운로드 실패: HTTP 상태 코드 {response.status_code}")

except Exception as e:
    print('Update failed.')
    print(str(e))

# 원래 코드의 끝부분
from launch import *
