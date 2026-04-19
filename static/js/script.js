let cart = [];
document.getElementById('displayDate').innerText = "Date: " + new Date().toLocaleDateString();

// Fast Click Items (Example items)
function fastAdd(name, price, cost) {
    let item = cart.find(i => i.name === name);
    if(item) { item.qty++; } 
    else { cart.push({name, price, cost, qty: 1}); }
    updateTable();
}

function updateTable() {
    let tbody = document.querySelector("#billTable tbody");
    tbody.innerHTML = "";
    let sub = 0;
    cart.forEach(i => {
        let t = i.price * i.qty;
        sub += t;
        tbody.innerHTML += `<tr><td>${i.name}</td><td>${i.price}</td><td>${i.qty}</td><td>${t}</td></tr>`;
    });
    document.getElementById('subTotal').innerText = sub;
    calculateNet();
}

function calculateNet() {
    let sub = parseFloat(document.getElementById('subTotal').innerText);
    let disc = parseFloat(document.getElementById('discountInput').value) || 0;
    document.getElementById('netTotal').innerText = sub - disc;
}

function saveBill() {
    let net = parseFloat(document.getElementById('netTotal').innerText);
    let totalCost = cart.reduce((a, b) => a + (b.cost * b.qty), 0);
    
    let billData = {
        company_id: document.getElementById('coId').value,
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
