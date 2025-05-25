# Desintegra
# Processador Sintegra MG

Este projeto é uma ferramenta em Python com interface gráfica (Tkinter) para filtrar registros de arquivos no layout Sintegra MG, preservando as regras de montagem do registro 90. A aplicação permite selecionar modelos de documento fiscal para filtrar e gera um novo arquivo já pronto para entrega ao fisco mineiro.

## Funcionalidades

- Interface gráfica amigável (Tkinter)
- Filtra registros dos modelos desejados (ex: 55, 65, etc)
- Gera novo arquivo no mesmo diretório do original, com sufixo `_filtrado`
- Monta o registro 90 conforme as regras de MG, incluindo:
  - Quantidades de registros: 50, 53, 54, 61, 75 e 99, cada um com 2 dígitos do tipo + 8 dígitos da quantidade (com zeros à esquerda)
  - O dígito final "1" na posição 126
  - Espaço após a inscrição estadual preservado

## Como usar

1. **Clone este repositório**  
   ```bash
   git clone https://github.com/<seu-usuario>/processador-sintegra-mg.git
   cd processador-sintegra-mg
   ```

2. **Instale o Python (3.7+)**  
   Este projeto requer Python 3.7 ou superior.  
   Verifique com:
   ```bash
   python --version
   ```

3. **Execute o programa**
   ```bash
   python processa_sintegra_mg_gui.py
   ```

4. **No programa:**
   - Clique em "Selecionar" para abrir o arquivo Sintegra original
   - O campo de saída será preenchido automaticamente no mesmo diretório (com `_filtrado`)
   - Informe os modelos desejados (exemplo: `55,65`)
   - Clique em "Processar"  
   Pronto! O novo arquivo estará no mesmo local do original.

## Licença

Código livre para uso, modificação e distribuição.

---
> Desenvolvido com auxílio de IA ([GitHub Copilot](https://github.com/features/copilot) / ChatGPT).
