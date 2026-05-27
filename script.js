const data = {
    summary: {
        totalEmployees: 199,
        totalDepartments: 6,
        avgSalary: 72839,
        avgPerformance: 75.2,
    },
    departments: [
        { name: "Support", count: 34, salary: 80283, perf: 71.6, exp: 15.6, age: 42.4 },
        { name: "HR", count: 17, salary: 77801, perf: 78.8, exp: 18.7, age: 43.6 },
        { name: "Sales", count: 36, salary: 73139, perf: 70.7, exp: 17.8, age: 39.0 },
        { name: "Marketing", count: 36, salary: 72850, perf: 79.2, exp: 14.4, age: 49.0 },
        { name: "Engineering", count: 52, salary: 68192, perf: 75.0, exp: 16.2, age: 41.5 },
        { name: "Finance", count: 24, salary: 67667, perf: 72.9, exp: 19.5, age: 42.0 },
    ],
    insights: [
        "Best performing department: Marketing (79.2 avg performance)",
        "Highest paid department: Support ($80,283 avg salary)",
        "Salary vs Performance correlation: 0.063 (very weak)",
        "Experience vs Performance correlation: -0.040 (negligible)",
        "Average employee tenure: 6.5 years",
        "Highest avg salary by city: Denver ($77,208)",
    ],
};

function loadCards() {
    const cards = [
        { num: data.summary.totalEmployees, label: "Total Employees" },
        { num: data.summary.totalDepartments, label: "Departments" },
        { num: "$" + data.summary.avgSalary.toLocaleString(), label: "Avg Salary" },
        { num: data.summary.avgPerformance, label: "Avg Performance", suffix: "" },
    ];

    const container = document.getElementById("summary-cards");
    container.innerHTML = cards.map(c =>
        `<div class="card">
            <div class="number">${c.num}${c.suffix || ""}</div>
            <div class="label">${c.label}</div>
        </div>`
    ).join("");
}

function loadDeptTable() {
    const tbody = document.getElementById("dept-body");
    tbody.innerHTML = data.departments.map(d =>
        `<tr>
            <td><strong>${d.name}</strong></td>
            <td>${d.count}</td>
            <td>$${d.salary.toLocaleString()}</td>
            <td>${d.perf}</td>
            <td>${d.exp} yrs</td>
            <td>${d.age}</td>
        </tr>`
    ).join("");
}

function loadInsights() {
    const list = document.getElementById("insights-list");
    list.innerHTML = data.insights.map((text, i) =>
        `<li><span class="badge">${i + 1}</span> ${text}</li>`
    ).join("");
}

loadCards();
loadDeptTable();
loadInsights();
