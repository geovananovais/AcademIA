"""
app.py — Servidor Flask do AcademIA
"""
from estatisticas import calcular_resumo_progresso
import os
import secrets
from datetime import date
from dotenv import load_dotenv
from flask import (
    Flask, jsonify, render_template,
    request, send_from_directory, session,
)
from werkzeug.utils import secure_filename

from bot import Bot
from database import Database

load_dotenv()

app = Flask(__name__, template_folder=".")
# A chave da sessão vem do .env (nunca fica no código).
# Se não estiver definida, gera uma aleatória (as sessões caem ao reiniciar).
app.secret_key = os.getenv("SECRET_KEY") or secrets.token_hex(32)

db = Database()
bot = Bot()

PASTA_FOTOS = "fotos"
os.makedirs(PASTA_FOTOS, exist_ok=True)


def usuario_atual():
    return session.get("usuario_id", "anonimo")


def calcular_nivel(total_treinos):
    """Nível sobe a cada 5 treinos."""
    return max(1, (total_treinos // 5) + 1)


# ── Login ─────────────────────────────────────────────────────────────────────

@app.route("/login", methods=["POST"])
def login():
    dados = request.get_json()
    nome_usuario = dados.get("usuario", "").strip().lower().replace(" ", "_")
    if not nome_usuario:
        return jsonify({"erro": "Nome inválido"}), 400
    session["usuario_id"] = nome_usuario
    session["nome_exibicao"] = dados.get("usuario", "").strip()
    return jsonify({"status": "ok", "usuario": nome_usuario})


@app.route("/logout", methods=["POST"])
def logout():
    session.clear()
    return jsonify({"status": "ok"})


@app.route("/sessao_atual")
def sessao_atual():
    uid = session.get("usuario_id")
    nome = session.get("nome_exibicao", "")
    return jsonify({"logado": uid is not None, "usuario": uid, "nome": nome})


# ── Página principal ──────────────────────────────────────────────────────────

@app.route("/")
def home():
    return render_template("index.html")


# ── Chat ──────────────────────────────────────────────────────────────────────

@app.route("/carregar_historico_chat")
def carregar_historico_chat():
    uid = usuario_atual()
    historico = db.carregar_historico(uid)
    mensagens = [
        {"role": m["role"], "content": m["content"]}
        for m in historico
        if m["role"] in ("user", "assistant") and m.get("content")
    ]
    return jsonify({"mensagens": mensagens})


@app.route("/enviar_mensagem", methods=["POST"])
def enviar_mensagem():
    uid = usuario_atual()
    dados = request.get_json()
    mensagem_usuario = dados.get("mensagem", "")

    historico = db.carregar_historico(uid)
    resposta_bot = bot.responder(mensagem_usuario, historico)

    # 1. Tenta extrair a avaliação física
    avaliacao = bot.extrair_avaliacao(resposta_bot)
    if avaliacao:
        if "data" not in avaliacao:
            avaliacao["data"] = str(date.today())
        db.salvar_avaliacao(uid, avaliacao)

    # 2. Captura o plano de treino customizado enviado pela IA
    plano_gerado = bot.extrair_plano(resposta_bot)
    if plano_gerado:
        db.salvar_plano_treino(uid, plano_gerado)

    resposta_limpa = bot.limpar_marcador(resposta_bot)

    historico.append({"role": "user", "content": mensagem_usuario})
    historico.append({"role": "assistant", "content": resposta_limpa})
    db.salvar_historico(uid, historico)

    return jsonify({"resposta": resposta_limpa})


@app.route("/obter_plano_customizado")
def obter_plano_customizado():
    uid = usuario_atual()
    plano = db.carregar_plano_treino(uid)
    return jsonify({"plano": plano})


# ── Concluir treino ───────────────────────────────────────────────────────────

@app.route("/concluir_treino", methods=["POST"])
def concluir_treino():
    uid = usuario_atual()
    dados = request.get_json()
    treino = dados.get("treino", "A")
    
    # 1. Pega a nota enviada pelo Javascript
    nota = dados.get("nota", 5)

    # Define a string do dia atual
    hoje_str = date.today().strftime('%d/%m/%Y')

    # 2. Salva a nota real recebida no dicionário de avaliação
    avaliacao = {
        "data": hoje_str,
        "nota": int(nota),
        "treino": treino
    }
    db.salvar_avaliacao(uid, avaliacao)

    # Inserir a confirmação no histórico do chat para manter consistência
    historico = db.carregar_historico(uid)
    historico.append({"role": "user", "content": f"Concluí o Treino {treino} pela aba de Planos com nota {nota}."})
    historico.append({"role": "assistant", "content": f"Sensacional! Registrei seu Treino {treino} de hoje ({hoje_str}) com nota {nota}/5 com sucesso por aqui! 💪 O seu gráfico de progresso já foi atualizado."})
    db.salvar_historico(uid, historico)

    # Calcula novo nível
    avaliacoes = db.carregar_avaliacoes(uid)
    total = len(avaliacoes)
    nivel = calcular_nivel(total)

    return jsonify({
        "status": "ok",
        "totalTreinos": total,
        "nivel": nivel,
        "mensagem": f"Treino {treino} concluído! 💪"
    })


# ── Perfil ────────────────────────────────────────────────────────────────────

@app.route("/carregar_perfil")
def carregar_perfil():
    return jsonify(db.carregar_perfil(usuario_atual()))


@app.route("/salvar_perfil", methods=["POST"])
def salvar_perfil():
    uid = usuario_atual()
    dados = request.get_json()
    perfil_atual = db.carregar_perfil(uid)
    perfil_atual.update(dados)
    db.salvar_perfil(uid, perfil_atual)
    return jsonify({"status": "ok"})


# ── Foto de perfil ────────────────────────────────────────────────────────────

@app.route("/upload_foto", methods=["POST"])
def upload_foto():
    if "foto" not in request.files:
        return jsonify({"erro": "Nenhum arquivo"}), 400
    arquivo = request.files["foto"]
    uid = usuario_atual()
    nome_seguro = f"{uid}_{secure_filename(arquivo.filename)}"
    caminho = os.path.join(PASTA_FOTOS, nome_seguro)
    arquivo.save(caminho)
    perfil = db.carregar_perfil(uid)
    perfil["foto"] = nome_seguro
    db.salvar_perfil(uid, perfil)
    return jsonify({"caminho": nome_seguro})


@app.route("/fotos/<nome_arquivo>")
def servir_foto(nome_arquivo):
    return send_from_directory(PASTA_FOTOS, nome_arquivo)


# ── Progresso ─────────────────────────────────────────────────────────────────

@app.route("/dados_progresso")
def dados_progresso():
    uid = usuario_atual()
    avaliacoes = db.carregar_avaliacoes(uid)
    resumo = calcular_resumo_progresso(avaliacoes)
    resumo["avaliacoes"] = avaliacoes
    resumo["nivel"] = calcular_nivel(resumo["totalTreinos"])
    resumo["proximoNivel"] = calcular_nivel(resumo["totalTreinos"]) * 5
    return jsonify(resumo)


# ── Inicialização ─────────────────────────────────────────────────────────────

if __name__ == "__main__":
    debug = os.getenv("FLASK_DEBUG", "0") == "1"
    app.run(debug=debug, port=5001)
