from crypt import methods
from flask import Flask, make_response
from markupsafe import escape
from flask import render_template
from flask import request
from flask_sqlalchemy import SQLAlchemy
from flask import url_for
from flask import redirect

app = Flask(__name__)
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://testuser:toledo22@localhost:3306/mydb'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://branquinhodiogo:toledo22@branquinhodiogo.mysql.pythonanywhere-services.com:3306/branquinhodiogo$mydb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Usuario(db.Model):
    __tablename__ = "usuario"
    id = db.Column('usu_id', db.Integer, primary_key=True)
    nome = db.Column('usu_nome', db.String(256))
    email = db.Column('usu_email', db.String(256))
    senha = db.Column('usu_senha', db.String(256))
    endereco = db.Column('usu_endereco', db.String(256))

    def __init__(self, nome, email, senha, endereco):
        self.nome = nome
        self.email = email
        self.senha = senha
        self.endereco = endereco

class Categoria(db.Model):
    __tablename__ = "categoria"
    id = db.Column('cat_id', db.Integer, primary_key=True)
    nome = db.Column('cat_nome', db.String(256))
    descricao = db.Column('cat_descricao', db.String(256))

    def __init__ (self, nome, descricao):
        self.nome = nome
        self.descricao= descricao

class Anuncio(db.Model):
    __tablename__ = "anuncio"
    id = db.Column('anu_id', db.Integer, primary_key=True)
    nome = db.Column('anu_nome', db.String(256))
    descricao = db.Column('anu_descricao', db.String(256))
    qtd = db.Column('anu_qtd', db.Integer)
    preco = db.Column('anu_preco', db.Float)
    cat_id = db.Column('cat_id',db.Integer, db.ForeignKey("categoria.cat_id"))
    usu_id = db.Column('usu_id',db.Integer, db.ForeignKey("usuario.usu_id"))

    def __init__(self, nome, descricao, qtd, preco, cat_id, usu_id):
        self.nome = nome
        self.descricao = descricao
        self.qtd = qtd
        self.preco = preco
        self.cat_id = cat_id
        self.usu_id = usu_id

@app.errorhandler(404)
def paginanaoencontrada(error):
    return render_template('pagnaoencontrada.html')

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/cad/usuario")
def usuario():
    return render_template('usuario.html', usuarios = Usuario.query.all(), titulo="Usuario")

@app.route("/usuario/criar", methods=['POST'])
def criarusuario():
    usuario = Usuario(request.form.get('user'), request.form.get('email'),request.form.get('senha'),request.form.get('endereco'))
    db.session.add(usuario)
    db.session.commit()
    return redirect(url_for('usuario'))

@app.route("/usuario/detalhar/<int:id>")
def buscarusuario(id):
    usuario = Usuario.query.get(id)
    return usuario.nome

@app.route("/usuario/editar/<int:id>", methods=['GET','POST'])
def editarusuario(id):
    usuario = Usuario.query.get(id)
    if request.method == 'POST':
        usuario.nome = request.form.get('user')
        usuario.email = request.form.get('email')
        usuario.senha = request.form.get('senha')
        usuario.endereco = request.form.get('endereco')
        db.session.add(usuario)
        db.session.commit()
        return redirect(url_for('usuario'))

    return render_template('eusuario.html', usuario = usuario, titulo="Usuario")

@app.route("/usuario/deletar/<int:id>")
def deletarusuario(id):
    usuario = Usuario.query.get(id)
    db.session.delete(usuario)
    db.session.commit()
    return redirect(url_for('usuario'))     

@app.route("/cad/anuncio")
def anuncio():
    return render_template('anuncio.html', anuncios = Anuncio.query.all(), categorias = Categoria.query.all(), titulo="Anuncio")

@app.route("/anuncio/criar", methods=['POST'])
def criaranuncio():
    anuncio = Anuncio(request.form.get('nome'), request.form.get('descricao'),request.form.get('qtd'),request.form.get('preco'),request.form.get('cat'),request.form.get('uso'))
    db.session.add(anuncio)
    db.session.commit()
    return redirect(url_for('anuncio'))

@app.route("/anuncios/pergunta")
def pergunta():
    return render_template('pergunta.html')

@app.route("/anuncios/compra")
def compra():
    print("anuncio comprado")
    return ""

@app.route("/anuncio/favoritos")
def favoritos():
    print("favorito inserido")
    return f"<h4>Comprado</h4>"

@app.route("/config/categoria")
def categoria():
    return render_template('categoria.html', categorias = Categoria.query.all(), titulo='Categoria')

@app.route("/categoria/criar", methods=['POST'])
def criarcategoria():
    categoria = Categoria(request.form.get('nome'), request.form.get('descricao'))
    db.session.add(categoria)
    db.session.commit()
    return redirect(url_for('categoria'))

@app.route("/relatorios/vendas")
def relVendas():
    return render_template('relVendas.html')

@app.route("/relatorios/compras")
def relCompras():
    return render_template('relCompras.html')

if __name__ == 'BBB':
    db.create_all()
    app.run()