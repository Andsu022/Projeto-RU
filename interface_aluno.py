from re import match
import tkinter as tk
from tkinter import ttk, messagebox
from unittest import case
import data


class SistemaRU:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema do Restaurante Universitário da UFVM ")
        self.root.geometry("500x450")
        self.root.resizable(False, False)

        self.root.columnconfigure(0, weight=1)

        self.create_widgets()

    def create_widgets(self):
        # Título
        title = ttk.Label(
            self.root,
            text="Restaurante Universitário UFVM",
            font=("Arial", 18, "bold")
        )
        title.grid(row=0, column=0, pady=20)

        # Frame dos botões
        frame = ttk.Frame(self.root, padding=20)
        frame.grid(row=1, column=0)

        buttons = [
            ("1 - Criar usuário", self.criar_usuario),
            ("2 - Efetuar recarga", self.efetuar_recarga),
            # ("3 - Entrar no RU", self.entrar_ru),
            ("3 - Visualizar perfil", self.visualizar_perfil),
            ("4 - Sair", self.sair)
        ]

        for i, (text, command) in enumerate(buttons):
            btn = ttk.Button(
                frame,
                text=text,
                command=command,
                width=30
            )
            btn.grid(row=i, column=0, pady=8)



    # ===== Funcionalidades =====

    def criar_usuario(self):
        janela = tk.Toplevel(self.root)
        janela.title("Criar Usuário")
        janela.geometry("400x300")

        # Dicionário: nome -> código
        self.cursos = {
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

        ttk.Label(janela, text= "Selecionar tipo de usuário").pack(pady=10)
        
        self.user_option = ttk.Combobox(
        janela,
        values = ("Aluno", "Funcionário", "Visitante"),
        state="readonly"
        )
        self.user_option.pack(pady=10)

        ttk.Button(
        janela,
        text="Confirmar",
        command=self.selecionar_usuario
        ).pack(pady=20)

        ttk.Button(
        janela,
        text = "Voltar",
        command=janela.destroy
        ).pack(pady=15)


    def selecionar_usuario(self):
        janela = tk.Toplevel(self.root)
        janela.title("Criar Usuário")
        janela.geometry("400x300")

        tipo_user = self.user_option.get().strip()
        match(tipo_user):

            case "Aluno":
                ttk.Label(janela, text="Selecionar curso").pack(pady=10)

                self.curso_combo = ttk.Combobox(
                janela,
                values=list(self.cursos.keys()),
                state="readonly"
                )
                
                self.curso_combo.pack(pady=10)

                ttk.Button(
                janela,
                text="Confirmar",
                command=self.salvar_aluno
                ).pack(pady=20)

                ttk.Button(
                janela,
                text = "Voltar",
                command=janela.destroy
                ).pack(pady=15)
                
            case "Funcionário":
                ttk.Button(
                janela,
                text="Confirmar",
                command=self.salvar_funcionario
                ).pack(pady=20)

                ttk.Button(
                janela,
                text = "Voltar",
                command=janela.destroy
                ).pack(pady=15)

            case "Visitante":
                messagebox.showinfo(
                    "Visitante", "Bem vindo, visitante !\nAcesso ao RU liberado !"
                )
                janela.destroy()

            case _:
                messagebox.showerror("Erro", "Por favor, selecione um tipo de usuário válido.")

    def salvar_aluno(self):
        curso_selecionado = self.curso_combo.get().strip()
        if curso_selecionado == "Selecione o seu curso" or curso_selecionado not in self.cursos:
            messagebox.showerror(
                "Erro",
                "Por favor, selecione um curso válido."
            )
            return
        
        # Procurando o id do curso pelo nome
        curso = data.Curso()
        id_curso_selecionado = curso.procurar_curso_id(curso_selecionado)

        # teste
        # messagebox.showinfo(
        #     f"Curso Selecionado",
        #     f"Você selecionou o curso: {curso_selecionado}"
        # )

        # Cria uma nova janela para coletar informações do usuário
        janela_info = tk.Toplevel(self.root)
        janela_info.title("Informações do Usuário")
        janela_info.geometry("350x200")
        janela_info.resizable(False, False)

        # Campo para matrícula
        ttk.Label(janela_info, text="Digite a matrícula:").pack(pady=5)
        campo_matricula = ttk.Entry(janela_info, width=30)
        campo_matricula.pack(pady=5)

        # Campo para nome
        ttk.Label(janela_info, text="Digite o nome:").pack(pady=5)
        campo_nome = ttk.Entry(janela_info, width=30)
        campo_nome.pack(pady=5)


        def confirmar_dados():
            matricula = campo_matricula.get().strip()
            nome = campo_nome.get().strip()
            
            if not campo_matricula.get().isdigit():
                messagebox.showerror("Erro", "A matrícula deve ser um número válido.")
                return
            
            if not matricula or not nome:
                messagebox.showerror("Erro", "Por favor, preencha todos os campos.")
                return

            # salvando os dados no banco de dados
            aluno = data.Aluno()
            aluno.adicionar_usuario(nome, id_curso_selecionado, matricula, saldo = 0.0)
            messagebox.showinfo(
                "Sucesso",
                f"Usuário criado com sucesso!\nCurso: {curso_selecionado}\nMatrícula: {matricula}\nNome: {nome}"
            )
            janela_info.destroy()

        ttk.Button(janela_info, text="Confirmar", command=confirmar_dados).pack(pady=10)
        ttk.Button(janela_info, text="Cancelar", command=janela_info.destroy).pack(pady=5)

    def salvar_funcionario(self):
        # Cria uma nova janela para coletar informações do usuário
        janela_info = tk.Toplevel(self.root)
        janela_info.title("Informações do Usuário")
        janela_info.geometry("350x200")
        janela_info.resizable(False, False)

        # Campo para matrícula
        ttk.Label(janela_info, text="Digite a matrícula:").pack(pady=5)
        campo_matricula = ttk.Entry(janela_info, width=30)
        campo_matricula.pack(pady=5)

        # Campo para nome
        ttk.Label(janela_info, text="Digite o nome:").pack(pady=5)
        campo_nome = ttk.Entry(janela_info, width=30)
        campo_nome.pack(pady=5)

        # Campo para cargo
        ttk.Label(janela_info, text="Digite o cargo:").pack(pady=5)
        campo_cargo = ttk.Entry(janela_info, width=30)
        campo_cargo.pack(pady=5)

        def confirmar_dados():
            matricula = campo_matricula.get().strip()
            nome = campo_nome.get().strip()
            cargo = campo_cargo.get().strip()

            if not campo_matricula.get().isdigit():
                messagebox.showerror("Erro", "A matrícula deve ser um número válido.")
                return
            
            if not matricula or not nome or not cargo:
                messagebox.showerror("Erro", "Por favor, preencha todos os campos.")
                return

            # salvando os dados no banco de dados
            funcionario = data.Funcionario()
            funcionario.adicionar_funcionario(nome, matricula, cargo)
            messagebox.showinfo(
                "Sucesso",
                f"Usuário criado com sucesso!\nCargo: {cargo}\nMatrícula: {matricula}\nNome: {nome}"
            )
            janela_info.destroy()

        ttk.Button(janela_info, text="Confirmar", command=confirmar_dados).pack(pady=10)
        ttk.Button(janela_info, text="Cancelar", command=janela_info.destroy).pack(pady=5)

    def efetuar_recarga(self):
        messagebox.showinfo(
            "Recarga",
            "Tela de recarga de saldo\n(Em desenvolvimento)"
        )

    def entrar_ru(self):
        messagebox.showinfo(
            "Entrada no RU",
            "Entrada liberada\nSaldo verificado\n(Em desenvolvimento)"
        )

    def visualizar_perfil(self):
        messagebox.showinfo(
            "Perfil",
            "Nome: ---\nMatrícula: ---\nSaldo: ---\n(Em desenvolvimento)"
        )

    def sair(self):
        resposta = messagebox.askyesno(
            "Sair",
            "Deseja realmente encerrar o sistema?"
        )
        if resposta:
            self.root.quit()


if __name__ == "__main__":
    root = tk.Tk()
    app = SistemaRU(root)
    root.mainloop()
