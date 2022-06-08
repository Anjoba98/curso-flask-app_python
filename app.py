from flask import Flask, render_template, request, redirect, url_for, flash
import urllib.request, json
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cursos.sqlite3'
app.secret_key = 'anjoba'
db = SQLAlchemy(app)

frutas = []
registros = []

class cursos(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50))
    descricao = db.Column(db.String(100))
    ch = db.Column(db.Integer)

    def __init__(self, nome, descricao, ch):
        self.nome = nome
        self.descricao = descricao
        self.ch = ch

@app.route("/", methods=["GET", "POST"])
def home():
    return render_template('home.html')

@app.route("/frutas/", methods=['GET', 'POST'])
def lista_frutas():
    if request.method == 'POST':
        if request.form.get('fruta'):
            frutas.append(request.form.get('fruta'))
    return render_template('lista_frutas.html', frutas = frutas)

@app.route("/diario/", methods=['GET', 'POST'])
def diario():
    if request.method == 'POST':
        if request.form.get('aluno') and request.form.get('nota'):
            registros.append({'aluno': request.form.get('aluno'), 'nota': request.form.get('nota')})
    return render_template('diario.html', registros=registros)

@app.route('/filmes/<propriedade>')
def filmes(propriedade):
    if propriedade == 'mais_populares':
        url = 'https://api.themoviedb.org/3/discover/movie?sort_by=popularity.desc&api_key=7b0beb1c848f739ab7672bcfe3f4fccc'
    elif propriedade == 'kids':
        url = 'https://api.themoviedb.org/3/discover/movie?certification_country=US&certification.lte=G&sort_by=popularity.desc&api_key=7b0beb1c848f739ab7672bcfe3f4fccc'
    elif propriedade == '2010':
        url = 'https://api.themoviedb.org/3/discover/movie?primary_release_year=2010&sort_by=vote_average.desc&api_key=7b0beb1c848f739ab7672bcfe3f4fccc'
    elif propriedade == 'drama':
        url = 'https://api.themoviedb.org/3/discover/movie?with_genres=18&sort_by=vote_average.desc&vote_count.gte=10&api_key=7b0beb1c848f739ab7672bcfe3f4fccc'
    elif propriedade == 'tom_cruise':
        url = 'https://api.themoviedb.org/3/discover/movie?with_genres=878&with_cast=500&sort_by=vote_average.desc&api_key=7b0beb1c848f739ab7672bcfe3f4fccc'
    elif propriedade == 'teatro':
        url = 'https://api.themoviedb.org/3/discover/movie?primary_release_date.gte=2014-09-15&primary_release_date.lte=2014-10-22&api_key=7b0beb1c848f739ab7672bcfe3f4fccc'
        
    resposta = urllib.request.urlopen(url)
    dados = resposta.read()
    jsondados = json.loads(dados)
    return render_template('filmes.html', filmes=jsondados['results'])

@app.route('/cursos/')
def lista_cursos():
    page = request.args.get('page', 1, type=int)
    per_page = 4
    todos_cursos = cursos.query.paginate(page, per_page)
    return render_template('cursos.html', cursos=todos_cursos)


@app.route('/criar_curso', methods=["GET", "POST"])
def criar_curso():
    nome = request.form.get('nome')
    descricao = request.form.get('descricao')
    ch = request.form.get('ch')

    if request.method == 'POST':
        if not nome or not descricao or not ch:
            flash("Preencha todos os campos do formulário.","error")
        else:
            curso = cursos(nome, descricao, ch)
            db.session.add(curso)
            db.session.commit()
            return redirect(url_for('lista_cursos'))
    return render_template("novo_curso.html")

@app.route('/cursos/<int:id>/atualizar_curso', methods=['GET', 'POST'])
def atualizar_curso(id):
    curso = cursos.query.filter_by(id=id).first()
    if request.method == 'POST':
        nome = request.form["nome"]
        descricao = request.form["descricao"]
        ch = request.form["ch"]
        
        cursos.query.filter_by(id=id).update({"nome":nome, "descricao":descricao, "ch":ch})
        db.session.commit()
        return redirect(url_for('lista_cursos'))
    return render_template("atualizar_curso.html", curso=curso)
    
@app.route('/cursos/<int:id>/remover_curso', methods=['GET', 'POST'])
def remover_curso(id):
    curso = cursos.query.filter_by(id=id).first()
    db.session.delete(curso)
    db.session.commit()
    return redirect(url_for('lista_cursos'))


if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)

