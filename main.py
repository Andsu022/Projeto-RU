from data import lista_cursos_CSHNB, dicionario_usuarios


def criar_usuário(nome, matricula, curso_aluno, saldo_conta):
    for cursos in lista_cursos_CSHNB:
        if curso_aluno == cursos:
            dicionario_usuarios.update({'Nome': nome, 'Matrícula': matricula, 'Curso': curso_aluno, 'Saldo': saldo_conta})

def verifica_matricula(matricula, curso):
    for cursos in lista_cursos_CSHNB:
        if curso == cursos:
            for dado in dicionario_usuarios.items():
                return True if matricula == dado['Matrícula'] else False


def efetuar_recarga(matrícula, curso, valor):
    #método para realizar autenticação
    autentica = verifica_matricula(matricula, curso)
    if autentica == True:
        #método para procurar a conta e atribuir saldo
        for dado in dicionario_usuarios.items():
            if matrícula == dado['Matrícula']:
                dado['Saldo'] = valor



menu = '''
    | 1 - Criar usuário
    | 2 - Efetuar recarga
    | 3 - Comprar ficha
    | 4 - Sair
    | OPC: '''

while True:
    opcao = int(input(menu))

    match menu:
        
        case 1:
            aluno = input('Nome completo: ')
            matricula = input('Matrícula: ')
            curso = input('Curso: ')
            saldo = 0

            criar_usuário(nome = aluno, matricula = matricula, curso_aluno = curso, saldo_conta = saldo)
            continue

        case 2:
            pass