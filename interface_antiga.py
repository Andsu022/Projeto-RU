import data

#lista recargas pendentes

cursos = data.Curso()
alunos = data.Aluno()

menu = ('''
    | 1 - Criar usuário
    | 2 - Efetuar recarga
    | 3 - Entrar no RU
    | 4 - Visualizar perfil
    | 5 - Sair
    | OPC: ''')

while True:
    try:
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
                
                id_curso = cursos.procurar_curso_id(menu_curso)

                if id_curso:
                    aluno = input('Nome completo: ')
                    matricula = int(input('Matrícula(somente números): '))
                    matricula = str(matricula)
                    saldo = 0
                    alunos.adicionar_usuario(nome = aluno, matricula = matricula, curso_id = id_curso, saldo = saldo)
                    continue        

                else:
                    print('Opção inválida !')
                    continue

            case 2:
                try:
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
                    
                    curso = cursos.procurar_curso_nome(menu_curso)

                    if curso:
                        matricula = input('Digite sua matrícula: ')
                        valor_recarga = int(input('Digite o valor da recarga: '))
                        confirma_usuario = alunos.verifica_usuario(matricula, curso)
                        alunos.efetuar_recarga(matricula, curso, valor_recarga)
                        continue
                    else:
                        print('Opção inválida !')
                        continue
                except ValueError as ve:
                    print(f"Erro: {ve}")
                    continue
            case 3:
                try:
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
                    
                    curso = cursos.procurar_curso_nome(menu_curso)

                    if curso:
                        matricula = input('Digite sua matrícula: ')
                        alunos.altera_saldo(matricula, curso)
                        continue
                    else:
                        print('Opção inválida !')
                        continue
                
                except ValueError as ve:
                    print(f"ERRO: {ve}") 
                
            case 4:
                try:
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
                        
                    curso = cursos.procurar_curso_nome(menu_curso)

                    if curso:
                        matricula = input('Digite sua matrícula: ')
                        alunos.mostrar_alunos(matricula, curso)
                        continue
                    else:
                        print('Opção inválida !')
                        continue
                    
                except ValueError as ve:
                    print(f"ERRO: {ve}") 

            case 5:
                print('| ENCERRANDO ....')
                break
            
            case _:
                print('Opção inválida !')
                continue
            
    except Exception as e:
        print(f"ERRO: {e}")
