(() => {
    const CART_KEY = 'casaNativaCart';
    const products = window.CASA_PRODUCTS || {};
    let cart;
    try { cart = JSON.parse(localStorage.getItem(CART_KEY) || '[]'); }
    catch (_) { cart = []; }
    if (!Array.isArray(cart)) cart = [];
    cart = cart.filter(item => item && products[item.id] && Number.isInteger(item.quantidade) && item.quantidade > 0 && item.quantidade <= 20);

    const money = cents => new Intl.NumberFormat('pt-BR', { style: 'currency', currency: 'BRL' }).format(cents / 100);
    const save = () => localStorage.setItem(CART_KEY, JSON.stringify(cart));
    const layer = document.getElementById('cart-layer');
    const list = document.getElementById('cart-items');

    function openCart() { layer.hidden = false; document.body.classList.add('cart-open'); render(); }
    function closeCart() { layer.hidden = true; document.body.classList.remove('cart-open'); }
    function render() {
        const count = cart.reduce((sum, item) => sum + item.quantidade, 0);
        document.getElementById('cart-count').textContent = count;
        document.getElementById('cart-empty').hidden = cart.length > 0;
        document.getElementById('cart-checkout').hidden = cart.length === 0;
        list.replaceChildren();
        let subtotal = 0;
        cart.forEach(item => {
            const product = products[item.id];
            if (!product) return;
            subtotal += product.price * item.quantidade;
            const row = document.createElement('article');
            row.className = 'cart-item';
            const art = document.createElement('div'); art.className = `cart-thumb ${product.art}`;
            const details = document.createElement('div'); details.className = 'cart-item-details';
            const name = document.createElement('strong'); name.textContent = product.name;
            const price = document.createElement('span'); price.textContent = money(product.price);
            const controls = document.createElement('div'); controls.className = 'quantity-controls';
            const minus = document.createElement('button'); minus.type = 'button'; minus.dataset.cartAction = 'minus'; minus.dataset.id = item.id; minus.textContent = '−'; minus.setAttribute('aria-label', `Diminuir ${product.name}`);
            const qty = document.createElement('span'); qty.textContent = item.quantidade;
            const plus = document.createElement('button'); plus.type = 'button'; plus.dataset.cartAction = 'plus'; plus.dataset.id = item.id; plus.textContent = '+'; plus.setAttribute('aria-label', `Aumentar ${product.name}`);
            const remove = document.createElement('button'); remove.type = 'button'; remove.dataset.cartAction = 'remove'; remove.dataset.id = item.id; remove.className = 'remove-item'; remove.textContent = 'Remover';
            controls.append(minus, qty, plus, remove); details.append(name, price, controls); row.append(art, details); list.append(row);
        });
        document.getElementById('cart-subtotal').textContent = money(subtotal);
    }

    document.querySelectorAll('.add-to-cart').forEach(button => button.addEventListener('click', () => {
        const id = button.dataset.productId;
        const found = cart.find(item => item.id === id);
        if (found) found.quantidade = Math.min(found.quantidade + 1, 20);
        else if (products[id]) cart.push({ id, quantidade: 1 });
        save(); render(); openCart();
    }));
    document.getElementById('cart-toggle').addEventListener('click', openCart);
    layer.addEventListener('click', event => {
        const close = event.target.closest('[data-close-cart]');
        if (close) closeCart();
        const action = event.target.closest('[data-cart-action]');
        if (!action) return;
        const item = cart.find(entry => entry.id === action.dataset.id);
        if (!item) return;
        if (action.dataset.cartAction === 'plus') item.quantidade = Math.min(item.quantidade + 1, 20);
        if (action.dataset.cartAction === 'minus') item.quantidade -= 1;
        if (action.dataset.cartAction === 'remove' || item.quantidade <= 0) cart = cart.filter(entry => entry.id !== item.id);
        save(); render();
    });
    document.addEventListener('keydown', event => { if (event.key === 'Escape' && !layer.hidden) closeCart(); });
    window.addEventListener('storage', event => {
        if (event.key !== CART_KEY) return;
        try { cart = JSON.parse(event.newValue || '[]') || []; } catch (_) { cart = []; }
        if (!Array.isArray(cart)) cart = [];
        cart = cart.filter(item => item && products[item.id] && Number.isInteger(item.quantidade) && item.quantidade > 0 && item.quantidade <= 20);
        render();
    });
    render();
})();
