import pandas as pd
from sklearn.utils import shuffle
import random

def get_user_list():    # user list  0~609까지 list 생성하는 함수
    data = pd.read_excel('./userProfile.xlsx', encoding='utf-8')
    user_list = []
    for i in range(len(data['id'])):
        user_list.append(data['id'][i]+1)

    return user_list

def recommendation(array):
    user_profile = pd.read_excel('./userprofile.xlsx')
    fa = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # 그룹안의 user들의 각 장르별 weight 합
    fb = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # 보편적인 추천을 하게 될 경우 weight 평균
    fc = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # 객체를 이용한 추천을 하게 될 경우 weight 평균
    count = 0
    count_difference = 0

    for i in array:     # list 안의 모든 user의 rating을 장르별로 합계내기
        ex_profile = user_profile[user_profile['id'] == (i-1)]
        for j in range(0, 19):
            fa[j] = fa[j] + ex_profile.iat[0, j + 1]
        count = count + 1   # user의 수도 센다

    for k in range(0, 19):
        fb[k] = fa[k] / count # fa[k]에 각 user의 장르 rating 넣고 평균으로 나눈 평균

    changed_count = count   # difference 4이상의 user가 그룹에서 빠졌을때 바뀐 count 저장

    for i in array: # list로 들어온 user들의 difference
        difference = 0  # 누적해서 더해야하는 difference 수치 초기화
        ex_profile = user_profile[user_profile['id'] == (i-1)]
        for j in range(0, 19):
            difference = difference + abs(fb[j] - ex_profile.iat[0, j + 1]) # fb(평균)과의 차이를 더해준다. 각 개인의 difference
        if difference > 4:  # 임계값 설정N  N 보다 큰 difference를 가진 user 들을 그룹에서 제외한다.
            #print('빠진 user : ', i)
            count_difference = count_difference + 1 # 몇명이 그룹의 평균과 많은 difference를 보였는지 수
            changed_count = changed_count - 1   # 사람이 빠졌을때 count 감소시키기
            for k in range(0, 19):
                fa[k] = fa[k] - ex_profile.iat[0, k + 1]    # 사람 빠지고 재 평균 계산을 위해 합들에서도 따로 뺴준다.

    for k in range(0, 19):
        fc[k] = fa[k] / changed_count   # 빠진 합들의 평균을 다시 구한다. (객체 생성)

    if count_difference >= (count / 3):  # 3(n) 변수이다 diffence가 큰 user수가 1/n 초과이면 보편적인 추천
        print('보편적인 추천')
        r = random.sample(range(1,43), 3)   # 1~43까지의 수 중 랜덤으로 3개의 수를 뽑는다.
        s = []
        best_movie = pd.read_excel('./bestmovies.xlsx')
        for i in range(0, 3):
            ex_best_movie = best_movie[best_movie['index'] == r[i]] # 랜덤한 3개의 수의 id를 가진 movie를 bestmovie에서 뽑는다.
            s.append(ex_best_movie.iat[0, 3])
        return s       # 그 3개 movie를 반환한다.

    else:   # 객체를 이용한 추천을 하게 되는 경우
        print('객체를 이용한 추천')
        difference = 0
        minimum = 100
        current = 0
        for i in range(0, 610): # 609명의 다른 user들 중 객체와 가장 비슷한 user를 찾는다.
            ex_profile = user_profile[user_profile['id'] == i]
            for j in range(0, 19):
                difference = difference + abs(fc[j] - ex_profile.iat[0, j + 1]) # 각 user마다 difference 수치 계산
            if difference < minimum:    # 609개의 difference 중 최소를 뽑아서 기억한다.
                minimum = difference
                current = i + 1
            difference = 0
        #print('객체 유저 번호: ', current)
        users = pd.read_excel('./ratings.xlsx')
        movies = pd.read_excel('./movies.xlsx')
        ex_users = users[users['id'] == current]    # current에 저장된 difference가 최소인 user의 영화 목록을 불러온다.
        ex_users = shuffle(ex_users)    # 랜덤으로 섞는다.
        ex_users.sort_values(by=['rating'], axis=0, ascending=False, inplace=True)  # 평점순으로 정렬한다.
        x = [0, 0, 0]
        s = []
        for i in range(0, 3):   # movie id를 위에서부터 3개 고른다.
            x[i] = ex_users.iat[i, 1]
        for i in range(0, 3):   # 해당 movie id로 movie name을 검색해서 s에 저장후 반환해준다.
            ex_movies = movies[movies['id'] == x[i]]
            s.append(ex_movies.iat[0, 1])
        return s