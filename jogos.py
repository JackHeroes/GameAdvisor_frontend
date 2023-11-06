from tkinter import messagebox
from tkinter import ttk
import json
import tkinter
import random  

generos_validos = ["Ação e aventura", "FPS", "JRPG", "RPG de ação", "RPG tático"]
plataformas_validas = ["PC", "Nintendo", "PlayStation", "Xbox"]
faixas_de_preco_validas = ["Até 50 reais", "Até 100 reais", "Até 200 reais", "Até 400 reais"]
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
    generos = ["Ação e aventura", "FPS", "JRPG", "RPG de ação", "RPG tático"]
    genero_combobox = ttk.Combobox(janela, values=generos)
    genero_combobox.pack()
    genero_combobox.config(width=30)

    label_plataforma = tkinter.Label(janela, text="Plataforma:")
    label_plataforma.pack()
    plataformas = ["PC", "Nintendo", "PlayStation", "Xbox"]
    plataforma_combobox = ttk.Combobox(janela, values=plataformas)
    plataforma_combobox.pack()
    plataforma_combobox.config(width=30)

    label_faixa_de_preco = tkinter.Label(janela, text="Faixa de Preço:")
    label_faixa_de_preco.pack()
    faixas_de_preco = ["Até 50 reais", "Até 100 reais", "Até 200 reais", "Até 400 reais"]
    faixa_de_preco_combobox = ttk.Combobox(janela, values=faixas_de_preco)
    faixa_de_preco_combobox.pack()
    faixa_de_preco_combobox.config(width=30)

    label_tempo_medio = tkinter.Label(janela, text="Tempo Médio para Zerar:")
    label_tempo_medio.pack()
    tempos_medio = ["Curto", "Longo", "Muito longo"]
    tempo_medio_combobox = ttk.Combobox(janela, values=tempos_medio)
    tempo_medio_combobox.pack()
    tempo_medio_combobox.config(width=30)

    botao_coletar = tkinter.Button(janela, text="Enviar", command=lambda: coletar_informacoes(entry_nome, entry_idade, genero_combobox, plataforma_combobox, faixa_de_preco_combobox, tempo_medio_combobox, label_resultado))
    botao_coletar.pack()
    botao_coletar.config(padx=10, pady=5)
    botao_coletar.config(fg="white")
    botao_coletar.config(bg="blue")

    label_resultado = tkinter.Label(janela, text="")
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

    dados = ler_dados()
    jogador = {
        'genero_preferido': genero,
        'plataforma': plataforma,
        'faixa_de_preco': faixa_de_preco,
        'tempo_medio': tempo_medio
    }

    jogos_recomendados = recomendar_jogos(dados, jogador)

    resultado_text = "Jogo Recomendado:\n"
    jogo_recomendado = jogos_recomendados[0]
    resultado_text += jogo_recomendado["titulo"]

    label_resultado.config(text=resultado_text)

def calcular_compatibilidade(jogo, jogador):
    faixas_de_preco = {
        "Até 50 reais": 50,
        "Até 100 reais": 100,
        "Até 200 reais": 200,
        "Até 400 reais": 400
    }

    tempos_medios = {
        "Curto": (0, 30),
        "Longo": (31, 60),
        "Muito longo": (61, 200)
    }
    
    if jogo['genero'] != jogador['genero_preferido']:
        return 0 

    if jogador['plataforma'] not in jogo['plataformas']:
        return 0 

    pontuacao = 0

    preco = jogo['preco']
    if preco <= faixas_de_preco.get(jogador['faixa_de_preco'], 0):
        pontuacao += 1

    tempo_medio = jogo['tempo_medio_para_zerar']
    intervalo_tempo = tempos_medios.get(jogador['tempo_medio'], (0, 0))

    if intervalo_tempo[0] <= tempo_medio <= intervalo_tempo[1]:
        pontuacao += 1

    return pontuacao

def recomendar_jogos(dados, jogador):
    jogos = dados.get("jogos", [])
    jogos_com_pontuacao = []

    for jogo in jogos:
        pontuacao = calcular_compatibilidade(jogo, jogador)
        if pontuacao > 0:
            jogos_com_pontuacao.append((jogo, pontuacao))

    jogos_com_pontuacao.sort(key=lambda x: x[1], reverse=True)

    maior_pontuacao = jogos_com_pontuacao[0][1]

    jogos_melhores = [jogo for jogo, pontuacao in jogos_com_pontuacao if pontuacao == maior_pontuacao]

    jogo_recomendado = random.choice(jogos_melhores)

    return [jogo_recomendado]

criar_interface()
