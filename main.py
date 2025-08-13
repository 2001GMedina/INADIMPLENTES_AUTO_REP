# main.py
import os
import sys
from dotenv import load_dotenv
from mods.logger import setup_logger, get_logger
from mods.sql_server import connect_sql_server, run_query
from mods.email_sender import send_email
from mods.gerar_html import gerar_html_tabela

# --- Setup ---
load_dotenv()
setup_logger()
logger = get_logger()

# Caminho base do projeto
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

try:
    # --- Conectar ao SQL Server ---
    conn = connect_sql_server(os.getenv("CONN_STRING"))

    # --- Primeira query: inadimplentes ---
    sql_path_inad = os.path.join(BASE_DIR, "queries", "inadimplentes.sql")
    with open(sql_path_inad, "r", encoding="utf-8") as f:
        sql_inadimplentes = f.read()
    df_inadimplentes = run_query(conn, sql_inadimplentes)
    logger.info(f"{len(df_inadimplentes)} linhas retornadas da primeira query (inadimplentes).")

    # --- Segunda query: resumo_total ---
    sql_path_total = os.path.join(BASE_DIR, "queries", "resumo_total.sql")
    with open(sql_path_total, "r", encoding="utf-8") as f:
        sql_total = f.read()
    df_total = run_query(conn, sql_total)
    logger.info(f"{len(df_total)} linhas retornadas da segunda query (resumo_total).")

    # --- Terceira query: valor_geral ---
    sql_path_valor = os.path.join(BASE_DIR, "queries", "valor_geral.sql")
    with open(sql_path_valor, "r", encoding="utf-8") as f:
        sql_valor_geral = f.read()
    df_valor_geral = run_query(conn, sql_valor_geral)
    logger.info(f"{len(df_valor_geral)} linhas retornadas da terceira query (valor_geral).")

    # --- Fechar conexão ---
    conn.close()

    # --- Ler template completo uma vez ---
    template_path = os.path.join(BASE_DIR, "utils", "template_email.html")
    with open(template_path, "r", encoding="utf-8") as f:
        template = f.read()

    # --- Gerar HTML das tabelas ---
    html_inadimplentes = gerar_html_tabela(df_inadimplentes, "Resumo de Inadimplentes")
    html_total = gerar_html_tabela(df_total, "Resumo Total")
    html_valor_geral = gerar_html_tabela(df_valor_geral, "Valor Geral")

    # --- Substituir placeholder {{TABELAS}} ---
    resumo_html_final = template.replace(
        "{{TABELAS}}",
        html_inadimplentes + html_total + html_valor_geral
    )

    logger.info("HTML das tabelas gerado com sucesso.")

    # --- Enviar e-mail ---
    send_email("Resumo de Inadimplentes", resumo_html_final)
    logger.info("E-mail enviado com sucesso!")

except Exception as e:
    logger.exception(f"Ocorreu um erro: {e}")
    sys.exit(1)  # <- Garante que o Jenkins marque como FAILED