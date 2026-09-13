const tg = window.Telegram.WebApp;
tg.expand();
tg.ready();

// ЗАМЕНИ ЭТОТ URL ПОСЛЕ ДЕПЛОЯ НА RENDER
const API_URL = "https://westy-toon.onrender.com";

let contacts = [];

async function loadContacts() {
    try {
        const res = await fetch(`${API_URL}/api/contacts`);
        contacts = await res.json();
        renderContacts();
    } catch (e) {
        alert("Ошибка загрузки: " + e.message);
    }
}

function renderContacts(filter = "") {
    const div = document.getElementById("contacts");
    const filtered = contacts.filter(c =>
        c.name.toLowerCase().includes(filter.toLowerCase()) ||
        c.phone.includes(filter) ||
        (c.email && c.email.toLowerCase().includes(filter.toLowerCase()))
    );

    div.innerHTML = filtered.map(c => `
        <div class="contact">
            <h3>${c.name}</h3>
            <p>📞 ${c.phone}</p>
            ${c.email ? `<p>✉️ ${c.email}</p>` : ""}
            ${c.note ? `<p>📝 ${c.note}</p>` : ""}
            <button class="delete-btn" onclick="deleteContact(${c.id})">Удалить</button>
        </div>
    `).join("");

    document.getElementById("counter").textContent = `Всего контактов: ${contacts.length}`;
}

async function addContact() {
    const name = document.getElementById("name").value.trim();
    const phone = document.getElementById("phone").value.trim();
    const email = document.getElementById("email").value.trim();
    const note = document.getElementById("note").value.trim();

    if (!name || !phone) {
        alert("Имя и телефон обязательны");
        return;
    }

    await fetch(`${API_URL}/api/contacts`, {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({name, phone, email, note})
    });

    ["name", "phone", "email", "note"].forEach(id => document.getElementById(id).value = "");
    loadContacts();
}

async function deleteContact(id) {
    if (!confirm("Удалить контакт?")) return;
    await fetch(`${API_URL}/api/contacts/${id}`, {method: "DELETE"});
    loadContacts();
}

function searchContacts() {
    const query = document.getElementById("search").value;
    renderContacts(query);
}

document.getElementById("addBtn").onclick = addContact;
loadContacts();