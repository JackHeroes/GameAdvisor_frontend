from tkinter import messagebox, ttk
import json
import random
import tkinter

janela = None
generos_validos = ["Ação e aventura", "FPS", "RPG"]
plataformas_validas = ["PC", "Nintendo", "PlayStation", "Xbox"]
faixas_de_preco_validas = ["Até 100 reais", "Até 200 reais", "Até 400 reais"]
tempos_medio_validos = ["Curto", "Longo", "Muito longo"]

def ler_dados():

    with open("jogos.json", "r", encoding="utf-8") as arquivo:
        dados = json.load(arquivo)
    return dados

def criar_interface():

    global janela
    janela = tkinter.Tk()
    janela.title("GameAdvisor")
    janela.geometry("400x400")

    frame_formulario = tkinter.Frame(janela)
    frame_formulario.pack()

    label_nome = tkinter.Label(frame_formulario, text="Nome:")
    label_nome.pack()
    entry_nome = tkinter.Entry(frame_formulario)
    entry_nome.pack()
    entry_nome.config(width=30)

    label_idade = tkinter.Label(frame_formulario, text="Idade:")
    label_idade.pack()
    entry_idade = tkinter.Entry(frame_formulario)
    entry_idade.pack()
    entry_idade.config(width=30)

    label_genero = tkinter.Label(frame_formulario, text="Gênero favorito:")
    label_genero.pack()
    generos = generos_validos
    genero_combobox = ttk.Combobox(frame_formulario, values=generos, state="readonly", textvariable=generos)
    genero_combobox.pack()
    genero_combobox.config(width=30)

    label_plataforma = tkinter.Label(frame_formulario, text="Plataforma:")
    label_plataforma.pack()
    plataformas = plataformas_validas
    plataforma_combobox = ttk.Combobox(frame_formulario, values=plataformas, state="readonly", textvariable=plataformas)
    plataforma_combobox.pack()
    plataforma_combobox.config(width=30)

    label_faixa_de_preco = tkinter.Label(frame_formulario, text="Faixa de preço:")
    label_faixa_de_preco.pack()
    faixas_de_preco = faixas_de_preco_validas
    faixa_de_preco_combobox = ttk.Combobox(frame_formulario, values=faixas_de_preco, state="readonly", textvariable=faixas_de_preco)
    faixa_de_preco_combobox.pack()
    faixa_de_preco_combobox.config(width=30)

    label_tempo_medio = tkinter.Label(frame_formulario, text="Tempo médio para zerar:")
    label_tempo_medio.pack()
    tempos_medio = tempos_medio_validos
    tempo_medio_combobox = ttk.Combobox(frame_formulario, values=tempos_medio, state="readonly", textvariable=tempos_medio)
    tempo_medio_combobox.pack()
    tempo_medio_combobox.config(width=30)

    botao_coletar = tkinter.Button(frame_formulario, text="Enviar", command=lambda: coletar_informacoes(entry_nome, entry_idade, genero_combobox, plataforma_combobox, faixa_de_preco_combobox, tempo_medio_combobox))
    botao_coletar.pack()
    botao_coletar.config(bg="blue")
    botao_coletar.config(fg="white")
    botao_coletar.config(padx=10, pady=5)

    janela.mainloop()

def coletar_informacoes(entry_nome, entry_idade, genero_combobox, plataforma_combobox, faixa_de_preco_combobox, tempo_medio_combobox):
    campos = {
        'nome': entry_nome.get(),
        'idade': entry_idade.get(),
        'genero': genero_combobox.get(),
        'plataforma': plataforma_combobox.get(),
        'faixa_de_preco': faixa_de_preco_combobox.get(),
        'tempo_medio': tempo_medio_combobox.get()
    }

    for campo, valor in campos.items():
        if not valor:
            messagebox.showerror("Erro", f"{campo} é um campo obrigatório")
            return
        elif campo == 'genero' and valor not in generos_validos:
            messagebox.showerror("Erro", "Gênero inválido")
            return
        elif campo == 'plataforma' and valor not in plataformas_validas:
            messagebox.showerror("Erro", "Plataforma inválida")
            return
        elif campo == 'faixa_de_preco' and valor not in faixas_de_preco_validas:
            messagebox.showerror("Erro", "Faixa de preço inválida")
            return
        elif campo == 'tempo_medio' and valor not in tempos_medio_validos:
            messagebox.showerror("Erro", "Tempo médio inválido")
            return

    dados = ler_dados()
    jogador = {
        'genero_preferido': campos['genero'],
        'plataforma': campos['plataforma'],
        'faixa_de_preco': campos['faixa_de_preco'],
        'tempo_medio': campos['tempo_medio']
    }

    jogo_recomendado = recomendar_jogo(dados, jogador)
    mostrar_recomendacao(janela, jogo_recomendado)

def recomendar_jogo(dados, jogador):

    jogos = dados.get("jogos")
    jogos_compativeis = []

    for jogo in jogos:
        if calcular_compatibilidade(jogo, jogador):
            jogos_compativeis.append(jogo)

    if jogos_compativeis:
        jogo_recomendado = random.choice(jogos_compativeis)
        return jogo_recomendado
    else:
        return None

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

def mostrar_recomendacao(janela, jogo_recomendado):
    
    for widget in janela.winfo_children():
        widget.pack_forget()

    frame_recomendacao = tkinter.Frame(janela)  
    frame_recomendacao.pack()

    label_recomendacao = tkinter.Label(frame_recomendacao, text="Jogo recomendado:")
    label_recomendacao.pack()

    if jogo_recomendado is not None:
        resultado_text = jogo_recomendado["titulo"]
    else:
        resultado_text = "Nenhum jogo compatível com o perfil enviado"

    label_resultado = tkinter.Label(frame_recomendacao, text=resultado_text)
    label_resultado.pack()

    botao_voltar = tkinter.Button(frame_recomendacao, text="Solicitar outra recomendação", command=lambda: reiniciar(janela))
    botao_voltar.pack()
    botao_voltar.config(bg="blue")
    botao_voltar.config(fg="white")
    botao_voltar.config(padx=10, pady=5)

def reiniciar(janela):
    janela.destroy()
    criar_interface()

criar_interface()
