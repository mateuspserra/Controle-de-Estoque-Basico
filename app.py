from flask import Flask, render_template, request, redirect, url_for, session
import mysql.connector

app = Flask(__name__)

app.secret_key = 'estoquedeprodutos'

try:
    conexao = mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='controleestoque'
    )
    if conexao.is_connected():
        print('Conexão realizada com sucesso')
except OSError as error:
    print('Erro ao conectar: ', error)

cursor = conexao.cursor(dictionary=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/categorias', methods=['GET', 'POST'])
def categorias():
    if request.method == 'POST':
        nome_categoria = request.form['nome_categoria']

        comando = 'insert into categorias (nome_categoria) values (%s)'
        valores = (nome_categoria,)

        if not nome_categoria:
            return redirect(url_for('index'))

        cursor.execute(comando, valores)

        conexao.commit()

        return redirect(url_for('index'))
      
    return render_template('categorias.html')

@app.route('/cadastrar_produtos', methods=['GET', 'POST'])
def produtos():
    if request.method  == 'POST':
        nome_produto = request.form['nome_produto']
        descricao = request.form['descricao']
        preco = request.form['preco']
        quantidade = request.form['quantidade']
        categoria_id = request.form['categoria_id']
        
        if not nome_produto or not descricao or not preco or not quantidade or not categoria_id:
            return redirect(url_for('index'))

        comando = 'insert into produtos (nome_produto, descricao, preco, quantidade, categoria_id) values (%s, %s, %s, %s, %s)'
        valores = (nome_produto, descricao, preco, quantidade, categoria_id)

        cursor.execute(comando, valores)

        conexao.commit()

        return redirect(url_for('index'))
    
    return render_template('cadastrar_produtos.html')  

@app.route('/entradas_estoque', methods={'GET', 'POST'})
def entrada_estoque():
    if request.method == 'POST':
        produto_id = request.form['produto_id']
        quantidade = request.form['quantidade']
        preco = request.form['preco']
        fornecedor = request.form['fornecedor']

        if not produto_id or not quantidade or not preco or not fornecedor:
            return redirect(url_for('index'))

        comando = 'insert into entradas_estoque (produto_id, quantidade, preco, fornecedor) values (%s, %s, %s, %s)'
        valores = (produto_id, quantidade, preco, fornecedor)

        cursor.execute(comando, valores)

        conexao.commit()

        return redirect(url_for('index'))
    
    return render_template('entradas_estoque.html')

@app.route('/saida_estoque', methods={'GET', 'POST'})
def saida_estoque():
    if request.method == 'POST':
        produto_id = request.form['produto_id']
        quantidade = request.form['quantidade']
        preco_venda = request.form['preco_venda']
        destino = request.form['destino']

        if not produto_id or not quantidade or not preco_venda or not destino:
            return redirect(url_for('index'))
        
        comando = 'insert into saidas_estoques (produto_id, quantidade, preco_venda, destino) values (%s, %s, %s, %s)'
        valores = (produto_id, quantidade, preco_venda, destino)

        cursor.execute(comando, valores)

        conexao.commit()

        return redirect(url_for('index'))

    return render_template('saidas_estoque.html')

@app.route('/movimento_estoque', methods={'GET', 'POST'})
def movimento_estoque():
    if request.method == 'POST':
        produto_id = request.form['produto_id']
        tipo_movimento = request.form['tipo_movimento']
        quantidade = request.form['quantidade']
        observacao = request.form['observacao']

        if not produto_id or not tipo_movimento or not quantidade or not observacao:
            return "Erro: Todos os campos são obrigatórios!", 400
        
        if tipo_movimento not in ['ENTRADA', 'SAIDA']:
            return "Erro: Tipo de movimento inválido!", 400
        
        comando = 'insert into movimentos_estoque (produto_id, tipo_movimento, quantidade, observacao) values (%s, %s, %s, %s)'
        valores = (produto_id, tipo_movimento, quantidade, observacao)

        cursor.execute(comando, valores)

        conexao.commit()

        return redirect(url_for('index'))
    
    return render_template('movimentos_estoque.html')

@app.route('/fornecedores', methods={'GET', 'POST'})
def fornecedores():
    if request.method == 'POST':
        nome = request.form['nome']
        endereco = request.form['endereco']
        telefone = request.form['telefone']
        email = request.form['email']

        comando = 'insert into fornecedores (nome, endereco, telefone, email) values (%s, %s, %s, %s)'
        valores = (nome, endereco, telefone, email)

        cursor.execute(comando, valores)

        conexao.commit()

        return redirect(url_for('index'))
    
    return render_template('fornecedores.html')

@app.route('/atualizar_estoque/<int:id_produto>', methods={'GET', 'POST'})
def atualizar_estoque(id_produto):
    if request.method == 'POST':
        nome_produto = request.form['nome_produto']
        descricao = request.form['descricao']
        preco = request.form['preco']
        quantidade = request.form['quantidade']
        categoria_id = request.form['categoria_id']

        try:
            quantidade = int(request.form['quantidade'])
        except ValueError:
            quantidade = 0

        comando = 'update produtos set nome_produto = %s, descricao = %s, preco = %s, quantidade = quantidade + %s, categoria_id = %s where id_produto = %s'
        valores = (nome_produto, descricao, preco, quantidade, categoria_id, id_produto)

        cursor.execute(comando, valores)

        conexao.commit()

        return redirect(url_for('listar_produtos'))
    
    comando = 'select * from produtos where id_produto = %s'
    valor = (id_produto,)
    cursor.execute(comando, valor)
    produtos = cursor.fetchone()
    return render_template('atualizar_estoque.html', produto = produtos)

@app.route('/excluir_estoque/<int:id_produto>')
def exlcuir_estoque(id_produto):
    comando = 'delete from produtos where id_produto = %s'
    valor = (id_produto,)

    cursor.execute(comando, valor)
    conexao.commit()

    return redirect(url_for('listar_produtos'))

@app.route('/listar_produtos', methods=['GET', 'POST'])
def listar_produtos():
    comando = 'select * from produtos'

    cursor.execute(comando)

    produtos = cursor.fetchall()

    return render_template('listar_produtos.html', produtos = produtos)

@app.route('/listar_movimentaçoes', methods={'GET', 'POST'})
def listar_movimentacoes():
    comando = 'select * from movimentos_estoque'

    cursor.execute(comando)

    produtos = cursor.fetchall()

    return render_template('listar_movimentacoes.html', produtos = produtos)

@app.route('/consultar_produto')
def consultar_produto():
    id_produto = request.args.get('id_produto')
    comando = 'select * from produtos p join categorias c on p.categoria_id = c.id_categoria where p.id_produto = %s'
    cursor.execute(comando, (id_produto,))
    produto = cursor.fetchall()
    return render_template('consultar_produto.html', produto = produto)
















if __name__ == '__main__':
    app.run(debug=True)