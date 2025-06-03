/*
Plik login.js
--------------
Obsługuje:
✅ logowanie użytkownika (wysyłka danych do FastAPI i odbiór tokena JWT)
✅ zapisywanie tokena i nazwy użytkownika w localStorage
✅ przekierowanie do panelu głównego po zalogowaniu
✅ przełączanie trybu ciemny/jasny
*/

// 🔹 Funkcja obsługująca logowanie użytkownika
async function login(event) {
  event.preventDefault(); // 🔸 zatrzymanie domyślnego działania formularza

  // 🔸 Pobranie loginu i hasła z inputów
  const username = document.getElementById("username").value;
  const password = document.getElementById("password").value;

  // 🔸 Wywołanie endpointu /token (FastAPI) metodą POST
  const response = await fetch("/token", {
    method: "POST",
    headers: { "Content-Type": "application/x-www-form-urlencoded" }, // standard dla OAuth2
    body: `username=${encodeURIComponent(username)}&password=${encodeURIComponent(password)}`
  });

  // 🔸 Odczytanie odpowiedzi JSON
  const data = await response.json();

  if (response.ok) {
    // 🔹 Jeśli logowanie poprawne:
    localStorage.setItem("token", data.access_token); // zapis tokena JWT w localStorage
    localStorage.setItem("user", username); // zapis nazwy użytkownika
    window.location.href = "/"; // przekierowanie do panelu głównego
  } else {
    // 🔹 Jeśli błąd logowania:
    document.getElementById("error").textContent = "❌ Błędna nazwa użytkownika lub hasło.";
  }
}

// 🔹 Funkcja przełączająca tryb jasny/ciemny
function toggleDarkMode() {
  document.body.classList.toggle("light-mode"); // przełącz klasę body
  const icon = document.querySelector(".dark-mode-toggle i"); // wybór ikony księżyca/słońca

  if (document.body.classList.contains("light-mode")) {
    // 🔸 Tryb jasny: zamiana ikony na słońce
    icon.classList.remove("fa-moon");
    icon.classList.add("fa-sun");
  } else {
    // 🔸 Tryb ciemny: zamiana ikony na księżyc
    icon.classList.remove("fa-sun");
    icon.classList.add("fa-moon");
  }
}
