from data import lista_cursos_CSHNB, lista_usuarios, recargas_pendentes, VALOR_FICHA, cursos_dict


def criar_usuário(nome, matricula, curso, saldo_conta):
    find = 0
    for cursos in lista_cursos_CSHNB:
        if curso == cursos:
            lista_usuarios.append({
                'Nome': nome,
                'Matrícula': matricula,
                'Curso': curso,
                'Saldo': saldo_conta
                                })
            find = 1
            print('Usuário adicionado com sucesso !!')
        
    if find != 1:
        print('Curso não encontrado !')

def verifica_matricula(matricula, curso):
    for dado in lista_usuarios:
        if matricula == dado['Matrícula'] and dado['Curso'] == curso :
            return True
            
    return False

def altera_saldo(matricula, curso):
    if verifica_matricula(matricula, curso):
        for dado in lista_usuarios:
            if dado['Matrícula'] == matricula:
                if dado['Saldo'] > 0:
                    dado['Saldo'] -= VALOR_FICHA
                    print('Bem vindo ao RU !')
                else:
                    print('Saldo insuficiente !')
    else:
        print('Conta não encontrada !')

def efetuar_recarga(matricula, curso, valor):
    if valor <= 10:
        #método para realizar autenticação
        autentica = verifica_matricula(matricula, curso)
        if autentica:
            #método para procurar a conta e atribuir saldo
            for dado in lista_usuarios:
                if dado['Matrícula'] == matricula and dado['Curso'] == curso:
                    dado['Saldo'] += valor
                    print('Recarga efetuada com sucesso !')

    else:
        print('|Recarga não efetuada !!')
        print('|Valor da recarga não pode ser maior que R$ 10,00 !')                

def visualizar_perfil(matricula, curso):
        find = 0
        for cursos in lista_cursos_CSHNB:
            if cursos == curso:
                for dado in lista_usuarios:
                    if dado['Matrícula'] == matricula:
                        print(f'|Nome: {dado['Nome']}\n|Matrícula: {dado['Matrícula']}\n|Curso: {dado['Curso']}\n|Saldo: R$ {dado['Saldo']:.2f}\n|------------------------')
                        find = 1
            
        if find != 1:
            print('Perfil não encontrado !!')


#lista recargas pendentes

menu = ('''
    | 1 - Criar usuário
    | 2 - Efetuar recarga
    | 3 - Entrar no RU
    | 4 - Visualizar perfil
    | 5 - Sair
    | OPC: ''')

while True:
    opcao = int(input(menu))

    match opcao:
        
        case 1:
            menu_curso = input('''
                        | SELECIONE O SEU CURSO 
                        |------------------------------------------
                        | A - Ciências Biológicas
                        | B - Educação do Campo/Ciências da Natureza
                        | C - História 
                        | D - Letras
                        | E - Pedagogia
                        | F - Matemática
                        | G - Administração
                        | H - Enfermagem 
                        | I - Medicina
                        | J - Nutrição
                        | K - Sistemas de informação
                        |------------------------------------------
                        | OPC: ''').upper()
                
            curso = cursos_dict.get(menu_curso)

            if curso:
                aluno = input('Nome completo: ')
                matricula = input('Matrícula: ')
                saldo = 0
                criar_usuário(nome = aluno, matricula = matricula, curso = curso, saldo_conta = saldo)
                continue

            else:
                print('Opção inválida !')
                continue

        case 2:
            if len(lista_usuarios) == 0:
                print('Nenhum usuário cadastrado, efetue cadastro !!!')
                continue
            else:
                menu_curso = input('''
                        | SELECIONE O SEU CURSO 
                        |------------------------------------------
                        | A - Ciências Biológicas
                        | B - Educação do Campo/Ciências da Natureza
                        | C - História 
                        | D - Letras
                        | E - Pedagogia
                        | F - Matemática
                        | G - Administração
                        | H - Enfermagem 
                        | I - Medicina
                        | J - Nutrição
                        | K - Sistemas de informação
                        |------------------------------------------
                        | OPC: ''').upper()
                
                curso = cursos_dict.get(menu_curso)

                if curso:
                    matricula = input('Digite sua matrícula: ')
                    valor_recarga = int(input('Digite o valor da recarga: '))
                    efetuar_recarga(matricula, curso, valor_recarga)
                    continue
                else:
                    print('Opção inválida !')
                    continue
            
        case 3:
            if len(lista_usuarios) == 0:
                print('Nenhum usuário cadastrado, efetue cadastro !!!')
                continue
            else:
                menu_curso = input('''
                        | SELECIONE O SEU CURSO 
                        |------------------------------------------
                        | A - Ciências Biológicas
                        | B - Educação do Campo/Ciências da Natureza
                        | C - História 
                        | D - Letras
                        | E - Pedagogia
                        | F - Matemática
                        | G - Administração
                        | H - Enfermagem 
                        | I - Medicina
                        | J - Nutrição
                        | K - Sistemas de informação
                        |------------------------------------------
                        | OPC: ''').upper()
                
                curso = cursos_dict.get(menu_curso)

                if curso:
                    matricula = input('Digite sua matrícula: ')
                    altera_saldo(matricula, curso)
                    continue
                else:
                    print('Opção inválida !')
                    continue
            
        case 4:
            menu_curso = input('''
                        | SELECIONE O SEU CURSO 
                        |------------------------------------------
                        | A - Ciências Biológicas
                        | B - Educação do Campo/Ciências da Natureza
                        | C - História 
                        | D - Letras
                        | E - Pedagogia
                        | F - Matemática
                        | G - Administração
                        | H - Enfermagem 
                        | I - Medicina
                        | J - Nutrição
                        | K - Sistemas de informação
                        |------------------------------------------
                        | OPC: ''').upper()
                
            curso = cursos_dict.get(menu_curso)

            if curso:
                matricula = input('Digite sua matrícula: ')
                visualizar_perfil(matricula, curso)
                continue
            else:
                print('Opção inválida !')
                continue
            

        case 5:
            print('| ENCERRANDO ....')
            break
