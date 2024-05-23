let loading = false;

document.addEventListener("keypress", async function(e) {
    if (e.key === "Enter") {
        await performSearch();
    }
});

document.querySelector('form').addEventListener('submit', async function(e) {
    e.preventDefault();
    await performSearch();
});

async function performSearch() {
    if (loading != true) {
        let loadingpage = document.getElementById("loadingpage");
        loadingpage.classList.remove("hidden");
        loading = true;

        const valueSearch = document.getElementById('searchbar').value;

        // Introduce un retraso mínimo de 1 segundo
        const minDelay = new Promise(resolve => setTimeout(resolve, 1000));

        try {
            //  Para subir cambiar fetch por https://gamewallet10.oa.r.appspot.com/search?q=' + valueSearch
            const response = await fetch('http://127.0.0.1:5555/search?q=' + valueSearch);
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            const data = await response.json();

            const boxGame = document.querySelectorAll(".col-span-1");

            for (let i = 0; i < boxGame.length; i++) {
                if (i < data.length) {
                    // Modificación de los spans
                    const listSpan = boxGame[i].querySelectorAll("span");
                    listSpan[0].innerText = data[i]['title'];
                    listSpan[1].innerText = data[i]['opinion'];
                    listSpan[2].innerText = data[i]['price'];
                    listSpan[3].innerHTML = data[i]['link'] != " - " ? '<a href="' + data[i]['link'] + '">Haz clic aquí</a>' : data[i]['link'];
                } else {
                    // Si no hay suficientes datos, limpiar o manejar adecuadamente los elementos restantes
                    const listSpan = boxGame[i].querySelectorAll("span");
                    listSpan[0].innerText = "No data";
                    listSpan[1].innerText = "";
                    listSpan[2].innerText = "";
                    listSpan[3].innerHTML = "";
                }
            }

            // Recupera todos los elementos de la página
            var element = document.querySelector(".container");
            var elements = element.querySelectorAll("*");

            elements.forEach(function(element) {
                if (element.classList.contains("hidden")) {
                    element.classList.remove("hidden");
                }

                if (element.classList.contains("w-9/12")) {
                    element.classList.add("hidden");
                }
            });
        } catch (error) {
            console.error('Error:', error);
        } finally {
            await minDelay;  // Espera al menos un segundo antes de continuar
            loading = false;
            loadingpage.classList.add("hidden");
        }
    }
}
