PRODUCTS = {
    'vaso-aurora': {'id': 'vaso-aurora', 'name': 'Vaso Aurora', 'price': 18900, 'art': 'image-ceramic'},
    'luminaria-lua': {'id': 'luminaria-lua', 'name': 'Luminária Lua', 'price': 34900, 'art': 'image-lamp'},
    'tigela-terra': {'id': 'tigela-terra', 'name': 'Tigela Terra', 'price': 12900, 'art': 'image-bowl'},
    'manta-brisa': {'id': 'manta-brisa', 'name': 'Manta Brisa', 'price': 25900, 'art': 'image-throw'},
}


def format_brl(centavos: int) -> str:
    valor = f'{centavos / 100:,.2f}'
    return 'R$ ' + valor.replace(',', 'X').replace('.', ',').replace('X', '.')
