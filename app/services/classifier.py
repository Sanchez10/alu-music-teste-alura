import requests
import json
import re

from concurrent.futures import ThreadPoolExecutor, as_completed

def classificar_comentario(texto):
    prompt = f"""
Você é um classificador de comentários musicais.

Classifique o comentário a seguir:

\"\"\"{texto}\"\"\"

Responda com **apenas** um JSON. Nenhum outro texto. Nenhum markdown. Nenhum comentário.

Formato obrigatório:
{{
  "categoria": "<ELOGIO|CRÍTICA|SUGESTÃO|DÚVIDA|SPAM>",
  "tags_funcionalidades": [
    {{
      "codigo": "nome_tecnico",
      "explicacao": "descrição curta da funcionalidade"
    }}
  ],
  "confianca": 0.85
}}

Exemplo válido:
{{
  "categoria": "CRÍTICA",
  "tags_funcionalidades": [
    {{
      "codigo": "clip_narrativa",
      "explicacao": "Clipe com narrativa mal estruturada"
    }}
  ],
  "confianca": 0.72
}}
"""

    try:
        print("[LLM DEBUG] Enviando prompt para o LLM...")
        response = requests.post(
            "http://172.22.64.1:11434/api/generate",
            json={"model": "tinyllama", "prompt": prompt, "stream": False},
            timeout=15
        )

        if response.status_code == 200:
            raw = response.json().get("response", "")
            print("[LLM DEBUG] Raw content in 'response':", raw)

            match = re.search(r'\{[\s\S]*\}', raw)
            if match:
                try:
                    parsed = json.loads(match.group(0))
                    if (
                        isinstance(parsed, dict)
                        and parsed.get("categoria") in ["ELOGIO", "CRÍTICA", "SUGESTÃO", "DÚVIDA", "SPAM"]
                        and isinstance(parsed.get("tags_funcionalidades"), list)
                        and isinstance(parsed.get("confianca"), float)
                    ):
                        print("[LLM DEBUG] JSON válido encontrado.")
                        return parsed
                except Exception as e:
                    print(f"[LLM ERROR] Falha ao decodificar JSON extraído: {e}")
            else:
                print("[LLM ERROR] Nenhum JSON encontrado na resposta.")
        else:
            print(f"[LLM ERROR] Status code: {response.status_code}")

    except Exception as e:
        print(f"[LLM EXCEPTION] Erro ao processar resposta: {e}")

    print("[LLM FALLBACK] Usando classificação simulada.")
    return {
        "categoria": "ELOGIO",
        "tags_funcionalidades": [
            {"codigo": "feat_autotune", "explicacao": "Uso de autotune perceptível"}
        ],
        "confianca": 0.80
    }

def classificar_comentarios_em_lote(lista_textos):
    resultados = []
    max_threads = min(10, len(lista_textos))

    with ThreadPoolExecutor(max_workers=max_threads) as executor:
        futuros = {executor.submit(classificar_comentario, texto): texto for texto in lista_textos}
        
        for futuro in as_completed(futuros):
            try:
                resultado = futuro.result()
                resultados.append(resultado)
            except Exception as e:
                print(f"[LLM ERROR] Erro ao processar comentário em lote: {e}")
                resultados.append({
                    "categoria": "ERRO",
                    "tags_funcionalidades": [],
                    "confianca": 0.0
                })

    return resultados
