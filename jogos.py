from tkinter import ttk
from tkinter import messagebox
import json
import tkinter as tk

generos_validos = ["Ação e aventura", "FPS", "JRPG", "RPG de ação", "RPG tático"]
plataformas_validas = ["PC", "Nintendo", "PlayStation", "Xbox"]
faixas_de_preco_validas = ["0-50", "50-100", "100-200", "Mais de 200"]
tempos_medio_validos = ["Curto", "Longo", "Muito longo"]

def ler_dados():
    with open("jogos.json", "r", encoding="utf-8") as arquivo_json:
        dados = json.load(arquivo_json)
    return dados

def imprimir_dados(dados):
    jogos = dados.get("jogos", [])
    for jogo in jogos:
        print("Título:", jogo["titulo"])
        print("Gênero:", jogo["genero"])
        print("Plataformas:", ", ".join(jogo["plataformas"]))
        print("Preço:", jogo["preco"])
        print("Tempo Médio para Zerar:", jogo["tempo_medio_para_zerar"])
        print()

def criar_interface():
    janela = tk.Tk()
    janela.title("GameAdvisor")
    janela.geometry("400x400")

    label_nome = tk.Label(janela, text="Nome:")
    label_nome.pack()
    entry_nome = tk.Entry(janela)
    entry_nome.pack()
    entry_nome.config(width=30)

    label_idade = tk.Label(janela, text="Idade:")
    label_idade.pack()
    entry_idade = tk.Entry(janela)
    entry_idade.pack()
    entry_idade.config(width=30)

    label_genero = tk.Label(janela, text="Gênero favorito:")
    label_genero.pack()
    generos = ["Ação e aventura", "FPS", "JRPG", "RPG de ação", "RPG tático"]
    genero_combobox = ttk.Combobox(janela, values=generos)
    genero_combobox.pack()
    genero_combobox.config(width=30)

    label_plataforma = tk.Label(janela, text="Plataforma:")
    label_plataforma.pack()
    plataformas = ["PC", "Nintendo", "PlayStation", "Xbox"]
    plataforma_combobox = ttk.Combobox(janela, values=plataformas)
    plataforma_combobox.pack()
    plataforma_combobox.config(width=30)

    label_faixa_de_preco = tk.Label(janela, text="Faixa de Preço:")
    label_faixa_de_preco.pack()
    faixas_de_preco = ["0-50", "50-100", "100-200", "mais de 200"]
    faixa_de_preco_combobox = ttk.Combobox(janela, values=faixas_de_preco)
    faixa_de_preco_combobox.pack()
    faixa_de_preco_combobox.config(width=30)

    label_tempo_medio = tk.Label(janela, text="Tempo Médio para Zerar:")
    label_tempo_medio.pack()
    tempos_medio = ["Curto", "Longo", "Muito longo"]
    tempo_medio_combobox = ttk.Combobox(janela, values=tempos_medio)
    tempo_medio_combobox.pack()
    tempo_medio_combobox.config(width=30)

    botao_coletar = tk.Button(janela, text="Enviar", command=lambda: coletar_informacoes(entry_nome, entry_idade, genero_combobox, plataforma_combobox, faixa_de_preco_combobox, tempo_medio_combobox, label_resultado))
    botao_coletar.pack()
    botao_coletar.config(padx=10, pady=5)
    botao_coletar.config(fg="white")
    botao_coletar.config(bg="blue")

    label_resultado = tk.Label(janela, text="")
    label_resultado.pack()

    janela.mainloop()

def coletar_informacoes(entry_nome, entry_idade, genero_combobox, plataforma_combobox, faixa_de_preco_combobox, tempo_combobox, label_resultado):
    nome = entry_nome.get()
    idade = entry_idade.get()
    genero = genero_combobox.get()
    plataforma = plataforma_combobox.get()
    faixa_de_preco = faixa_de_preco_combobox.get()
    tempo_medio = tempo_combobox.get()

    if genero not in generos_validos:
        messagebox.showerror("Erro", "Gênero inválido")
        return

    if plataforma not in plataformas_validas:
        messagebox.showerror("Erro", "Plataforma inválida")
        return

    if faixa_de_preco not in faixas_de_preco_validas:
        messagebox.showerror("Erro", "Faixa de preço inválida")
        return

    if tempo_medio not in tempos_medio_validos:
        messagebox.showerror("Erro", "Tempo médio inválido")
        return

    mensagem = f"Nome: {nome}\nIdade: {idade}\nGênero: {genero}\nPlataforma: {plataforma}\nFaixa de Preço: {faixa_de_preco}\nTempo Médio para Zerar: {tempo_medio}"
    print(mensagem)

dados = ler_dados()
imprimir_dados(dados)

criar_interface()
