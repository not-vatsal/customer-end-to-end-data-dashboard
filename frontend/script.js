const BASE_URL = "http://127.0.0.1:8000";

async function fetchData(endpoint) {
    try {
        const res = await fetch(`${BASE_URL}${endpoint}`);
        if (!res.ok) throw new Error("API error");
        return await res.json();
    } catch (err) {
        document.getElementById("error").style.display = "block";
        throw err;
    }
}

async function loadDashboard() {
    try {
        const revenue = await fetchData("/api/revenue");
        const customers = await fetchData("/api/top-customers");
        const categories = await fetchData("/api/categories");
        const regions = await fetchData("/api/regions");

        document.getElementById("loading").style.display = "none";

        renderRevenueChart(revenue);
        renderCustomersTable(customers);
        renderCategoryChart(categories);
        renderRegionTable(regions);

    } catch (err) {
        console.error(err);
    }
}

function renderRevenueChart(data) {
    const ctx = document.getElementById("revenueChart");

    new Chart(ctx, {
        type: "line",
        data: {
            labels: data.map(d => d.order_year_month),
            datasets: [{
                label: "Revenue",
                data: data.map(d => d.total_revenue)
            }]
        }
    });
}

function renderCustomersTable(data) {
    const tbody = document.querySelector("#customersTable tbody");

    data.forEach(c => {
        const row = `
            <tr>
                <td>${c.name}</td>
                <td>${c.region}</td>
                <td>${c.total_spend}</td>
                <td>${c.churned}</td>
            </tr>
        `;
        tbody.innerHTML += row;
    });
}

function renderCategoryChart(data) {
    const ctx = document.getElementById("categoryChart");

    new Chart(ctx, {
        type: "bar",
        data: {
            labels: data.map(d => d.category),
            datasets: [{
                label: "Revenue",
                data: data.map(d => d.total_revenue)
            }]
        }
    });
}

function renderRegionTable(data) {
    const tbody = document.querySelector("#regionTable tbody");

    data.forEach(r => {
        const row = `
            <tr>
                <td>${r.region}</td>
                <td>${r.num_customers}</td>
                <td>${r.num_orders}</td>
                <td>${r.total_revenue}</td>
            </tr>
        `;
        tbody.innerHTML += row;
    });
}

loadDashboard();