import re
import unicodedata


def _ascii_text(value: str, limit: int) -> str:
    value = unicodedata.normalize('NFKD', value or '').encode('ascii', 'ignore').decode('ascii')
    value = re.sub(r'[^A-Za-z0-9 ]', '', value).upper().strip()
    value = re.sub(r'\s+', ' ', value)
    return value[:limit]


def _tlv(tag: str, value: str) -> str:
    length = len(value.encode('utf-8'))
    if length > 99:
        raise ValueError(f'Campo Pix maior que o permitido: {tag}')
    return f'{tag}{length:02d}{value}'


def _crc16_ccitt(text: str) -> str:
    crc = 0xFFFF
    for byte in text.encode('utf-8'):
        crc ^= byte << 8
        for _ in range(8):
            crc = ((crc << 1) ^ 0x1021) & 0xFFFF if crc & 0x8000 else (crc << 1) & 0xFFFF
    return f'{crc:04X}'


def build_pix_payload(chave: str, nome: str, cidade: str, valor_centavos: int, txid: str) -> str:
    """Monta o BR Code Pix estático para uma cobrança com valor e identificador."""
    chave = (chave or '').strip()
    nome = _ascii_text(nome, 25)
    cidade = _ascii_text(cidade, 15)
    txid = re.sub(r'[^A-Za-z0-9]', '', txid or '').upper()[:25] or '***'
    if not chave or not nome or not cidade or valor_centavos <= 0:
        raise ValueError('Configure a chave Pix, o nome, a cidade e um valor positivo.')

    merchant = _tlv('00', 'br.gov.bcb.pix') + _tlv('01', chave)
    additional_data = _tlv('05', txid)
    amount = f'{valor_centavos / 100:.2f}'
    payload = (
        _tlv('00', '01')
        + _tlv('26', merchant)
        + _tlv('52', '0000')
        + _tlv('53', '986')
        + _tlv('54', amount)
        + _tlv('58', 'BR')
        + _tlv('59', nome)
        + _tlv('60', cidade)
        + _tlv('62', additional_data)
        + '6304'
    )
    return payload + _crc16_ccitt(payload)
