import pandas as pd
import numpy as np

genre = 0


def find_max(array):        # list내 최대값 찾는 함수
    ex_max = 0
    for i in range(0, 19):
        if array[i] > ex_max:
            ex_max = array[i]
    return ex_max


def select_genre(movie_genre):          # genre를 숫자로 바꿔주는 함수
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


ratings = pd.read_excel('./ratings.xlsx')
movies = pd.read_excel('./movies.xlsx')

users = np.zeros( (610, 20, 2) )
users_profile = np.zeros( (610, 19) )
extra_movie = np.zeros( (193609, 2) )
movie_profile = np.zeros( (193609, 1) )

for i in range(0, 100789):      # 전체 평가 횟수 100789만큼 평가 마다 해당 rating을 그 id와 일치하는 영화의 장르를 찾아서 user id 와 일치하는 userprofile에 저장해준다.
   a = ratings.iat[i, 1]        # a = movie id
   b = ratings.iat[i, 0] - 1    # b = user id
   c = ratings.iat[i, 2]        # c = rating
   ex_movie = movies[movies['id'] == a]     # id가 같은 movie를 찾는다
   for j in range(2, 10):                   # 해당 movie의 genre를 숫자로 바꿔서 비어있는 userprofile list의 해당 index에 rating만큼 더한다.
       select_genre(ex_movie.iat[0, j])
       if genre != 20:
           users[b][genre][1] += c  # rating 더하기
           users[b][genre][0] += 1  # rating 횟수세기
   users[b][19][0] += 1
   extra_movie[ex_movie.iat[0, 0] - 1][1] += c  # movie profile 제작용
   extra_movie[ex_movie.iat[0, 0] - 1][0] += 1


for i in range(0, 610):     # userprofile 계산하는 구체적인 loop 609명의 user
    for j in range(0, 19):  # (user가 평가한 각 장르 레이팅의 평균) * (각 user가 평가한 장르 횟수 / 전체 평가 횟수 + 1)
        users_profile[i][j] = (users[i][j][1] / users[i][j][0]) * ((users[i][j][0] / users[i][19][0]) + 1)
    temp_max = find_max(users_profile[i])  # 가장 높게 평가한 장르 찾기
    for k in range(0, 19):
        users_profile[i][k] = (users_profile[i][k] / temp_max) # 가장 높게 평가한 장르 weight로 모두 나눠줌 = userprofile 생성

for i in range(0, 193609):  # (movie raing의 편균) + (movie가 평가된 횟수 / 100)
    movie_profile[i][0] = (extra_movie[i][1] / extra_movie[i][0]) + (extra_movie[i][0] / 100)


np.nan_to_num(users_profile, copy=False)
np.nan_to_num(movie_profile, copy=False)

df = pd.DataFrame.from_records(users_profile)
df.to_excel('userprofile.xlsx')

df = pd.DataFrame.from_records(movie_profile)
df.to_excel('movieprofile.xlsx')