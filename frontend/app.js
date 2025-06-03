/*
Skrypt front-end (JavaScript)
------------------------------
Zarządza interakcją użytkownika z aplikacją FastAPI:
- logowanie/wylogowywanie
- import i eksport danych
- generowanie wykresów PNG i interaktywnych (Chart.js)
- raporty i korelacje
*/

// 🔹 Globalny token JWT
let token = "";

// 🔹 Po załadowaniu strony:
document.addEventListener("DOMContentLoaded", async () => {
    // Pobranie tokena JWT i użytkownika z localStorage
    token = localStorage.getItem("token");
    const user = localStorage.getItem("user");

    // Jeśli brak tokena — przekierowanie na stronę logowania
    if (!token) {
        window.location.href = "/login";
    } else {
        // Wyświetlamy nazwę użytkownika w panelu
        const userNameEl = document.getElementById("user-name");
        if (userNameEl) {
            userNameEl.textContent = user || "użytkowniku";
        }
    }

    // Automatyczne wyświetlenie wykresu PNG po starcie
    updatePNG();

    // Automatyczne załadowanie regionów i narysowanie wykresu
    const defaultCollection = document.getElementById("collection-chart").value;
    await loadRegions(defaultCollection);
    document.getElementById("region-chart").selectedIndex = 0;
    drawChart();
});

// 🔹 Wylogowanie
function logout() {
    localStorage.removeItem("token");
    localStorage.removeItem("user");
    window.location.href = "/login";
}

// 🔹 Import danych (wysyłka pliku)
async function importData() {
    const collection = document.getElementById("collection-import").value;
    const format = document.getElementById("import-format").value;
    const fileInput = document.getElementById("file-input");

    if (fileInput.files.length === 0) {
        alert("Wybierz plik do importu.");
        return;
    }

    const file = fileInput.files[0];
    const formData = new FormData();
    formData.append("file", file);

    try {
        const response = await fetch(`/import/${collection}?format=${format}`, {
            method: "POST",
            body: formData
        });

        if (response.ok) {
            const result = await response.json();
            alert(result.message);
        } else {
            const error = await response.json();
            alert(`Błąd importu: ${error.detail}`);
        }
    } catch (error) {
        console.error("Błąd importu:", error);
        alert("Błąd importu.");
    }
}

// 🔹 Przełączanie trybu jasnego/ciemnego
function toggleDarkMode() {
    document.body.classList.toggle("light-mode");
}

// 🔹 Eksport danych
async function exportData() {
    const collection = document.getElementById("collection-export").value;
    const format = document.getElementById("export-format").value;

    try {
        const response = await fetch(`/export/${collection}?format=${format}`);
        if (!response.ok) {
            const error = await response.json();
            alert(`Błąd eksportu: ${error.detail}`);
            return;
        }

        let blob;
        let filename;
        if (format === "json") {
            const data = await response.json();
            blob = new Blob([JSON.stringify(data, null, 2)], { type: "application/json" });
            filename = `${collection}.json`;
        } else {
            const data = await response.text();
            let mimeType = "text/plain";
            if (format === "yaml") mimeType = "application/x-yaml";
            if (format === "xml") mimeType = "application/xml";
            blob = new Blob([data], { type: mimeType });
            filename = `${collection}.${format}`;
        }

        // Pobieranie pliku eksportu
        const url = URL.createObjectURL(blob);
        const a = document.createElement("a");
        a.href = url;
        a.download = filename;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
    } catch (error) {
        console.error("Błąd eksportu:", error);
        alert("Błąd eksportu.");
    }
}

// 🔹 Pobieranie danych przez REST API
async function fetchDataFromMongo() {
    const collection = document.getElementById("collection-rest").value;
    const year = document.getElementById("filter-year").value;
    const region = document.getElementById("filter-region").value;
    const sort = document.getElementById("sort-order").value;
    const limit = document.getElementById("limit").value;
    const page = document.getElementById("page").value;

    let url = `/external/fetch?collection=${collection}&sort=${sort}&limit=${limit}&page=${page}`;
    if (year) url += `&year=${year}`;
    if (region) url += `&region=${region}`;

    try {
        const response = await fetch(url);
        const data = await response.json();

        if (!data.sample || data.sample.length === 0) {
            document.getElementById("rest-output").textContent = "Brak danych.";
            return;
        }

        document.getElementById("rest-output").textContent = JSON.stringify(data, null, 2);
    } catch (error) {
        console.error("Błąd pobierania danych:", error);
        document.getElementById("rest-output").textContent = "Błąd pobierania danych.";
    }
}

