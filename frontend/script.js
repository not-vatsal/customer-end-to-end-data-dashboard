const BASE_URL = "http://127.0.0.1:8000";

// ✅ GLOBAL STATE
let revenueData = [];
let customersData = [];
let revenueChart = null;

// =========================
// 🔹 FETCH FUNCTION
// =========================
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

// =========================
// 🔹 LOAD DASHBOARD
// =========================
async function loadDashboard() {
    try {
        revenueData = await fetchData("/api/revenue");
        customersData = await fetchData("/api/top-customers");
        const categories = await fetchData("/api/categories");
        const regions = await fetchData("/api/regions");

        document.getElementById("loading").style.display = "none";

        renderRevenueChart(revenueData);
        renderCustomersTable(customersData);
        renderCategoryChart(categories);
        renderRegionTable(regions);

    } catch (err) {
        console.error(err);
    }
}

// =========================
// 🔹 REVENUE CHART
// =========================
function renderRevenueChart(data) {
    const ctx = document.getElementById("revenueChart");

    // 🔥 destroy old chart before creating new
    if (revenueChart) {
        revenueChart.destroy();
    }

    revenueChart = new Chart(ctx, {
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

// =========================
// 🔹 CUSTOMERS TABLE
// =========================
function renderCustomersTable(data) {
    const tbody = document.querySelector("#customersTable tbody");

    // 🔥 clear table before re-render
    tbody.innerHTML = "";

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

// =========================
// 🔹 CATEGORY CHART
// =========================
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

// =========================
// 🔹 REGION TABLE
// =========================
function renderRegionTable(data) {
    const tbody = document.querySelector("#regionTable tbody");

    tbody.innerHTML = "";

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

// =========================
// 🔹 DATE FILTER (BONUS 1)
// =========================
function filterRevenue() {
    const start = document.getElementById("startDate").value;
    const end = document.getElementById("endDate").value;

    // If empty → reset
    if (!start || !end) {
        renderRevenueChart(revenueData);
        return;
    }

    const filtered = revenueData.filter(d =>
        d.order_year_month >= start &&
        d.order_year_month <= end
    );

    renderRevenueChart(filtered);
}

// =========================
// 🔹 SEARCH BOX (BONUS 2)
// =========================
window.onload = function () {
    document.getElementById("searchBox").addEventListener("input", function () {
        const value = this.value.toLowerCase();

        const filtered = customersData.filter(c =>
            c.name.toLowerCase().includes(value)
        );

        renderCustomersTable(filtered);
    });
};

// =========================
// 🔹 INIT
// =========================
loadDashboard();