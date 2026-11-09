document.getElementById("registerForm").addEventListener("submit", async function (e) {
    e.preventDefault();
    const form = e.target;
    const messageBox = document.getElementById("registerMessage");
    messageBox.innerHTML = "";

    const formData = new FormData(form);
    const data = Object.fromEntries(formData.entries());
    delete data.csrfmiddlewaretoken;

    const csrfToken = form.querySelector('[name="csrfmiddlewaretoken"]').value;
    const url = form.dataset.url;

    try {
        const response = await fetch(url, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": csrfToken
            },
            body: JSON.stringify(data)
        });

        const result = await response.json();
        console.log("Сервер відповів:", result);

        if (response.ok) {
            messageBox.innerHTML =
                '<div class="alert alert-success mb-0">Успішно зареєстровано: ' +
                (result.username || data.username || '') + '</div>';
            form.reset();
        } else {
            messageBox.innerHTML =
                '<div class="alert alert-danger mb-0">Помилка: ' +
                (result.error || 'невідома') + '</div>';
        }
    } catch (error) {
        console.error("Помилка запиту:", error);
        messageBox.innerHTML =
            '<div class="alert alert-danger mb-0">Помилка з\'єднання з сервером.</div>';
    }
});
