from difference import recommendation
import random
import pandas as pd


def select_genre(movie_genre): # 장르를 정수로 바꿔주기
    global genre
    if movie_genre == 'Action':
        genre = 0
    elif movie_genre == 'Adventure':
        genre = 1
    elif movie_genre == 'Animation':
        genre = 2
    elif movie_genre == 'Children':
        genre = 3
    elif movie_genre == 'Comedy':
        genre = 4
    elif movie_genre == 'Fantasy':
        genre = 5
    elif movie_genre == 'Imax':
        genre = 6
    elif movie_genre == 'Romance':
        genre = 7
    elif movie_genre == 'Scifi':
        genre = 8
    elif movie_genre == 'Western':
        genre = 9
    elif movie_genre == 'Crime':
        genre = 10
    elif movie_genre == 'Mystery':
        genre = 11
    elif movie_genre == 'Thriller':
        genre = 12
    elif movie_genre == 'Drama':
        genre = 13
    elif movie_genre == 'Horror':
        genre = 14
    elif movie_genre == 'Filmnoir':
        genre = 15
    elif movie_genre == 'Documentary':
        genre = 16
    elif movie_genre == 'War':
        genre = 17
    elif movie_genre == 'Musical':
        genre = 18
    else:
        genre = 20

movies = pd.read_excel('./movies.xlsx')
user_profile = pd.read_excel('./userprofile.xlsx')

sum = 0

print('TEST 시작')

for z in range(0, 30):
    count = 0       # 전체횟수 세기
    fail = 0        # 실패횟수 세기
    a = random.sample(range(4,10), 1)       # 4~10사이의 랜덤 수 1개 생성
    r = random.sample(range(1,609), a[0])   # 1~609 사이의 랜덤 수 a개 생성
    print('유저 :', r)
    s = recommendation(r)           # 추천엔진
    print('영화 :', s)
    ex_list = []

    for i in range(0, 3):
        ex_movie = movies[movies['name'] == s[i]]   # 이름이 같은 영화의 장르 찾기
        for j in range(2, 10):
            select_genre(ex_movie.iat[0, j])
            if genre != 20:
               ex_list.append(genre)
    ex_list.append(0)
    ex_list = list(set(ex_list))            # 장르를 찾아서 중복 제거하고 저장한다

    print('장르 :', ex_list)

    for i in r:
        ex_profile = user_profile[user_profile['id'] == (i - 1)]    # userprofile에서 그 user 뽑는다.
        for j in ex_list:
            #print(ex_profile.iat[0,j])
            count = count + 1;
            if ex_profile.iat[0, j] < 0.6:      # 그 유저의 해당 genre weight가 0.6보다 작으면 실패
                #print('실패')
                fail = fail + 1

    sum = sum + 1 - (fail / count)
    print(z+1, '번째 user data set 성공률 : ', 1 - (fail / count))

print('TEST 끝')
print('전체 성공률 평균: ', sum / 30 )