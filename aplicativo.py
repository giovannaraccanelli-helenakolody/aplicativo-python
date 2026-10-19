```python
import string
import hashlib
import gradio as gr

# Dicionarios de conversao
ORIGINAL = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
SUBSTITUTO = (
    "plmoknijbuhvygctfxrdzeswaq"
    "PLMOKNIJBUHVYGCTFXRDZESWAQ"
    "0246813579"
)


def converter(conteudo, reverso=False):
    if not conteudo:
        return ""

    origem, destino = (
        (SUBSTITUTO, ORIGINAL) if reverso
        else (ORIGINAL, SUBSTITUTO)
    )

    tabela = str.maketrans(origem, destino)
    return conteudo.translate(tabela)


def criar_hash(conteudo):
    if not conteudo:
        return "Nenhum conteudo informado."

    resultado = hashlib.sha256(
        conteudo.encode("utf-8")
    ).hexdigest()

    return f"SHA-256:\n{resultado}"


def checar_senha(senha):
    if not senha:
        return "Informe uma senha."

    regras = [
        len(senha) >= 8,
        len(senha) >= 12,
        any(c.islower() for c in senha),
        any(c.isupper() for c in senha),
        any(c.isdigit() for c in senha),
        any(c in string.punctuation for c in senha)
    ]

    pontos = sum(regras)

    if len(senha) < 8:
        nivel = "FRACA"
    elif pontos >= 5:
        nivel = "FORTE"
    elif pontos >= 3:
        nivel = "INTERMEDIARIA"
    else:
        nivel = "FRACA"

    return (
        f"Nivel: {nivel}\n"
        f"Pontuacao: {pontos}/6\n"
        f"Tamanho: {len(senha)} caracteres"
    )


with gr.Blocks(
    theme=gr.themes.Base(
        primary_hue="green",
        neutral_hue="slate"
    ),
    title="CyberLock"
) as app:

    gr.Markdown("""
    # `> CYBERLOCK_`
    ### Terminal de ferramentas criptograficas
    """)

    with gr.Tab("Codificar"):
        entrada = gr.Textbox(
            label="Entrada",
            lines=4
        )
        saida = gr.Textbox(label="Resultado")
        gr.Button("Executar codificacao").click(
            converter, entrada, saida
        )

    with gr.Tab("Decodificar"):
        codigo = gr.Textbox(
            label="Texto codificado",
            lines=4
        )
        original = gr.Textbox(label="Texto recuperado")
        gr.Button("Reverter codigo").click(
            lambda t: converter(t, True),
            codigo,
            original
        )

    with gr.Tab("Hash"):
        conteudo = gr.Textbox(label="Texto para hash")
        resumo = gr.Textbox(label="SHA-256")
        gr.Button("Calcular").click(
            criar_hash, conteudo, resumo
        )

    with gr.Tab("Senhas"):
        credencial = gr.Textbox(
            label="Senha",
            type="password"
        )
        relatorio = gr.Textbox(label="Diagnostico")
        gr.Button("Verificar").click(
            checar_senha, credencial, relatorio
        )

    gr.Markdown("--- Sistema educacional CyberLock ---")


if __name__ == "__main__":
    app.launch()
```
