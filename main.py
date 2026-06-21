# === MODELOS ===

import tkinter as tk
from tkinter import simpledialog, messagebox

class Aluno:
    def __init__(self, nome, matricula, turma, curso):
        self.nome = nome
        self.matricula = matricula
        self.turma = turma
        self.curso = curso
        self.notas = []           # lista de notas por semestre/atividade
        self.atividades = []      # lista de atividades (e notas)
    
    def calcular_media(self):
        total = 0
        count = 0
        for atividade in self.atividades:
            total += atividade['nota']
            count += 1
        if count == 0:
            return 0
        return total / count

    def situacao(self):
        media = self.calcular_media()
        if media > 6:
            return "Aprovado!"
        elif media == 6:
            return "Passou arrastado, mas passou!"
        else:
            return "Reprovado! Deverá refazer tudo de novo."

    def historico(self):
        return {
            'nome': self.nome,
            'matricula': self.matricula,
            'disciplina': [a['disciplina'] for a in self.atividades],
            'curso': self.curso,
            'turma': self.turma,
            'notas': [a['nota'] for a in self.atividades],
            'situacao': self.situacao()
        }

class Disciplina:
    def __init__(self, nome, professor, carga_horaria):
        self.nome = nome
        self.professor = professor
        self.carga_horaria = carga_horaria

# === BANCO DE DADOS SIMPLES ===

alunos = {}         # chave: matricula, valor: objeto Aluno
disciplinas = {}    # chave: nome, valor: objeto Disciplina

# === FUNÇÕES DO SISTEMA COM TKINTER ===

def cadastrar_aluno():
    nome = simpledialog.askstring("Cadastro de Aluno", "Nome do aluno:")
    if nome is None:
        return
    matricula = simpledialog.askstring("Cadastro de Aluno", "Número de matrícula:")
    if matricula is None:
        return
    turma = simpledialog.askstring("Cadastro de Aluno", "Turma:")
    if turma is None:
        return
    curso = simpledialog.askstring("Cadastro de Aluno", "Curso:")
    if curso is None:
        return
    if matricula in alunos:
        messagebox.showinfo("Atenção", "Aluno já cadastrado!")
        return
    aluno = Aluno(nome, matricula, turma, curso)
    alunos[matricula] = aluno
    messagebox.showinfo("Sucesso", "Aluno cadastrado com sucesso!")

def editar_aluno():
    matricula = simpledialog.askstring("Editar Aluno", "Digite o número de matrícula do aluno a ser editado:")
    if matricula is None:
        return
    if matricula not in alunos:
        messagebox.showinfo("Erro", "Aluno não encontrado!")
        return
    novo_nome = simpledialog.askstring("Editar Aluno", "Novo nome do aluno:")
    if novo_nome is None:
        return
    alunos[matricula].nome = novo_nome
    messagebox.showinfo("Sucesso", "Aluno editado com sucesso.")

def cadastrar_disciplina():
    nome = simpledialog.askstring("Cadastro de Disciplina", "Nome da disciplina:")
    if nome is None:
        return
    professor = simpledialog.askstring("Cadastro de Disciplina", "Nome do professor:")
    if professor is None:
        return
    carga_horaria = simpledialog.askstring("Cadastro de Disciplina", "Carga horária (em horas):")
    if carga_horaria is None:
        return
    if nome in disciplinas:
        messagebox.showinfo("Atenção", "Disciplina já cadastrada!")
        return
    disciplina = Disciplina(nome, professor, carga_horaria)
    disciplinas[nome] = disciplina
    messagebox.showinfo("Sucesso", "Disciplina cadastrada com sucesso!")

def editar_disciplina():
    nome = simpledialog.askstring("Editar Disciplina", "Digite o nome da disciplina que deseja editar:")
    if nome is None:
        return
    if nome not in disciplinas:
        messagebox.showinfo("Erro", "Disciplina não encontrada!")
        return
    novo_nome = simpledialog.askstring("Editar Disciplina", "Novo nome da disciplina:")
    if novo_nome is None:
        return
    disciplina = disciplinas.pop(nome)
    disciplina.nome = novo_nome
    disciplinas[novo_nome] = disciplina
    messagebox.showinfo("Sucesso", "Disciplina editada com sucesso.")

