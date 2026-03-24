import sqlite3
import json
from datetime import datetime
from pathlib import Path
from abc import ABC
from Libs import qrcode_pix
"""Gerenciador de banco de dados SQLite para o RU."""

# Definir caminho do banco relativo ao arquivo atual e garantir que o diretório exista
ROOT_DIR = Path(__file__).resolve().parent
DB_DIR = ROOT_DIR / 'Databank RU'
DB_DIR.mkdir(parents=True, exist_ok=True)
DB_PATH = DB_DIR / 'RU.db'
CHAVE_PIX = "andersoncarvalho240@gmail.com"

VALOR_FICHA = 0.8

cursos_dict = {
    'Ciências Biológicas': 'A',
    'Educação do Campo/Ciências da Natureza': 'B',
    'História': 'C',
    'Letras': 'D',
    'Pedagogia': 'E',
    'Matemática': 'F',
    'Administração': 'G',
    'Enfermagem': 'H',
    'Medicina': 'I',
    'Nutrição': 'J',
    'Sistemas de informação': 'K'
}

lista_cursos_CSHNB = list(cursos_dict.values())
"""Inicializa as tabelas se não existirem."""
conection = sqlite3.connect(str(DB_PATH))
cursor = conection.cursor()

class Pagamento(ABC):
    def __init__(self):
        super().__init__()

    @classmethod
    def pagamento_pix(cls, matricula, valor):
        chave_pix = CHAVE_PIX
        try:
            # gerar QR code
            qrcode_pix.Pagamento.pagamento_pix(matricula, chave_pix, valor)
            return True
        
        except Exception as e :
            print(f"Erro: {e}")

    @classmethod
    def pagamento_especie(cls, matricula, valor):
        try:    
            data_solicitacao = datetime.now().strftime('%d/%m/%Y %H:%M')

            cursor.execute('''
                        CREATE TABLE IF NOT EXISTS solicitacao_recargas(
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        matricula_aluno TEXT NOT NULL UNIQUE,
                        data_recarga DATETIME,
                        valor REAL NOT NULL,
                        FOREIGN KEY (matricula_aluno) REFERENCES alunos (matricula)
                        )
                    ''')
            cursor.execute('INSERT INTO solicitacao_recargas (matricula_aluno, data_recarga, valor) VALUES (?, ?, ?)', 
                        (matricula, data_solicitacao, valor))
            conection.commit()
            print('Solicitação de recarga registrada com sucesso !')

        except Exception as e:
            print(f'Erro ao registrar solicitação de recarga: {e}')

class Curso():
    def __init__(self):
         cursor.execute('''
            CREATE TABLE IF NOT EXISTS cursos(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome_curso TEXT NOT NULL UNIQUE)
            ''')
        
    def adicionar_curso(self, nome_curso):
        connection = sqlite3.connect(str(DB_PATH))
        cursor = connection.cursor()    
        cursor.execute('INSERT INTO cursos (nome_curso) VALUES (?)', (nome_curso,))
        connection.commit()
        connection.close()

    def editar_curso(self, curso_id, novo_nome):
        connection = sqlite3.connect(str(DB_PATH))
        cursor = connection.cursor()
        cursor.execute('UPDATE cursos SET nome_curso = ? WHERE id = ?', (novo_nome, curso_id))
        connection.commit()
        connection.close()

    def deletar_curso(self, curso_id):
        connection = sqlite3.connect(str(DB_PATH))
        cursor = connection.cursor()
        cursor.execute('DELETE FROM cursos WHERE id = ?', (curso_id,))
        connection.commit()
        connection.close()

    def mostrar_cursos(self):
        """Exibe todos os cursos cadastrados."""
        connection = sqlite3.connect(str(DB_PATH))
        cursor = connection.cursor()
        
        try:
            cursor.execute('SELECT id, nome_curso FROM cursos')
            cursos = cursor.fetchall()
            if not cursos:
                print('Nenhum curso encontrado.')
            else:
                for curso in cursos:
                    print(f'ID: {curso[0]}, Curso: {curso[1]}')
                    print('---------------------------------------')
        finally:
            connection.close()
    
    def procurar_curso_id(self, nome_curso):        
        connection = sqlite3.connect(str(DB_PATH))
        cursor = connection.cursor()
        cursor.execute('SELECT id FROM cursos WHERE nome_curso = ?', (nome_curso,))
        curso = cursor.fetchone()[0]
        if not curso:
            raise ValueError("Curso não encontrado ou inválido !")
        else:
            return curso
        
    # def procurar_curso_nome(self, menu_curso):
    #     nome_curso = cursos_dict.get(menu_curso)
    #     connection = sqlite3.connect(str(DB_PATH))
    #     cursor = connection.cursor()
    #     cursor.execute('SELECT nome_curso FROM cursos WHERE nome_curso = ?', (nome_curso,))
    #     curso = cursor.fetchone()[0]
    #     if not curso:
    #         raise ValueError("Curso não encontrado ou inválido !")
    #     else:
    #         return curso
    
        
