import flask
# エントリーポイントがapp.ymlで定義されていなかった場合、App Engineはmain.pyでappと呼ばれる部分を探す
app = flask.Flask(__name__)


@app.route("/", methods=["GET"])
def hello():
    """ Return a friendly HTTP greeting. """
    return "Hello World!\n"


if __name__ == "__main__":
    '''
    ローカル実行のみの定義
    GAEにデプロイすると、ウェブサーバープロセスがアプリを提供する
    app.yamlにentrypointを追加することで、構成できる
    '''
    app.run(host="localhost", port=8080, debug=True)