// 🔹 Generowanie raportu
async function generateReport() {
    const collection = document.getElementById("collection-report").value;
    const year = document.getElementById("report-year").value;
    try {
        const response = await fetch(`/report/${collection}?year=${year}`);
        const data = await response.json();
        if (data.regions.length === 0) {
            document.getElementById("report-output").textContent = "Brak danych.";
            return;
        }
        const output = data.regions
            .map(r => `${r.region}: ${r.total.toFixed(2)}`)
            .join("\n");
        document.getElementById("report-output").textContent = output;
    } catch (error) {
        console.error("Błąd pobierania raportu:", error);
        document.getElementById("report-output").textContent = "Błąd pobierania raportu.";
    }
}

// 🔹 Sprawdzanie korelacji między dwiema kolekcjami
async function checkCorrelation() {
    const col1 = document.getElementById("collection1-corr").value;
    const col2 = document.getElementById("collection2-corr").value;
    try {
        const response = await fetch(`/correlation/${col1}/${col2}`);
        const data = await response.json();
        if (!data.results || data.results.length === 0) {
            document.getElementById("correlation-output").textContent = "Brak wspólnych danych.";
            return;
        }
        const output = data.results
            .map(r => `${r.region}: korelacja = ${r.correlation}`)
            .join("\n");
        document.getElementById("correlation-output").textContent = output;
    } catch (error) {
        console.error("Błąd pobierania korelacji:", error);
        document.getElementById("correlation-output").textContent = "Błąd pobierania korelacji.";
    }
}

// 🔹 Wyświetlanie wykresu PNG
function updatePNG() {
    const collection = document.getElementById("collection-png").value;
    document.getElementById("chart-png").src = `/charts/${collection}.png`;
}

// 🔹 Ładowanie regionów do selecta
async function loadRegions(collection) {
    try {
        const response = await fetch(`/charts/${collection}`);
        const data = await response.json();
        const regionSelect = document.getElementById("region-chart");
        regionSelect.innerHTML = "";
        const regions = data.map(item => item.region);
        regions.forEach(region => {
            const option = document.createElement("option");
            option.value = region;
            option.textContent = region;
            regionSelect.appendChild(option);
        });
    } catch (error) {
        console.error("Błąd ładowania regionów:", error);
    }
}

// 🔹 Rysowanie wykresu (Chart.js)
async function drawChart() {
    const collection = document.getElementById("collection-chart").value;
    const region = document.getElementById("region-chart").value;

    try {
        const response = await fetch(`/charts/${collection}`);
        const data = await response.json();

        if (!Array.isArray(data) || data.length === 0) {
            alert("Brak danych do wykresu.");
            return;
        }

        const selectedRegion = data.find(item => item.region === region);
        if (!selectedRegion) {
            alert(`Brak danych dla regionu: ${region}`);
            return;
        }

        const years = selectedRegion.data.map(item => item.year);
        const values = selectedRegion.data.map(item => parseFloat(item.amount) || 0);

        const ctx = document.getElementById("myChart").getContext("2d");

        if (window.myChart && typeof window.myChart.destroy === "function") {
            window.myChart.destroy();
        }

        window.myChart = new Chart(ctx, {
            type: "bar",  // 🔥 Zmieniono wykres na słupkowy (dla lepszej czytelności)
            data: {
                labels: years,
                datasets: [{
                    label: `${region}`,
                    data: values,
                    backgroundColor: "rgba(75, 192, 192, 0.6)"
                }]
            },
            options: {
                responsive: true,
                scales: {
                    y: { beginAtZero: true }
                }
            }
        });
    } catch (error) {
        console.error("Błąd podczas generowania wykresu:", error);
        alert("Błąd podczas generowania wykresu.");
    }
}

// 🔹 Obsługa zmiany kolekcji — automatyczne przeładowanie regionów i wykresu
document.getElementById("collection-chart").addEventListener("change", async () => {
    const collection = document.getElementById("collection-chart").value;
    await loadRegions(collection);
    document.getElementById("region-chart").selectedIndex = 0;
    drawChart();
});
