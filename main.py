# main.py
import os
from dotenv import load_dotenv
from mods.logger import setup_logger, get_logger
from mods.sql_server import connect_sql_server, run_query
from mods.email_sender import send_email
from mods.gerar_html import gerar_html_tabela

# --- Setup ---
load_dotenv()
setup_logger()
logger = get_logger()

try:
    # --- Conectar ao SQL Server ---
    conn = connect_sql_server(os.getenv("CONN_STRING"))

    # --- Primeira query: inadimplentes ---
    with open("queries/inadimplentes.sql", "r", encoding="utf-8") as f:
        sql_inadimplentes = f.read()
    df_inadimplentes = run_query(conn, sql_inadimplentes)
    logger.info(f"{len(df_inadimplentes)} linhas retornadas da primeira query (inadimplentes).")

    # --- Segunda query: resumo_total ---
    with open("queries/resumo_total.sql", "r", encoding="utf-8") as f:
        sql_total = f.read()
    df_total = run_query(conn, sql_total)
    logger.info(f"{len(df_total)} linhas retornadas da segunda query (resumo_total).")

    # --- Terceira query: valor_geral ---
    with open("queries/valor_geral.sql", "r", encoding="utf-8") as f:
        sql_valor_geral = f.read()
    df_valor_geral = run_query(conn, sql_valor_geral)
    logger.info(f"{len(df_total)} linhas retornadas da segunda query (valor_geral).")

    # --- Fechar conexão ---
    conn.close()

    # --- Ler template completo uma vez ---
    with open("utils/template_email.html", "r", encoding="utf-8") as f:
        template = f.read()

    # --- Gerar HTML das tabelas (apenas h3 + table) ---
    html_inadimplentes = gerar_html_tabela(df_inadimplentes, "Resumo de Inadimplentes")
    html_total = gerar_html_tabela(df_total, "Resumo Total")
    html_valor_geral = gerar_html_tabela(df_valor_geral, "Valor Geral")

    # --- Substituir placeholder {{TABELAS}} por ambas as tabelas ---
    resumo_html_final = template.replace("{{TABELAS}}", html_inadimplentes + html_total + html_valor_geral)

    logger.info("HTML das tabelas gerado com sucesso.")

    # --- Enviar e-mail ---
    send_email("Resumo de Inadimplentes", resumo_html_final)
    logger.info("E-mail enviado com sucesso!")

except Exception as e:
    logger.exception(f"Ocorreu um erro: {e}")
