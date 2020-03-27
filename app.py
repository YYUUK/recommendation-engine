from flask import Flask, render_template, request
import difference

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
@app.route('/table.html', methods=['POST'])

def hello_name():
    if request.method == 'GET':
        user_list = difference.get_user_list()         # userlist를 가져와서 table에 checkbox로 출력
        return render_template('table.html', payload=user_list)
    elif request.method == 'POST':
        user_list = list(map(int, request.form.getlist('user_name')))
        movie_list = difference.recommendation(user_list)
        return render_template('result.html', payload=movie_list)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000, debug=True)
    # 192.168.56.1