"""
bot.py — O cérebro do AcademIA
Usando OpenAI (gpt-4o-mini) com datas dinâmicas no padrão brasileiro (DD-MM-AAAA),
mas salvando internamente em formato universal (AAAA-MM-DD) para não quebrar o gráfico.
"""

import os
import re
import json
from datetime import date, timedelta
from openai import OpenAI
from dotenv import load_dotenv
from prompts import SYSTEM_PROMPT
from exercicios import get_contexto_exercicios, get_exercicios_por_local

load_dotenv()


class Bot:
    def __init__(self):
        self.cliente = OpenAI(
            api_key=os.getenv("OPENAI_API_KEY")
        )
        self.modelo = "gpt-4o-mini"

    def _detectar_local_treino(self, historico: list) -> str:
        for msg in historico:
            if msg.get("role") == "user":
                conteudo = msg.get("content", "").lower()
                if "academia" in conteudo:
                    return "academia"
                if "casa" in conteudo:
                    return "casa"
        return None

    def responder(self, mensagem_usuario, historico):
        try:
            local = self._detectar_local_treino(historico)

            if local:
                contexto_exercicios = get_contexto_exercicios(local)
                system_completo = SYSTEM_PROMPT + "\n\n" + contexto_exercicios
            else:
                system_completo = SYSTEM_PROMPT

            # Calcula as datas no momento do envio
            hoje = date.today()
            ontem = hoje - timedelta(days=1)
            anteontem = hoje - timedelta(days=2)

            # Formata as datas no padrão brasileiro DD-MM-AAAA
            hoje_br = hoje.strftime('%d-%m-%Y')
            ontem_br = ontem.strftime('%d-%m-%Y')
            anteontem_br = anteontem.strftime('%d-%m-%Y')

            # Regra dinâmica adaptada para o padrão do Brasil
            instrucao_data = (
                f"\n\n════════════════════════════════════════\n"
                f"REGRA CRÍTICA DE REGISTRO DE TREINO:\n"
                f"Sempre que o usuário confirmar um treino, você DEVE incluir obrigatoriamente no FINAL da resposta o marcador oculto:\n"
                f"[AVALIACAO: nota=X treino=Y data=DD-MM-AAAA]\n"
                f"- Considere estritamente que HOJE é {hoje.strftime('%d/%m/%Y')}.\n"
                f"- Se o usuário não citar dia, ou disser 'hoje', use data={hoje_br}.\n"
                f"- Se disser 'ontem', use data={ontem_br}.\n"
                f"- Se disser 'anteontem', use data={anteontem_br}.\n"
                f"- Se disser uma data específica (ex: '02/07/2026'), converta rigidamente para o formato data=DD-MM-AAAA.\n"
            )
            system_completo += instrucao_data

            mensagens = [{"role": "system", "content": system_completo}]
            mensagens.extend(historico)
            
            conteudo_usuario = mensagem_usuario
            palavras_chave = ["treino", "fiz", "conclui", "concluí", "nota", "1", "2", "3", "4", "5", "/", "ontem", "anteontem"]
            
            if any(palavra in mensagem_usuario.lower() for palavra in palavras_chave):
                conteudo_usuario += "\n\n(Lembrete de sistema: Lembre-se de gerar a tag [AVALIACAO: nota=X treino=Y data=DD-MM-AAAA] no final, incluindo a data retroativa no formato brasileiro se eu tiver mencionado uma)."

            mensagens.append({"role": "user", "content": conteudo_usuario})

            print(f"[AcademIA] 🤖 Processando sua mensagem...")
            
            resposta = self.cliente.chat.completions.create(
                model=self.modelo,
                messages=mensagens,
                max_tokens=600,
                temperature=0.3
            )

            texto = resposta.choices[0].message.content
            print(f"[AcademIA] 💬 Texto gerado pela IA (incluindo tag oculta):\n{texto}\n")
            return texto

        except Exception as erro:
            print(f"[AcademIA] ❌ Erro na função responder: {erro}")
            return "Desculpe, tive um problema para processar essa resposta. Tente novamente."

    def extrair_avaliacao(self, texto_resposta):
        try:
            padrao_tag = r"\[AVALIA[CÇ][AÃ]O:(.*?)\]"
            tag_match = re.search(padrao_tag, texto_resposta, re.IGNORECASE)
            
            if tag_match:
                conteudo = tag_match.group(1)
                
                nota_match = re.search(r"nota\s*[=:]\s*(\d)", conteudo, re.IGNORECASE)
                treino_match = re.search(r"treino\s*[=:]\s*([a-zA-Z])", conteudo, re.IGNORECASE)
                data_match = re.search(r"data\s*[=:]\s*([\d]{2}-[\d]{2}-[\d]{2,4})", conteudo, re.IGNORECASE)
                
                if nota_match and treino_match:
                    dados = {
                        "nota": int(nota_match.group(1)),
                        "treino": treino_match.group(1).upper()
                    }
                    
                    if data_match:
                        data_br = data_match.group(1)
                        # Traduz DD-MM-AAAA para AAAA-MM-DD para o gráfico funcionar!
                        partes = data_br.split('-')
                        if len(partes) == 3:
                            dados["data"] = f"{partes[2]}-{partes[1]}-{partes[0]}"
                        else:
                            dados["data"] = data_br
                    
                    print(f"[AcademIA] 🎯 TAG LIDA E TRADUZIDA PARA O GRÁFICO: {dados}")
                    return dados
                    
            print("[AcademIA] ⚠️ Nenhuma avaliação capturada no texto.")
            return None
        except Exception as e:
            print(f"[AcademIA] ❌ Erro ao extrair avaliação: {e}")
            return None

    def extrair_plano(self, texto_resposta):
        """
        Lê o marcador oculto [PLANO: {...}] gerado pela IA, valida os nomes
        dos exercícios contra o catálogo real (exercicios.py) e devolve um
        dicionário já enriquecido com grupo muscular, séries/reps e o ID do
        vídeo do YouTube — nunca confiamos em dados que a IA "inventou".
        """
        try:
            inicio_tag = texto_resposta.find("[PLANO:")
            if inicio_tag == -1:
                return None

            inicio_json = texto_resposta.find("{", inicio_tag)
            if inicio_json == -1:
                return None

            # raw_decode lida corretamente com chaves aninhadas (diferente de regex)
            decoder = json.JSONDecoder()
            plano_bruto, _fim_json = decoder.raw_decode(texto_resposta, inicio_json)

            dias = plano_bruto.get("dias")
            local = str(plano_bruto.get("local", "")).lower().strip()
            treinos_nomes = plano_bruto.get("treinos", {})

            if not isinstance(treinos_nomes, dict) or not local:
                print("[AcademIA] ⚠️ Plano sem 'local' ou 'treinos' válidos, ignorando.")
                return None

            catalogo = get_exercicios_por_local(local)
            catalogo_por_nome = {e["nome"]: e for e in catalogo}

            treinos_enriquecidos = {}
            for letra, nomes in treinos_nomes.items():
                if not isinstance(nomes, list):
                    continue
                lista = []
                for nome in nomes:
                    exercicio = catalogo_por_nome.get(nome)
                    if not exercicio:
                        print(f"[AcademIA] ⚠️ Exercício '{nome}' não encontrado no catálogo de {local}, descartado.")
                        continue
                    video_match = re.search(r"[?&]v=([\w-]+)", exercicio.get("video", ""))
                    lista.append({
                        "nome": exercicio["nome"],
                        "grupo": exercicio["grupo"],
                        "series_reps": exercicio["series_reps"],
                        "videoId": video_match.group(1) if video_match else "",
                    })
                if lista:
                    treinos_enriquecidos[letra.upper().strip()] = lista

            if not treinos_enriquecidos:
                print("[AcademIA] ⚠️ Nenhum exercício válido encontrado no plano, ignorando.")
                return None

            plano_final = {
                "dias": dias,
                "local": local,
                "treinos": treinos_enriquecidos,
            }
            print(f"[AcademIA] 📋 PLANO EXTRAÍDO E VALIDADO: {plano_final}")
            return plano_final

        except Exception as e:
            print(f"[AcademIA] ❌ Erro ao extrair plano: {e}")
            return None

    def _remover_marcador_plano(self, texto_resposta):
        """Remove a tag [PLANO: {...}] do texto, mesmo com JSON aninhado."""
        inicio_tag = texto_resposta.find("[PLANO:")
        if inicio_tag == -1:
            return texto_resposta

        inicio_json = texto_resposta.find("{", inicio_tag)
        if inicio_json == -1:
            return texto_resposta

        try:
            decoder = json.JSONDecoder()
            _plano, fim_json = decoder.raw_decode(texto_resposta, inicio_json)
            fim_colchete = texto_resposta.find("]", fim_json)
            fim_tag = fim_colchete + 1 if fim_colchete != -1 else fim_json
            return texto_resposta[:inicio_tag] + texto_resposta[fim_tag:]
        except Exception:
            return texto_resposta

    def limpar_marcador(self, texto_resposta):
        texto = re.sub(r"\[AVALIA[CÇ][AÃ]O:.*?\]", "", texto_resposta, flags=re.IGNORECASE)
        texto = self._remover_marcador_plano(texto)
        return texto.strip()