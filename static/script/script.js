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
    if (loading) return;

    const loadingpage = document.getElementById("loadingpage");
    loadingpage.classList.remove("hidden");
    loading = true;

    const valueSearch = document.getElementById('searchbar').value;

    const minDelay = new Promise(resolve => setTimeout(resolve, 1000));

    try {
        //  Para subir cambiar fetch por https://gamewallet10.oa.r.appspot.com/search?q=' + valueSearch
        const response = await fetch('http://127.0.0.1:5555/search?q=' + valueSearch);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();

        const platforms = ["Steam", "IG", "G2A"];
        platforms.forEach((platform, index) => {
            const boxGame = document.getElementById(platform);
            const spans = boxGame.querySelectorAll("span");
            const img = boxGame.querySelector("img");

            if (index < data.length) {
                const game = data[index];
                spans[0].innerText = game.title;
                spans[1].innerText = game.opinion;
                spans[2].innerText = game.price;
                spans[3].innerHTML = game.link !== "-" ? `<a href="${game.link}">Haz clic aquí</a>` : game.link;
                img.src = game.picture_url !== "-" ? game.picture_url : "https://static.vecteezy.com/system/resources/thumbnails/024/405/934/small/icon-tech-error-404-icon-isolated-png.png";
            } else {
                spans[0].innerText = "No data";
                spans[1].innerText = "";
                spans[2].innerText = "";
                spans[3].innerHTML = "";
                img.src = "https://static.vecteezy.com/system/resources/thumbnails/024/405/934/small/icon-tech-error-404-icon-isolated-png.png"; // Imagen por defecto si no hay datos
            }
            boxGame.classList.remove('hidden');
        });

    } catch (error) {
        console.error('Error:', error);
    } finally {
        await minDelay;
        loading = false;
        loadingpage.classList.add("hidden");
    }
}
