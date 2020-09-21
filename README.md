# 내승 인승 

>  "내가 승리한 것이지 인간이 승리한 것이 아니야 "
>
> B201팀 - Insert Coin

## 목차
- [개요](#개요)
- [기능](#기능)
- [기술 스택](#기술-스택)
- [기술 설명](#기술-설명)
- [향후 전망](#향후-전망)
- [테스트 방법](#테스트-방법)

## 개요
> man VS AI  인공지능과 사람이 겨루는게임 플랫폼  

## 기능
> * 두뇌의 벽
>
>   - 2048 
>   - 뱀게임 

## 기술 스택
> Python, Pygame, Numpy

## 기술 설명
> - 2048 
>
>   (Heuristic Algorithm+ Minimax Algorithm를 변형한 Expectimax Algorithm)
>
>   - Heuristic 조건 
>
>     1. Big (큰수의 타일)
>
>     2. Emptiness (빈칸의 수)
>
>     3. Monotonicity (큰 수의 위치지정)
>
>     4. Smoothness  (상하좌우 타일의 비슷함)
>
>        => 조건 만족시 Expectimax 최대 손실을 최소화 
>
> - 뱀게임 
>
>   (Genetic Algorithm)
>
>   - 조건
>     1. 초기 세대 난수 설정
>     2. 규칙에 따라 각 유전자별 fitness 수치 산출
>     3. fitness 정리 후 난수를 이용하여 돌연변이 제작
>     4. 과정 반복

## 향후 전망

> - 2048 
>
>   ​	Pygame을 활용한 Python코드를 웹페이지 상에서 구현 도중 기술적인 한계를 	발견, 이를 해결하기 어려워 본 게임을 프로젝트에 포함시킬지 여부는 미정.
>
> - 두뇌의 벽
>
>   ​	Teachable Machine 사용 예정.
>
> - 뱀게임
>
>   ​	유전 알고리즘을 통하여 인공지능이 향상 되는 것을 확인하였음.
>
>   ​	최소 5단계의 난이도 조절을 위하여 더욱 많이 학습 할 예정.

## 테스트 방법
> 2048
>
> python game.py 실행
>
> 뱀게임
>
>  evolution.py 실행