class Aluno(Pagamento):
    def __init__(self):
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS alunos(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                saldo REAL NOT NULL,
                curso_id INTEGER,
                matricula TEXT NOT NULL UNIQUE,
                recargas TEXT DEFAULT '[]',
                FOREIGN KEY (curso_id) REFERENCES cursos (id))
            ''')
    
    def adicionar_usuario(self, nome, curso_id, matricula, saldo):
        connection = sqlite3.connect(str(DB_PATH))
        cursor = connection.cursor()    
        cursor.execute('INSERT INTO alunos (nome, saldo, curso_id, matricula) VALUES (?, ?, ?, ?)', 
                     (nome, saldo, curso_id, matricula))
        connection.commit()
        connection.close()

    def editar_usuario(self, usuario_id, nome=None, curso_id=None, matricula=None, saldo=None):
        connection = sqlite3.connect(str(DB_PATH))
        cursor = connection.cursor()
        updates = []
        params = []
        
        if nome is not None:
            updates.append('nome = ?')
            params.append(nome)
        if curso_id is not None:
            updates.append('curso_id = ?')
            params.append(curso_id)
        if matricula is not None:
            updates.append('matricula = ?')
            params.append(matricula)
        if saldo is not None:
            updates.append('saldo = ?')
            params.append(saldo)
        
        params.append(usuario_id)
        sql = f'UPDATE alunos SET {", ".join(updates)} WHERE id = ?'
        cursor.execute(sql, params)
        connection.commit()
        connection.close()

    def deletar_usuario(self, usuario_id):
        connection = sqlite3.connect(str(DB_PATH))
        cursor = connection.cursor()
        cursor.execute('DELETE FROM alunos WHERE id = ?', (usuario_id,))
        connection.commit()
        connection.close()

    def verifica_usuario(self, matricula, nome_curso):
        """Verifica se um usuário existe."""
        conection = sqlite3.connect(str(DB_PATH))
        cursor = conection.cursor()
        
        try:
            cursor.execute('''
                SELECT a.id FROM alunos a
                JOIN cursos c ON a.curso_id = c.id
                WHERE a.matricula = ? AND c.nome_curso = ?
            ''', (matricula, nome_curso))
            usuario = cursor.fetchone()
            return usuario[0] if usuario is not None else None
        finally:
            conection.close()

    
    def altera_saldo(self, matricula, nome_curso):
        """Reduz o saldo do usuário em VALOR_FICHA."""
        conection = sqlite3.connect(str(DB_PATH))
        cursor = conection.cursor()
        
        try:
            aluno = Aluno()
            usuarioid = aluno.verifica_usuario(matricula, nome_curso)
            if usuarioid:
                cursor.execute('SELECT saldo FROM alunos WHERE matricula = ?', (matricula,))
                saldo_atual = cursor.fetchone()[0]
                if saldo_atual >= VALOR_FICHA:
                    novo_saldo = saldo_atual - VALOR_FICHA
                    cursor.execute('UPDATE alunos SET saldo = ? WHERE matricula = ?', (novo_saldo, matricula))
                    print('Bem vindo ao RU, bom apetite !!')
                    conection.commit()
                    return True
                else:
                    raise ValueError('Saldo insuficiente !')
            else:
                raise ValueError('Usuário não encontrado !')
        finally:
            conection.close()

    def efetuar_recarga(self, matricula, nome_curso, valor):
        """Efetua uma recarga de saldo para o usuário."""
        conection = sqlite3.connect(str(DB_PATH))
        cursor = conection.cursor()
        
        try:
            aluno = Aluno()
            usuarioid = aluno.verifica_usuario(matricula, nome_curso)
            if usuarioid:
                # Buscar saldo e histórico de recargas atuais
                cursor.execute('SELECT saldo, recargas FROM alunos WHERE matricula = ?', (matricula,))
                row = cursor.fetchone()
                if row is None:
                    raise ValueError('Usuário não encontrado !')
                saldo_atual, recargas_json = row
                try:
                    recargas = json.loads(recargas_json) if recargas_json else []
                except (TypeError, json.JSONDecodeError):
                    recargas = []

                # Solicita o meio de pagamento
                pagamento = Pagamento()
                opcao_pagamento = int(input("\n| SELECIONE UM MEIO DE PAGAMENTO:\n| 1 - PIX\n| 2 - DINNHEIRO EM ESPÉCIE"))
                if opcao_pagamento == 2:
                    pagamento.pagamento_especie(matricula, valor)
                    conection.commit()
                else:
                    confirmacao_pagamento = pagamento.pagamento_pix(matricula, valor)
                    if confirmacao_pagamento:
                        # Atualiza valores
                        novo_saldo = saldo_atual + valor
                        recargas.append({'valor': valor, 'data': datetime.now().strftime('%d/%m/%Y %H:%M')})
                        cursor.execute('UPDATE alunos SET saldo = ?, recargas = ? WHERE matricula = ?', 
                                    (novo_saldo, json.dumps(recargas), matricula))
                        print('Recarga feita com sucesso !')
                        conection.commit()
                        return True
                    else:
                        print("Erro ao efetuar pagamento !")
                
            else:
                raise ValueError('Usuário não encontrado !')
        finally:
            conection.close()    

    def obter_saldo(self, matricula):
        """Retorna o saldo atual do usuário."""
        conection = sqlite3.connect(str(DB_PATH))
        cursor = conection.cursor()
        
        try:
            cursor.execute('SELECT saldo FROM alunos WHERE matricula = ?', (matricula,))
            row = cursor.fetchone()
            if row:
                return row[0]
            else:
                raise ValueError('Usuário não encontrado !')
        finally:
            conection.close()


    def obter_recargas(self, matricula):
        """Retorna o histórico de recargas do usuário."""
        conection = sqlite3.connect(str(DB_PATH))
        cursor = conection.cursor()
        
        try:
            cursor.execute('SELECT recargas FROM alunos WHERE matricula = ?', (matricula,))
            row = cursor.fetchone()
            if row:
                recargas_json = row[0]
                try:
                    return json.loads(recargas_json) if recargas_json else []
                except (TypeError, json.JSONDecodeError):
                    return []
            else:
                raise ValueError('Usuário não encontrado !')
        finally:
            conection.close()

    def mostrar_alunos(self, matricula, nome_curso):
        """Exibe todos os usuários cadastrados."""
        conection = sqlite3.connect(str(DB_PATH))
        cursor = conection.cursor()
        
        try:
            aluno = Aluno()
            usuario = aluno.verifica_usuario(matricula, nome_curso)
            if usuario:
                cursor.execute('''
                    SELECT a.id, a.nome, a.matricula, a.saldo, c.nome_curso
                    FROM alunos a
                    JOIN cursos c ON a.curso_id = c.id
                ''')
                alunos = cursor.fetchall()

                for usuario in alunos:
                    print(f'|ID: {usuario[0]}\n|Nome: {usuario[1]}\n|Matrícula: {usuario[2]}\n|Saldo: {usuario[3]:.2f}\n|Curso: {usuario[4]}\n|-------------------------------------')
            
            else:
                raise ValueError('Nenhum usuário encontrado.')
            
        finally:
            conection.close()

conection.commit()


# def _inserir_cursos_iniciais():
#     """Insere os cursos iniciais se ainda não existirem."""
#     conection = sqlite3.connect(str(DB_PATH))
#     cursor = conection.cursor()
    
#     for curso in lista_cursos_CSHNB:
#         try:
#             cursor.execute('INSERT INTO cursos (nome_curso) VALUES (?)', (curso,))
#         except sqlite3.IntegrityError:
#             pass  # Curso já existe, ignorar o erro
    
#     conection.commit()
#     conection.close()


class Funcionario():
    def __init__(self):
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS funcionarios(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                matricula TEXT NOT NULL UNIQUE,
                funcao TEXT NOT NULL)   
            ''')
        
    def adicionar_funcionario(self, nome, matricula, funcao):
        connection = sqlite3.connect(str(DB_PATH))
        cursor = connection.cursor()    
        cursor.execute('INSERT INTO funcionarios (nome, matricula, funcao) VALUES (?, ?, ?)', 
                     (nome, matricula, funcao))
        connection.commit()
        connection.close()


class Caixa(Pagamento, Funcionario, Aluno):
    def __init__(self):
        Funcionario.__init__(self)
        Aluno.__init__(self)

if __name__ == "__main__":
    # Exemplo de uso
    curso = Curso()
    aluno = Aluno()
    funcionario = Funcionario()
    caixa = Caixa()

# Inicializar banco ao importar o módulo
# _init_db()
# _inserir_cursos_iniciais()
# # mostrar_cursos()
# # mostrar_alunos()

# _inserir_cursos_iniciais()
# mostrar_alunos()
# mostrar_cursos()
# conection.commit()
# conection.close()
