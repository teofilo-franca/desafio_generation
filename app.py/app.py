from flask import Flask, request, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///school.db'
db = SQLAlchemy(app)

class Aluno(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100))
    idade = db.Column(db.Integer)
    nota_primeiro_semestre = db.Column(db.Float)
    nota_segundo_semestre = db.Column(db.Float)
    nome_professor = db.Column(db.String(100))
    numero_sala = db.Column(db.Integer)

@app.route('/')
def listar_alunos():
    alunos = Aluno.query.all()
    return render_template('listar_alunos.html', alunos=alunos)

@app.route('/adicionar_aluno', methods=['GET', 'POST'])
def adicionar_aluno():
    if request.method == 'POST':
        novo_aluno = Aluno(
            nome=request.form['nome'],
            idade=int(request.form['idade']),
            nota_primeiro_semestre=float(request.form['nota_primeiro_semestre']),
            nota_segundo_semestre=float(request.form['nota_segundo_semestre']),
            nome_professor=request.form['nome_professor'],
            numero_sala=int(request.form['numero_sala'])
        )
        db.session.add(novo_aluno)
        db.session.commit()
        return redirect(url_for('listar_alunos'))
    return render_template('adicionar_aluno.html')

@app.route('/editar_aluno/<int:id>', methods=['GET', 'POST'])
def editar_aluno(id):
    aluno = Aluno.query.get(id)
    if request.method == 'POST':
        aluno.nome = request.form['nome']
        aluno.idade = int(request.form['idade'])
        aluno.nota_primeiro_semestre = float(request.form['nota_primeiro_semestre'])
        aluno.nota_segundo_semestre = float(request.form['nota_segundo_semestre'])
        aluno.nome_professor = request.form['nome_professor']
        aluno.numero_sala = int(request.form['numero_sala'])
        db.session.commit()
        return redirect(url_for('listar_alunos'))
    return render_template('editar_aluno.html', aluno=aluno)

@app.route('/remover_aluno/<int:id>')
def remover_aluno(id):
    aluno = Aluno.query.get(id)
    db.session.delete(aluno)
    db.session.commit()
    return redirect(url_for('listar_alunos'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
