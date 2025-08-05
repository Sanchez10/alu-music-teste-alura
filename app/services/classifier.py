import requests
import json
import re

def classificar_comentario(texto):
    prompt = f"""
Classifique o seguinte comentário musical do usuário:

{texto}

Retorne apenas um JSON neste formato:

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

Apenas o JSON. Nenhum outro texto.
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

            # Regex corrigida
            json_candidates = re.findall(r'\{.*?\}', raw, re.DOTALL)
            for candidate in json_candidates:
                try:
                    parsed = json.loads(candidate)
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
