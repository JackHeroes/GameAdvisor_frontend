from tkinter import messagebox
from tkinter import ttk
import json
import random  
import tkinter

generos_validos = ["Ação e aventura", "FPS", "JRPG", "RPG de ação", "RPG tático"]
plataformas_validas = ["PC", "Nintendo", "PlayStation", "Xbox"]
faixas_de_preco_validas = ["Até 100 reais", "Até 200 reais", "Até 400 reais"]
tempos_medio_validos = ["Curto", "Longo", "Muito longo"]

def ler_dados():
    with open("jogos.json", "r", encoding="utf-8") as arquivo_json:
        dados = json.load(arquivo_json)
    return dados

def criar_interface():
    janela = tkinter.Tk()  
    janela.title("GameAdvisor")
    janela.geometry("400x400")

    label_nome = tkinter.Label(janela, text="Nome:")
    label_nome.pack()
    entry_nome = tkinter.Entry(janela)
    entry_nome.pack()
    entry_nome.config(width=30)

    label_idade = tkinter.Label(janela, text="Idade:")
    label_idade.pack()
    entry_idade = tkinter.Entry(janela)
    entry_idade.pack()
    entry_idade.config(width=30)

    label_genero = tkinter.Label(janela, text="Gênero favorito:")
    label_genero.pack()
    generos = generos_validos
    genero_combobox = ttk.Combobox(janela, values=generos)
    genero_combobox.pack()
    genero_combobox.config(width=30)

    label_plataforma = tkinter.Label(janela, text="Plataforma:")
    label_plataforma.pack()
    plataformas = plataformas_validas
    plataforma_combobox = ttk.Combobox(janela, values=plataformas)
    plataforma_combobox.pack()
    plataforma_combobox.config(width=30)

    label_faixa_de_preco = tkinter.Label(janela, text="Faixa de Preço:")
    label_faixa_de_preco.pack()
    faixas_de_preco = faixas_de_preco_validas
    faixa_de_preco_combobox = ttk.Combobox(janela, values=faixas_de_preco)
    faixa_de_preco_combobox.pack()
    faixa_de_preco_combobox.config(width=30)

    label_tempo_medio = tkinter.Label(janela, text="Tempo Médio para Zerar:")
    label_tempo_medio.pack()
    tempos_medio = tempos_medio_validos
    tempo_medio_combobox = ttk.Combobox(janela, values=tempos_medio)
    tempo_medio_combobox.pack()
    tempo_medio_combobox.config(width=30)

    botao_coletar = tkinter.Button(janela, text="Enviar", command=lambda: coletar_informacoes(genero_combobox, plataforma_combobox, faixa_de_preco_combobox, tempo_medio_combobox, label_resultado))
    botao_coletar.pack()
    botao_coletar.config(bg="blue")
    botao_coletar.config(fg="white")
    botao_coletar.config(padx=10, pady=5)

    label_resultado = tkinter.Label(janela, text="")
    label_resultado.pack()

    janela.mainloop()

def coletar_informacoes(genero_combobox, plataforma_combobox, faixa_de_preco_combobox, tempo_medio_combobox, label_resultado):
    genero = genero_combobox.get()
    plataforma = plataforma_combobox.get()
    faixa_de_preco = faixa_de_preco_combobox.get()
    tempo_medio = tempo_medio_combobox.get()

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

    dados = ler_dados()
    jogador = {
        'genero_preferido': genero,
        'plataforma': plataforma,
        'faixa_de_preco': faixa_de_preco,
        'tempo_medio': tempo_medio
    }

    jogo_recomendado = recomendar_jogo(dados, jogador)

    resultado_text = "Jogo Recomendado:\n"
    resultado_text += jogo_recomendado["titulo"]

    label_resultado.config(text=resultado_text)

def recomendar_jogo(dados, jogador):
    jogos = dados.get("jogos", [])
    jogos_compativeis = []

    for jogo in jogos:
        if calcular_compatibilidade(jogo, jogador):
            jogos_compativeis.append(jogo)

    jogo_recomendado = random.choice(jogos_compativeis)
    return jogo_recomendado

def calcular_compatibilidade(jogo, jogador):
    faixas_de_preco = {
        "Até 100 reais": 100,
        "Até 200 reais": 200,
        "Até 400 reais": 400
    }

    tempos_medios = {
        "Curto": (0, 30),
        "Longo": (31, 60),
        "Muito longo": (61, 200)
    }

    if jogador['genero_preferido'] in jogo['genero'] and jogador['plataforma'] in jogo['plataformas']:
        faixa_preco = jogo['preco']
        faixa_preco_jogador = faixas_de_preco.get(jogador['faixa_de_preco'])
        tempo_medio = jogo['tempo_medio_para_zerar']
        tempo_medio_jogador = tempos_medios.get(jogador['tempo_medio'])

        if faixa_preco <= faixa_preco_jogador and tempo_medio_jogador[0] <= tempo_medio <= tempo_medio_jogador[1]:
            return True

    return False

criar_interface()
