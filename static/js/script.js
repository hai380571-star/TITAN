let cart = [];
document.getElementById('billDate').innerText = new Date().toLocaleDateString();

// Section Switching Logic
function showSection(id) {
    document.querySelectorAll('section').forEach(s => s.classList.add('d-none'));
    document.getElementById('sec-' + id).classList.remove('d-none');
    // Sidebar close karo (mobile ke liye)
    let sidebar = bootstrap.Offcanvas.getInstance(document.getElementById('menuSidebar'));
    if(sidebar) sidebar.hide();
}

function addToCart(name, price, cost) {
    let item = cart.find(i => i.name === name);
    if(item) { item.qty++; } 
    else { cart.push({name, price, cost, qty: 1}); }
    renderBill();
}

function renderBill() {
    let tbody = document.querySelector("#billTable tbody");
    tbody.innerHTML = "";
    let total = 0;
    cart.forEach(i => {
        total += i.price * i.qty;
        tbody.innerHTML += `<tr><td>${i.name}</td><td>${i.qty}</td><td>${i.price * i.qty}</td></tr>`;
    });
    document.getElementById('netTotal').innerText = total;
}

function finalSubmit() {
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

function saveNewItem() {
    let data = {
        name: document.getElementById('newItemName').value,
        price: document.getElementById('newItemPrice').value,
        cost: document.getElementById('newItemCost').value,
        co_id: document.getElementById('coId').value
    };
    fetch('/add-item', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(data)
    }).then(() => {
        alert("Item Saved!");
        location.reload();
    });
}
        type: document.getElementById('billType').value,
        ref_no: document.getElementById('refInput').value,
        total: net,
        profit: net - totalCost,
        payment: document.getElementById('payMode').value
    };

    fetch('/save-bill', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(billData)
    }).then(() => {
        window.print();
        location.reload();
    });
}
