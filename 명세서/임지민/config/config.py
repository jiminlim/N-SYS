import argparse

# Req. 2-1	Config.py 파일 생성
parser = argparse.ArgumentParser(description="test")

# 캡션 데이터가 있는 파일 경로 (예시)
parser.add_argument('--answer', type=str, default='train',
                choices=['train','valid','test'],
                help='What data would you like to have?')   
parser.add_argument('--answer2', type=int, default=3,
                help='How many data?')              
parser.add_argument('--caption_file_path', type=str, default='.\\datasets\\captions.csv')
args = parser.parse_args()

def do_sampling():
    pass