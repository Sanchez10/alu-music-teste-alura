from datetime import datetime, timedelta
from app.models.comentario import Comentario
from app.models.resumo import ResumoSemanal
from app import db
from app.services.classifier import gerar_resumo_llm
import smtplib
from email.mime.text import MIMEText
import os

def gerar_e_enviar_resumo():
    hoje = datetime.utcnow()
    inicio_semana = hoje - timedelta(days=7)

    comentarios = Comentario.query.filter(Comentario.criado_em >= inicio_semana).all()
    textos = [c.texto for c in comentarios]
    
    if not textos:
        print("[RESUMO] Nenhum comentário para resumir.")
        return

    try:
        resumo = gerar_resumo_llm(textos)
    except Exception as e:
        print("[LLM ERROR]", e)
        resumo = "Resumo gerado com LLM falhou. Conteúdo gerado automaticamente: " + " ".join(textos[:3])


    novo_resumo = ResumoSemanal(
        data_inicio=inicio_semana,
        data_fim=hoje,
        resumo=resumo
    )
    db.session.add(novo_resumo)
    db.session.commit()

    destinatario = os.getenv("EMAIL_TO", "equipe@aluramusic.com")
    enviar_email(destinatario, "Resumo Semanal", resumo)

    print("[RESUMO] Resumo semanal gerado e enviado com sucesso.")

def enviar_email(destinatario, assunto, corpo):
    msg = MIMEText(corpo, "plain", "utf-8")
    msg["Subject"] = assunto
    msg["From"] = os.getenv("EMAIL_USER")
    msg["To"] = destinatario

    try:
        with smtplib.SMTP(os.getenv("EMAIL_HOST"), int(os.getenv("EMAIL_PORT"))) as server:
            server.starttls()
            server.login(os.getenv("EMAIL_USER"), os.getenv("EMAIL_PASS"))
            server.send_message(msg)
        print("Email enviado com sucesso.")
    except Exception as e:
        print("Erro ao enviar e-mail:", e)