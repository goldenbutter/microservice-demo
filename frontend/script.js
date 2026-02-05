// Backend API base URL
//const API_URL = "http://127.0.0.1:8000";
//const API_URL = "http://backend:8000";

// use localhost for development, and backend for Docker
//const API_URL = "http://localhost:8000";

// use microservice.local for production deployment with minikube / ingress
//const API_URL = "http://microservice.local"
const API_URL = "/api";

// Fetch and display all items
async function loadItems() {
    const response = await fetch(`${API_URL}/items`);
    const items = await response.json();

    const container = document.getElementById("items-container");
    container.innerHTML = ""; // Clear previous items

    items.forEach(item => {
        const div = document.createElement("div");
        div.classList.add("item-box");
        div.innerHTML = `
            <strong>ID:</strong> ${item.id}<br>
            <strong>Name:</strong> ${item.name}<br>
            <strong>Description:</strong> ${item.description}
        `;
        container.appendChild(div);
    });
}

// Create a new item
async function createItem() {
    const name = document.getElementById("name").value;
    const description = document.getElementById("description").value;

    if (!name || !description) {
        alert("Please fill both name and description.");
        return;
    }

    await fetch(`${API_URL}/items`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ name, description })
    });

    // Reload the updated item list
    loadItems();

    // Clear inputs
    document.getElementById("name").value = "";
    document.getElementById("description").value = "";
}

// Load items on page start
window.onload = loadItems;