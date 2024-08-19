from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'  # Use uma chave secreta forte
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://branquinhodiogo:toledo22@branquinhodiogo.mysql.pythonanywhere-services.com:3306/branquinhodiogo$mydb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = "login"

# Modelos
class Usuario(db.Model, UserMixin):
    __tablename__ = "usuario"
    id = db.Column('usu_id', db.Integer, primary_key=True)
    nome = db.Column('usu_nome', db.String(256))
    email = db.Column('usu_email', db.String(256), unique=True)
    senha = db.Column('usu_senha', db.String(256))
    endereco = db.Column('usu_endereco', db.String(256))

    def __init__(self, nome, email, senha, endereco):
        self.nome = nome
        self.email = email
        self.senha = generate_password_hash(senha, method='sha256')  # Armazena a senha criptografada
        self.endereco = endereco

    def check_password(self, senha):
        return check_password_hash(self.senha, senha)  # Verifica a senha criptografada

class Categoria(db.Model):
    __tablename__ = "categoria"
    id = db.Column('cat_id', db.Integer, primary_key=True)
    nome = db.Column('cat_nome', db.String(256))
    descricao = db.Column('cat_descricao', db.String(256))

    def __init__(self, nome, descricao):
        self.nome = nome
        self.descricao= descricao

class Anuncio(db.Model):
    __tablename__ = "anuncio"
    id = db.Column('anu_id', db.Integer, primary_key=True)
    nome = db.Column('anu_nome', db.String(256))
    descricao = db.Column('anu_descricao', db.String(256))
    qtd = db.Column('anu_qtd', db.Integer)
    preco = db.Column('anu_preco', db.Float)
    cat_id = db.Column('cat_id', db.Integer, db.ForeignKey("categoria.cat_id"))
    usu_id = db.Column('usu_id', db.Integer, db.ForeignKey("usuario.usu_id"))

    def __init__(self, nome, descricao, qtd, preco, cat_id, usu_id):
        self.nome = nome
        self.descricao = descricao
        self.qtd = qtd
        self.preco = preco
        self.cat_id = cat_id
        self.usu_id = usu_id

# Configuração do LoginManager
@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(int(user_id))

# Rotas
@app.errorhandler(404)
def paginanaoencontrada(error):
    return render_template('404.html')

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        senha = request.form.get('senha')
        user = Usuario.query.filter_by(email=email).first()
        if user and user.check_password(senha):
            login_user(user)
            return redirect(url_for('index'))
        else:
            return "Login failed. Check your email and/or password."
    return render_template('login.html')

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route("/cad/usuario")
@login_required
def usuario():
    return render_template('usuario.html', usuarios=Usuario.query.all(), titulo="Usuario")

@app.route("/usuario/criar", methods=['POST'])
@login_required
def criarusuario():
    usuario = Usuario(
        request.form.get('user'),
        request.form.get('email'),
        request.form.get('senha'),
        request.form.get('endereco')
    )
    db.session.add(usuario)
    db.session.commit()
    return redirect(url_for('usuario'))

@app.route("/usuario/detalhar/<int:id>")
@login_required
def buscarusuario(id):
    usuario = Usuario.query.get(id)
    return usuario.nome

@app.route("/usuario/editar/<int:id>", methods=['GET', 'POST'])
@login_required
def editarusuario(id):
    usuario = Usuario.query.get(id)
    if request.method == 'POST':
        usuario.nome = request.form.get('user')
        usuario.email = request.form.get('email')
        usuario.senha = generate_password_hash(request.form.get('senha'), method='sha256')  # Atualiza a senha criptografada
        usuario.endereco = request.form.get('endereco')
        db.session.commit()
        return redirect(url_for('usuario'))
    return render_template('eusuario.html', usuario=usuario, titulo="Usuario")

@app.route("/usuario/deletar/<int:id>")
@login_required
def deletarusuario(id):
    usuario = Usuario.query.get(id)
    db.session.delete(usuario)
    db.session.commit()
    return redirect(url_for('usuario'))

@app.route("/cad/anuncio")
@login_required
def anuncio():
    return render_template('anuncio.html', anuncios=Anuncio.query.all(), categorias=Categoria.query.all(), titulo="Anuncio")

@app.route("/anuncio/criar", methods=['POST'])
@login_required
def criaranuncio():
    anuncio = Anuncio(
        request.form.get('nome'),
        request.form.get('descricao'),
        request.form.get('qtd'),
        request.form.get('preco'),
        request.form.get('cat'),
        request.form.get('uso')
    )
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
@login_required
def categoria():
    return render_template('categoria.html', categorias=Categoria.query.all(), titulo='Categoria')

@app.route("/categoria/criar", methods=['POST'])
@login_required
def criarcategoria():
    categoria = Categoria(request.form.get('nome'), request.form.get('descricao'))
    db.session.add(categoria)
    db.session.commit()
    return redirect(url_for('categoria'))

@app.route("/relatorios/vendas")
@login_required
def relVendas():
    return render_template('relVendas.html')

@app.route("/relatorios/compras")
@login_required
def relCompras():
    return render_template('relCompras.html')

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)  # Ative o modo de debug se desejar durante o desenvolvimento