def lancar_nota():
    matricula = simpledialog.askstring("Lançar Nota", "Matrícula do aluno:")
    if matricula is None:
        return
    if matricula not in alunos:
        messagebox.showinfo("Erro", "Aluno não encontrado!")
        return
    disciplina = simpledialog.askstring("Lançar Nota", "Disciplina:")
    if disciplina is None:
        return
    nota_str = simpledialog.askstring("Lançar Nota", "Nota:")
    if nota_str is None:
        return
    try:
        nota = float(nota_str)
    except (TypeError, ValueError):
        messagebox.showinfo("Erro", "Nota inválida!")
        return
    semestre = simpledialog.askstring("Lançar Nota", "Semestre:")
    if semestre is None:
        return
    alunos[matricula].notas.append({'disciplina': disciplina, 'nota': nota, 'semestre': semestre})
    messagebox.showinfo("Sucesso", "Nota lançada com sucesso.")

def adicionar_atividade():
    matricula = simpledialog.askstring("Adicionar Atividade", "Matrícula do aluno:")
    if matricula is None:
        return
    if matricula not in alunos:
        messagebox.showinfo("Erro", "Aluno não encontrado!")
        return
    tipo = simpledialog.askstring("Adicionar Atividade", "Tipo de atividade (prova/trabalho/ponto extra):")
    if tipo is None:
        return
    disciplina = simpledialog.askstring("Adicionar Atividade", "Disciplina:")
    if disciplina is None:
        return
    nota_str = simpledialog.askstring("Adicionar Atividade", "Nota da atividade:")
    if nota_str is None:
        return
    try:
        nota = float(nota_str)
    except (TypeError, ValueError):
        messagebox.showinfo("Erro", "Nota inválida!")
        return
    alunos[matricula].atividades.append({'tipo': tipo, 'disciplina': disciplina, 'nota': nota})
    messagebox.showinfo("Sucesso", "Atividade foi adicionada com sucesso.")

def verificar_situacao_aluno():
    matricula = simpledialog.askstring("Verificar Situação do Aluno", "Matrícula do aluno:")
    if matricula is None:
        return
    if matricula not in alunos:
        messagebox.showinfo("Erro", "Aluno não encontrado!")
        return
    aluno = alunos[matricula]
    media = aluno.calcular_media()
    situacao = aluno.situacao()
    messagebox.showinfo("Situação do Aluno", f"Média: {media:.2f}\nSituação: {situacao}")

def verificar_historico_aluno():
    matricula = simpledialog.askstring("Verificar Histórico", "Matrícula do aluno:")
    if matricula is None:
        return
    if matricula not in alunos:
        messagebox.showinfo("Erro", "Aluno não encontrado!")
        return
    historico = alunos[matricula].historico()
    disciplinas_str = ', '.join(historico['disciplina'])
    notas_str = ', '.join(str(n) for n in historico['notas'])
    texto = (
        "=== Histórico do Aluno ===\n"
        f"Nome: {historico['nome']}\n"
        f"Matrícula: {historico['matricula']}\n"
        f"Curso: {historico['curso']}\n"
        f"Turma: {historico['turma']}\n"
        f"Disciplinas: {disciplinas_str}\n"
        f"Notas: {notas_str}\n"
        f"Situação: {historico['situacao']}"
    )
    messagebox.showinfo("Histórico do Aluno", texto)

# === GUI MENU PRINCIPAL ===

def menu_tk():
    root = tk.Tk()
    root.title("Sistema de Gerenciamento de Notas")

    def sair():
        root.destroy()

    # Criação dos botões
    botoes = [
        ("Cadastrar Aluno", cadastrar_aluno),
        ("Editar Aluno", editar_aluno),
        ("Cadastrar Disciplina", cadastrar_disciplina),
        ("Editar Disciplina", editar_disciplina),
        ("Lançar Nota", lancar_nota),
        ("Adicionar Atividade", adicionar_atividade),
        ("Verificar Situação do Aluno", verificar_situacao_aluno),
        ("Verificar Histórico do Aluno", verificar_historico_aluno),
        ("Sair", sair)
    ]

    for idx, (nome, func) in enumerate(botoes):
        btn = tk.Button(root, text=nome, width=35, command=func)
        btn.pack(pady=3)

    root.mainloop()

if __name__ == "__main__":
    menu_tk()