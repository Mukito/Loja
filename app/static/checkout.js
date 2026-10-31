(() => {
    const KEY = 'casaNativaCart';
    const products = window.CASA_PRODUCTS || {};
    const money = cents => new Intl.NumberFormat('pt-BR', { style: 'currency', currency: 'BRL' }).format(cents / 100);
    let cart = [];
    try { cart = JSON.parse(localStorage.getItem(KEY) || '[]'); } catch (_) { cart = []; }
    if (!Array.isArray(cart)) cart = [];

    const summary = document.getElementById('checkout-summary');
    const form = document.getElementById('checkout-form');
    const validItems = cart.filter(item => products[item.id] && Number.isInteger(item.quantidade) && item.quantidade > 0 && item.quantidade <= 20);
    let subtotal = 0;
    validItems.forEach(item => {
        const product = products[item.id];
        subtotal += product.price * item.quantidade;
        const row = document.createElement('div'); row.className = 'checkout-item';
        const name = document.createElement('span'); name.textContent = `${item.quantidade}× ${product.name}`;
        const price = document.createElement('strong'); price.textContent = money(product.price * item.quantidade);
        row.append(name, price); summary.append(row);
    });

    const shipping = subtotal === 0 || subtotal >= window.CASA_FREE_SHIPPING_FROM ? 0 : window.CASA_SHIPPING_FEE;
    document.getElementById('checkout-subtotal').textContent = money(subtotal);
    document.getElementById('checkout-shipping').textContent = shipping ? money(shipping) : 'Grátis';
    document.getElementById('checkout-total').textContent = money(subtotal + shipping);
    if (!validItems.length) {
        const empty = document.createElement('p'); empty.className = 'checkout-empty'; empty.textContent = 'Sua sacola está vazia. Volte à loja e escolha uma peça.'; summary.append(empty);
        form.querySelector('.checkout-submit').disabled = true;
    }
    form.addEventListener('submit', event => {
        if (!validItems.length) { event.preventDefault(); return; }
        document.getElementById('checkout-items').value = JSON.stringify(validItems);
        const submit = form.querySelector('.checkout-submit');
        submit.disabled = true;
        submit.textContent = 'Gerando pedido…';
    });
})();
