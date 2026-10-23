"""
exercicios.py — Banco de exercícios do AcademIA

30 exercícios para academia + 30 para casa.
Cada exercício tem: nome, grupo muscular, séries/reps sugeridas
e link real do YouTube em português com a execução correta.

Este arquivo NÃO é enviado para a IA a cada mensagem.
O bot.py seleciona os exercícios certos e injeta apenas os
relevantes no contexto antes de chamar a API.
"""

# ─────────────────────────────────────────────────────────────
# ACADEMIA — 30 exercícios
# ─────────────────────────────────────────────────────────────
EXERCICIOS_ACADEMIA = [

    # ── PEITO ──────────────────────────────────────────────
    {
        "nome": "Supino Reto com Barra",
        "grupo": "peito",
        "series_reps": "3x10",
        "equipamento": ["barra", "banco"],
        "video": "https://www.youtube.com/watch?v=8UiTPNj66AU"
    },
    {
        "nome": "Supino Inclinado com Halteres",
        "grupo": "peito",
        "series_reps": "3x12",
        "equipamento": ["halteres", "banco inclinado"],
        "video": "https://www.youtube.com/watch?v=fG_03xSzT2s"
    },
    {
        "nome": "Crossover (polia)",
        "grupo": "peito",
        "series_reps": "3x15",
        "equipamento": ["polia"],
        "video": "https://www.youtube.com/watch?v=WbNZqYrUbJw"
    },

    # ── COSTAS ─────────────────────────────────────────────
    {
        "nome": "Puxada Frontal (pulley)",
        "grupo": "costas",
        "series_reps": "3x12",
        "equipamento": ["pulley"],
        "video": "https://www.youtube.com/watch?v=pJM_rHhluK8"
    },
    {
        "nome": "Remada Curvada com Barra",
        "grupo": "costas",
        "series_reps": "3x10",
        "equipamento": ["barra"],
        "video": "https://www.youtube.com/watch?v=TfxJMertfsw"
    },
    {
        "nome": "Remada Unilateral com Halter",
        "grupo": "costas",
        "series_reps": "3x12 cada lado",
        "equipamento": ["halter", "banco"],
        "video": "https://www.youtube.com/watch?v=SUvZiVClLKw"
    },
    {
        "nome": "Remada Baixa (cabo)",
        "grupo": "costas",
        "series_reps": "3x12",
        "equipamento": ["cabo"],
        "video": "https://www.youtube.com/watch?v=mUgFn3aMAP4"
    },

    # ── OMBROS ─────────────────────────────────────────────
    {
        "nome": "Desenvolvimento com Halteres",
        "grupo": "ombros",
        "series_reps": "3x12",
        "equipamento": ["halteres"],
        "video": "https://www.youtube.com/watch?v=Kr5_BPFRxrg"
    },
    {
        "nome": "Elevação Lateral com Halteres",
        "grupo": "ombros",
        "series_reps": "3x15",
        "equipamento": ["halteres"],
        "video": "https://www.youtube.com/watch?v=WMhXKiS3bO8"
    },
    {
        "nome": "Elevação Frontal com Halter",
        "grupo": "ombros",
        "series_reps": "3x12",
        "equipamento": ["halter"],
        "video": "https://www.youtube.com/watch?v=QDZQNTty_Wc"
    },

    # ── BÍCEPS ─────────────────────────────────────────────
    {
        "nome": "Rosca Direta com Barra",
        "grupo": "biceps",
        "series_reps": "3x12",
        "equipamento": ["barra"],
        "video": "https://www.youtube.com/watch?v=EZMYCLKuGow"
    },
    {
        "nome": "Rosca Alternada com Halteres",
        "grupo": "biceps",
        "series_reps": "3x12 cada braço",
        "equipamento": ["halteres"],
        "video": "https://www.youtube.com/watch?v=vIGvt-vgrvY"
    },
    {
        "nome": "Rosca Scott (banco scott)",
        "grupo": "biceps",
        "series_reps": "3x10",
        "equipamento": ["banco scott", "barra ou halter"],
        "video": "https://www.youtube.com/watch?v=5tsBcW_EQo8"
    },

    # ── TRÍCEPS ────────────────────────────────────────────
    {
        "nome": "Tríceps Pulley (corda)",
        "grupo": "triceps",
        "series_reps": "3x15",
        "equipamento": ["pulley", "corda"],
        "video": "https://www.youtube.com/watch?v=FM4AV2GWogo"
    },
    {
        "nome": "Tríceps Francês com Halter",
        "grupo": "triceps",
        "series_reps": "3x12",
        "equipamento": ["halter", "banco"],
        "video": "https://www.youtube.com/watch?v=HPnSFx5CIzs"
    },
    {
        "nome": "Mergulho no Banco (paralelas)",
        "grupo": "triceps",
        "series_reps": "3x12",
        "equipamento": ["paralelas ou dois bancos"],
        "video": "https://www.youtube.com/watch?v=XI-4buHz7Xo"
    },

    # ── PERNAS ─────────────────────────────────────────────
    {
        "nome": "Agachamento Livre com Barra",
        "grupo": "quadriceps/gluteos",
        "series_reps": "4x10",
        "equipamento": ["barra", "rack"],
        "video": "https://www.youtube.com/watch?v=4D-ZGYFUxyM"
    },
    {
        "nome": "Leg Press 45°",
        "grupo": "quadriceps/gluteos",
        "series_reps": "4x12",
        "equipamento": ["leg press"],
        "video": "https://www.youtube.com/watch?v=gsSNayxK3YI"
    },
    {
        "nome": "Cadeira Extensora",
        "grupo": "quadriceps",
        "series_reps": "3x15",
        "equipamento": ["cadeira extensora"],
        "video": "https://www.youtube.com/watch?v=Ufh39C5cMfU"
    },
    {
        "nome": "Mesa Flexora",
        "grupo": "posteriores de coxa",
        "series_reps": "3x15",
        "equipamento": ["mesa flexora"],
        "video": "https://www.youtube.com/watch?v=cjHkQeGe_F4"
    },
    {
        "nome": "Stiff com Barra",
        "grupo": "posteriores/gluteos",
        "series_reps": "3x12",
        "equipamento": ["barra"],
        "video": "https://www.youtube.com/watch?v=50AkPBZwACQ"
    },
    {
        "nome": "Avanço com Halteres",
        "grupo": "quadriceps/gluteos",
        "series_reps": "3x12 cada perna",
        "equipamento": ["halteres"],
        "video": "https://www.youtube.com/watch?v=2DDcRBp07uY"
    },
    {
        "nome": "Cadeira Adutora",
        "grupo": "adutores",
        "series_reps": "3x15",
        "equipamento": ["cadeira adutora"],
        "video": "https://www.youtube.com/watch?v=HPnSFx5CIzs"
    },
    {
        "nome": "Panturrilha em Pé (máquina)",
        "grupo": "panturrilha",
        "series_reps": "4x20",
        "equipamento": ["máquina de panturrilha"],
        "video": "https://www.youtube.com/watch?v=4w8gEJq8eAA"
    },

    # ── ABDÔMEN ────────────────────────────────────────────
    {
        "nome": "Abdominal na Polia Alta",
        "grupo": "abdomen",
        "series_reps": "3x15",
        "equipamento": ["polia alta", "corda"],
        "video": "https://www.youtube.com/watch?v=IZL63x3I6lg"
    },
    {
        "nome": "Prancha Abdominal",
        "grupo": "abdomen/core",
        "series_reps": "3x45 segundos",
        "equipamento": [],
        "video": "https://www.youtube.com/watch?v=TbVWMhyax2U"
    },

    # ── FULL BODY / FUNCIONAIS ─────────────────────────────
    {
        "nome": "Levantamento Terra",
        "grupo": "full body / costas / posteriores",
        "series_reps": "4x8",
        "equipamento": ["barra"],
        "video": "https://www.youtube.com/watch?v=50AkPBZwACQ"
    },
    {
        "nome": "Agachamento Sumô com Halter",
        "grupo": "adutores/gluteos",
        "series_reps": "3x12",
        "equipamento": ["halter"],
        "video": "https://www.youtube.com/watch?v=gsSNayxK3YI"
    },
    {
        "nome": "Barra Fixa (pegada pronada)",
        "grupo": "costas/biceps",
        "series_reps": "3x ao máximo",
        "equipamento": ["barra fixa"],
        "video": "https://www.youtube.com/watch?v=thg6cGXSlvY"
    },
    {
        "nome": "Hack Squat (máquina)",
        "grupo": "quadriceps",
        "series_reps": "3x12",
        "equipamento": ["hack squat"],
        "video": "https://www.youtube.com/watch?v=4w8gEJq8eAA"
    },
]


