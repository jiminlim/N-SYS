# 테스트 이미지를 받아 캡션을 예측하는 파일
from utils import utils
import config

## req 1-1
nomal_flag = True #True : 정규화
# nomal_flag = False #False : 정규화X
utils.image_check(config.args.image_file_path+config.args.image_name,nomal_flag)