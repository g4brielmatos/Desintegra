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