# ─────────────────────────────────────────────────────────────
# CASA — 30 exercícios
# Divididos entre: sem equipamento e com equipamento básico
# (halteres, elástico, cadeira, garrafa de água)
# ─────────────────────────────────────────────────────────────
EXERCICIOS_CASA = [

    # ── PEITO / BRAÇOS — SEM EQUIPAMENTO ──────────────────
    {
        "nome": "Flexão de Braço (padrão)",
        "grupo": "peito/triceps",
        "series_reps": "3x12",
        "equipamento": [],
        "video": "https://www.youtube.com/watch?v=TbVWMhyax2U"
    },
    {
        "nome": "Flexão de Braço Inclinada (pés na cadeira)",
        "grupo": "peito superior",
        "series_reps": "3x10",
        "equipamento": ["cadeira"],
        "video": "https://www.youtube.com/watch?v=IZL63x3I6lg"
    },
    {
        "nome": "Flexão de Braço Declinada (mãos na cadeira)",
        "grupo": "peito inferior",
        "series_reps": "3x12",
        "equipamento": ["cadeira"],
        "video": "https://www.youtube.com/watch?v=H23VZ7IZwG4"
    },
    {
        "nome": "Flexão de Braço Diamante",
        "grupo": "triceps/peito",
        "series_reps": "3x10",
        "equipamento": [],
        "video": "https://www.youtube.com/watch?v=RRi0-tvte6A"
    },
    {
        "nome": "Flexão de Braço Archer (unilateral)",
        "grupo": "peito",
        "series_reps": "3x8 cada lado",
        "equipamento": [],
        "video": "https://www.youtube.com/watch?v=9ozLIq3Nmkw"
    },

    # ── COSTAS — COM/SEM EQUIPAMENTO ──────────────────────
    {
        "nome": "Remada com Elástico",
        "grupo": "costas",
        "series_reps": "3x15",
        "equipamento": ["elástico"],
        "video": "https://www.youtube.com/watch?v=mUgFn3aMAP4"
    },
    {
        "nome": "Remada com Halter (apoio na cadeira)",
        "grupo": "costas",
        "series_reps": "3x12 cada lado",
        "equipamento": ["halter", "cadeira"],
        "video": "https://www.youtube.com/watch?v=SUvZiVClLKw"
    },
    {
        "nome": "Superman (extensão lombar no chão)",
        "grupo": "lombar/gluteos",
        "series_reps": "3x15",
        "equipamento": [],
        "video": "https://www.youtube.com/watch?v=Vk6c7CjtM14"
    },
    {
        "nome": "Barra Fixa em Casa (barra de porta)",
        "grupo": "costas/biceps",
        "series_reps": "3x ao máximo",
        "equipamento": ["barra de porta"],
        "video": "https://www.youtube.com/watch?v=thg6cGXSlvY"
    },

    # ── OMBROS ─────────────────────────────────────────────
    {
        "nome": "Desenvolvimento com Halteres (sentado)",
        "grupo": "ombros",
        "series_reps": "3x12",
        "equipamento": ["halteres"],
        "video": "https://www.youtube.com/watch?v=Kr5_BPFRxrg"
    },
    {
        "nome": "Elevação Lateral com Garrafa de Água",
        "grupo": "ombros",
        "series_reps": "3x15",
        "equipamento": ["garrafas de água (improviso)"],
        "video": "https://www.youtube.com/watch?v=WMhXKiS3bO8"
    },
    {
        "nome": "Elevação Lateral com Elástico",
        "grupo": "ombros",
        "series_reps": "3x15",
        "equipamento": ["elástico"],
        "video": "https://www.youtube.com/watch?v=QDZQNTty_Wc"
    },
    {
        "nome": "Pike Push-up (flexão em V)",
        "grupo": "ombros/triceps",
        "series_reps": "3x10",
        "equipamento": [],
        "video": "https://www.youtube.com/watch?v=NZM9dui2MZo"
    },

    # ── BÍCEPS ─────────────────────────────────────────────
    {
        "nome": "Rosca com Halter (em pé)",
        "grupo": "biceps",
        "series_reps": "3x12 cada braço",
        "equipamento": ["halteres"],
        "video": "https://www.youtube.com/watch?v=EZMYCLKuGow"
    },
    {
        "nome": "Rosca com Elástico",
        "grupo": "biceps",
        "series_reps": "3x15",
        "equipamento": ["elástico"],
        "video": "https://www.youtube.com/watch?v=vIGvt-vgrvY"
    },

    # ── TRÍCEPS ────────────────────────────────────────────
    {
        "nome": "Tríceps no Banco (mergulho)",
        "grupo": "triceps",
        "series_reps": "3x12",
        "equipamento": ["cadeira ou banco firme"],
        "video": "https://www.youtube.com/watch?v=XI-4buHz7Xo"
    },
    {
        "nome": "Tríceps Testa com Halter (deitado no chão)",
        "grupo": "triceps",
        "series_reps": "3x12",
        "equipamento": ["halteres"],
        "video": "https://www.youtube.com/watch?v=HPnSFx5CIzs"
    },

    # ── PERNAS — SEM EQUIPAMENTO ───────────────────────────
    {
        "nome": "Agachamento com Peso Corporal",
        "grupo": "quadriceps/gluteos",
        "series_reps": "4x15",
        "equipamento": [],
        "video": "https://www.youtube.com/watch?v=v_raQBqybiY"
    },
    {
        "nome": "Agachamento Sumô (peso corporal)",
        "grupo": "adutores/gluteos",
        "series_reps": "3x15",
        "equipamento": [],
        "video": "https://www.youtube.com/watch?v=cjHkQeGe_F4"
    },
    {
        "nome": "Avanço (afundo) no lugar",
        "grupo": "quadriceps/gluteos",
        "series_reps": "3x12 cada perna",
        "equipamento": [],
        "video": "https://www.youtube.com/watch?v=2DDcRBp07uY"
    },
    {
        "nome": "Agachamento Búlgaro (pé na cadeira)",
        "grupo": "quadriceps/gluteos",
        "series_reps": "3x10 cada perna",
        "equipamento": ["cadeira"],
        "video": "https://www.youtube.com/watch?v=3Y2U3Agkvbs"
    },
    {
        "nome": "Agachamento com Cadeira (para iniciantes/idosos)",
        "grupo": "quadriceps/gluteos",
        "series_reps": "3x12",
        "equipamento": ["cadeira"],
        "video": "https://www.youtube.com/watch?v=Ufh39C5cMfU"
    },
    {
        "nome": "Ponte de Glúteos (no chão)",
        "grupo": "gluteos/posteriores",
        "series_reps": "3x15",
        "equipamento": [],
        "video": "https://www.youtube.com/watch?v=GOj4TMPVuZg"
    },
    {
        "nome": "Elevação de Quadril Unilateral",
        "grupo": "gluteos",
        "series_reps": "3x12 cada lado",
        "equipamento": [],
        "video": "https://www.youtube.com/watch?v=HaaWL7Gt4Cs"
    },
    {
        "nome": "Stiff com Halteres",
        "grupo": "posteriores/gluteos",
        "series_reps": "3x12",
        "equipamento": ["halteres"],
        "video": "https://www.youtube.com/watch?v=50AkPBZwACQ"
    },
    {
        "nome": "Panturrilha em Pé (usando degrau ou chão)",
        "grupo": "panturrilha",
        "series_reps": "4x20",
        "equipamento": [],
        "video": "https://www.youtube.com/watch?v=4w8gEJq8eAA"
    },

    # ── ABDÔMEN / CORE ─────────────────────────────────────
    {
        "nome": "Prancha Frontal",
        "grupo": "core/abdomen",
        "series_reps": "3x45 segundos",
        "equipamento": [],
        "video": "https://www.youtube.com/watch?v=TbVWMhyax2U"
    },
    {
        "nome": "Abdominal Crunch (no chão)",
        "grupo": "abdomen",
        "series_reps": "3x20",
        "equipamento": [],
        "video": "https://www.youtube.com/watch?v=DKb79PvO1mY"
    },
    {
        "nome": "Abdominal Bicicleta",
        "grupo": "abdomen obliquo",
        "series_reps": "3x20",
        "equipamento": [],
        "video": "https://www.youtube.com/watch?v=p40Ky9LMgG0"
    },
    {
        "nome": "Mountain Climber",
        "grupo": "core/cardio",
        "series_reps": "3x30 segundos",
        "equipamento": [],
        "video": "https://www.youtube.com/watch?v=HaaWL7Gt4Cs"
    },
]


