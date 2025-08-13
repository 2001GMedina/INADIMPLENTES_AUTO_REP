def gerar_html_tabela(df, titulo="Tabela"):
    # Formatar valores
    if 'VALOR_ACUMULADO' in df.columns:
        df['VALOR_ACUMULADO'] = df['VALOR_ACUMULADO'].apply(
            lambda x: f"R$ {x:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')
        )
    if 'TOTAL_GERAL' in df.columns:
        df['TOTAL_GERAL'] = df['TOTAL_GERAL'].apply(
            lambda x: f"R$ {x:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')
        )
    if 'VALOR_GERAL' in df.columns:
        df['VALOR_GERAL'] = df['VALOR_GERAL'].apply(
            lambda x: f"R$ {x:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')
        )

    # Gerar HTML da tabela isolada (apenas <h3> + <table>)
    tabela_html = f"<h3>{titulo}</h3>" + df.to_html(index=False, escape=False)
    return tabela_html
