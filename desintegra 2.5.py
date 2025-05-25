import tkinter as tk
from tkinter import filedialog, messagebox
from collections import Counter
import os

def ler_sintegra(arquivo):
    registros = []
    with open(arquivo, encoding='latin-1') as f:
        for linha in f:
            tipo = linha[:2]
            registros.append({'tipo': tipo, 'linha': linha.rstrip('\r\n')})
    return registros

def extrai_modelo(linha, tipo):
    if tipo == '50':
        return linha[40:42]
    elif tipo == '53':
        return linha[40:42]
    elif tipo == '54':
        return linha[16:18]
    elif tipo == '61':
        return linha[38:40]
    else:
        return None

def extrai_codigo_produto(linha, tipo):
    if tipo == '54':
        return linha[37:51].strip()
    elif tipo == '75':
        return linha[18:32].strip()
    else:
        return None

def filtrar_por_modelo(registros, tipos_desejados, modelos_desejados):
    filtrados = []
    codigos_produto_54 = set()
    for r in registros:
        if r['tipo'] in tipos_desejados:
            if r['tipo'] == '61' and len(r['linha']) > 2 and r['linha'][2] == 'R':
                continue
            modelo = extrai_modelo(r['linha'], r['tipo'])
            if modelo in modelos_desejados:
                if r['tipo'] == '54':
                    codigo_produto = extrai_codigo_produto(r['linha'], r['tipo'])
                    codigos_produto_54.add(codigo_produto)
                    filtrados.append({**r, 'modelo': modelo, 'codigo_produto': codigo_produto})
                else:
                    filtrados.append({**r, 'modelo': modelo})
    return filtrados, codigos_produto_54

def filtrar_registros_75_por_codigo(registros, codigos_produto_54):
    filtrados = []
    for r in registros:
        if r['tipo'] == '75':
            codigo_produto = extrai_codigo_produto(r['linha'], r['tipo'])
            if codigo_produto in codigos_produto_54:
                filtrados.append({**r, 'codigo_produto': codigo_produto})
    return filtrados

def obter_prefixo_registro_90(registros):
    for r in registros:
        if r['tipo'] == '90':
            linha = r['linha']
            if ' ' in linha:
                idx = linha.index(' ')
                return linha[:idx+1]
            else:
                return linha[:31] + ' '
    return '90' + ' ' * 29

def cria_registro_90_mg(prefixo, contagem_tipos, total_linhas):
    """
    Monta o registro 90 com pares de 10 caracteres (2 tipo + 8 quantidade), inclusive para o 99,
    e o '1' na posição 126.
    """
    tipos_usados = ['50', '53', '54', '61', '75']
    pares = ''
    for tipo in tipos_usados:
        qtde = contagem_tipos.get(tipo, 0)
        pares += f"{tipo:0>2}{qtde:0>8}"
    bloco99 = f"99{total_linhas:0>8}"
    parcial = prefixo + pares + bloco99
    tam_atual = len(parcial)
    if tam_atual > 125:
        raise Exception(f"O registro 90 ficou maior que 125 caracteres antes do número final: {tam_atual}")
    espacos = 125 - tam_atual
    registro = parcial + (" " * espacos) + "1"
    return registro

def processa_e_salva(entrada, saida, modelos_desejados):
    registros = ler_sintegra(entrada)
    tipos_para_filtrar = ['50', '53', '54', '61']

    cabecalho = [r['linha'] for r in registros[:2]]

    registros_filtrados, codigos_prod_54 = filtrar_por_modelo(registros, tipos_para_filtrar, modelos_desejados)
    registros_75_filtrados = filtrar_registros_75_por_codigo(registros, codigos_prod_54)

    outros_registros = [
        r for idx, r in enumerate(registros)
        if r['tipo'] not in (tipos_para_filtrar + ['75', '90', '99'])
        and idx >= 2
    ]

    todos_registros = (
        cabecalho +
        [r['linha'] for r in registros_filtrados] +
        [r['linha'] for r in registros_75_filtrados] +
        [r['linha'] for r in outros_registros]
    )

    tipos_para_90 = [linha[:2] for linha in todos_registros]
    contagem = Counter(tipos_para_90)
    total_linhas = len(todos_registros) + 1  # +1 pois o próprio 90 entra na contagem

    prefixo_90 = obter_prefixo_registro_90(registros)
    registro_90 = cria_registro_90_mg(prefixo_90, contagem, total_linhas)

    with open(saida, "w", encoding="latin-1") as f:
        for linha in todos_registros:
            f.write(linha + "\n")
        f.write(registro_90 + "\n")

# ===== GUI =====

def selecionar_entrada(entry_entrada, entry_saida):
    filename = filedialog.askopenfilename(title="Selecione o arquivo Sintegra original")
    if filename:
        entry_entrada.delete(0, tk.END)
        entry_entrada.insert(0, filename)
        # Preenche o campo de saída automaticamente
        caminho, nome_arquivo = os.path.split(filename)
        nome, ext = os.path.splitext(nome_arquivo)
        novo_nome = f"{nome}_filtrado{ext}"
        saida_path = os.path.join(caminho, novo_nome)
        entry_saida.delete(0, tk.END)
        entry_saida.insert(0, saida_path)

def selecionar_saida(entry):
    filename = filedialog.asksaveasfilename(title="Salvar como", defaultextension=".txt",
                                            filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
    if filename:
        entry.delete(0, tk.END)
        entry.insert(0, filename)

def processar_gui(entry_entrada, entry_saida, entry_modelos, status_label):
    arquivo_entrada = entry_entrada.get()
    arquivo_saida = entry_saida.get()
    modelos = entry_modelos.get().replace(' ', '').split(',')
    modelos_desejados = set(modelos)
    try:
        processa_e_salva(arquivo_entrada, arquivo_saida, modelos_desejados)
        status_label.config(text="Arquivo processado com sucesso!", fg="green")
        messagebox.showinfo("Sucesso", "Arquivo processado com sucesso!")
    except Exception as e:
        status_label.config(text=f"Erro: {e}", fg="red")
        messagebox.showerror("Erro", f"Ocorreu um erro: {e}")

def main():
    root = tk.Tk()
    root.title("Processador Sintegra MG")

    tk.Label(root, text="Arquivo de entrada:").grid(row=0, column=0, sticky="e")
    entry_entrada = tk.Entry(root, width=50)
    entry_entrada.grid(row=0, column=1)
    entry_saida = tk.Entry(root, width=50)
    entry_saida.grid(row=1, column=1)
    tk.Button(root, text="Selecionar", command=lambda: selecionar_entrada(entry_entrada, entry_saida)).grid(row=0, column=2)

    tk.Label(root, text="Arquivo de saída:").grid(row=1, column=0, sticky="e")
    tk.Button(root, text="Selecionar", command=lambda: selecionar_saida(entry_saida)).grid(row=1, column=2)

    tk.Label(root, text="Modelos desejados (ex: 55,65):").grid(row=2, column=0, sticky="e")
    entry_modelos = tk.Entry(root, width=20)
    entry_modelos.insert(0, "55,65")
    entry_modelos.grid(row=2, column=1, sticky="w")

    status_label = tk.Label(root, text="", fg="green")
    status_label.grid(row=4, column=0, columnspan=3)

    tk.Button(root, text="Processar", width=20,
              command=lambda: processar_gui(entry_entrada, entry_saida, entry_modelos, status_label)).grid(row=3, column=0, columnspan=3, pady=10)

    root.mainloop()

if __name__ == "__main__":
    main()
