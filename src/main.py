import os
import pandas as pd
import requests
from dotenv import load_dotenv

# Carregar variáveis do .env
load_dotenv()

URL = "https://sgt.cnmp.mp.br/consulta_publica_classes.php"
HEADERS = {"User-Agent": os.getenv("USER_AGENT")}
OUTPUT_DIR = os.getenv("OUTPUT_DIR", "data")

def fetch_tpu():
    response = requests.get(URL, headers=HEADERS)
    response.raise_for_status()
    tables = pd.read_html(response.content, encoding="utf-8")

    if not tables:
        raise ValueError("Nenhuma tabela encontrada.")

    df = tables[0]
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    output_file = os.path.join(OUTPUT_DIR, "tabela_TPU.json")
    df.to_json(output_file, orient="records", force_ascii=False, indent=2)
    print(f"Tabela TPU salva em {output_file}")

if __name__ == "__main__":
    fetch_tpu()
