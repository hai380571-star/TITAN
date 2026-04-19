// Setup Company Function
function setupCompany() {
    let data = {
        name: document.getElementById('setupName').value,
        addr: document.getElementById('setupAddr').value,
        prefix: document.getElementById('setupPrefix').value,
        start: document.getElementById('setupStart').value || 100
    };

    if(!data.name || !data.addr || !data.prefix) return alert("Pehle saari details bharo bhai!");

    fetch('/create-company', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(data)
    }).then(() => {
        location.reload(); // Refresh hote hi ab Dashboard dikhega
    });
}

// Baki logic (Cart, Save Bill, Page Switch) same rahega...
let cart = [];
if(document.getElementById('dateLine')) {
    document.getElementById('dateLine').innerText = new Date().toLocaleDateString();
}

function showPage(pageId) {
    document.querySelectorAll('.page-content').forEach(p => p.classList.add('d-none'));
    document.getElementById('page-' + pageId).classList.remove('d-none');
    let offcanvas = bootstrap.Offcanvas.getInstance(document.getElementById('sidebar'));
    if(offcanvas) offcanvas.hide();
}

function addToCart(name, price, cost) {
    let item = cart.find(i => i.name === name);
    if(item) { item.qty++; } else { cart.push({name, price, cost, qty: 1}); }
    renderTable();
}

function renderTable() {
    let tbody = document.querySelector("#billTable tbody");
    if(!tbody) return;
    tbody.innerHTML = "";
    let sub = 0;
    cart.forEach(i => {
        sub += i.price * i.qty;
        tbody.innerHTML += `<tr><td>${i.name}</td><td>${i.qty}</td><td>${i.price * i.qty}</td></tr>`;
    });
    document.getElementById('netTotal').innerText = sub;
}

function saveItem() {
    let data = {
        name: document.getElementById('newIName').value,
        price: document.getElementById('newIPrice').value,
        cost: document.getElementById('newICost').value,
        co_id: document.getElementById('coId').value
    };
    fetch('/add-item', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(data)
    }).then(() => location.reload());
}

function saveAndPrint() {
    let grand = parseFloat(document.getElementById('netTotal').innerText);
    let totalCost = cart.reduce((a, b) => a + (b.cost * b.qty), 0);
    let data = {
        company_id: document.getElementById('coId').value,
        total: grand,
        profit: grand - totalCost
    };
    fetch('/save-bill', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(data)
    }).then(() => {
        window.print();
        location.reload();
    });
}
