import pandas as pd

def convert_value_ida(valor):
    """
    Converte valores corrompidos ou longos em floats legíveis no formato xx.xxx (ex: 8747783687943263 -> 87.478).
    """
    try:
        if pd.isna(valor):
            return None

        valor_str = str(valor).strip()

        # Remove tudo que não for dígito
        numeros_apenas = ''.join(filter(str.isdigit, valor_str))

        # Se for um número absurdamente grande (como 16 dígitos), assume que são casas extras
        if len(numeros_apenas) > 5:
            # Mantém só os 5 primeiros dígitos e insere ponto antes dos 3 últimos
            significativos = numeros_apenas[:5]
            valor_formatado = f"{significativos[:-3]}.{significativos[-3:]}"
            return float(valor_formatado)

        # Se estiver num tamanho normal (ex: 87478), converte direto
        return float(numeros_apenas[:-3] + "." + numeros_apenas[-3:]) if len(numeros_apenas) >= 4 else float(numeros_apenas)

    except Exception as e:
        return None