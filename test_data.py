import data

curso = list(data.cursos_dict.values())[0]
mat = 'TEST001'

print('Usando DB em:', data.DB_PATH)

# Tentar criar usuário (pode já existir)
try:
    uid = data.adicionar_usuario('Teste', curso, mat, 0.0)
    print('Usuário criado:', uid)
except Exception as e:
    print('Adicionar usuário:', e)

# Mostrar saldo e recargas antes
try:
    saldo = data.obter_saldo(mat)
    recargas = data.obter_recargas(mat)
    print('Antes -> Saldo:', saldo, ', Recargas:', recargas)
except Exception as e:
    print('Erro lendo antes:', e)

# Efetuar recarga
try:
    ok = data.efetuar_recarga(mat, curso, 5.0)
    print('Recarga OK:', ok)
except Exception as e:
    print('Erro recarga:', e)

# Mostrar saldo e recargas depois
try:
    saldo = data.obter_saldo(mat)
    recargas = data.obter_recargas(mat)
    print('Depois -> Saldo:', saldo, ', Recargas:', recargas)
except Exception as e:
    print('Erro lendo depois:', e)