# ─────────────────────────────────────────────────────────────
# FUNÇÕES AUXILIARES
# Usadas pelo bot.py para filtrar os exercícios certos
# ─────────────────────────────────────────────────────────────

def get_exercicios_por_local(local: str) -> list:
    """
    Retorna a lista de exercícios conforme o local de treino.
    local: 'academia' ou 'casa'
    """
    local = local.lower().strip()
    if "academia" in local:
        return EXERCICIOS_ACADEMIA
    return EXERCICIOS_CASA


def get_exercicios_por_grupo(local: str, grupo: str) -> list:
    """
    Retorna exercícios de um grupo muscular específico para o local informado.
    Exemplo: get_exercicios_por_grupo('casa', 'peito')
    """
    todos = get_exercicios_por_local(local)
    grupo = grupo.lower().strip()
    return [e for e in todos if grupo in e["grupo"].lower()]


def formatar_exercicios_para_prompt(exercicios: list) -> str:
    """
    Formata a lista de exercícios num texto compacto para injetar no prompt.
    Exemplo de saída:
      - Agachamento Livre: 4x10 | https://youtube.com/...
    """
    linhas = []
    for e in exercicios:
        linhas.append(
            f"  - {e['nome']} ({e['grupo']}): {e['series_reps']} | Vídeo: {e['video']}"
        )
    return "\n".join(linhas)


def get_contexto_exercicios(local: str) -> str:
    """
    Retorna um bloco de texto pronto para ser injetado no prompt do bot,
    com todos os exercícios disponíveis para o local informado.
    """
    exercicios = get_exercicios_por_local(local)
    texto = f"EXERCÍCIOS DISPONÍVEIS PARA {local.upper()} (use SOMENTE estes ao montar o treino):\n"
    texto += formatar_exercicios_para_prompt(exercicios)
    return texto