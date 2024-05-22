const picture_url_error = "http://127.0.0.1:5555/static/img/error404.png"
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
    const response = await fetch('http://127.0.0.1:5555/api/?q=' + valueSearch);
      const data = await response.json();
  
      const boxGame = document.querySelectorAll(".col-span-1")
      for (let i = 0; i < boxGame.length ; i++) {
        // Modificación de la imagen
        boxGame[i].querySelectorAll("img")[1].src = data[i]['image'] != " - " ? data[i]['image'] : "https://static.vecteezy.com/system/resources/thumbnails/022/877/601/small_2x/3d-illustration-computer-error-object-png.png"
  
        // Modificación de los spans
        const listSpan = boxGame[i].querySelectorAll("span")
        listSpan[0].innerText = data[i]['title']
        listSpan[1].innerText = data[i]['opinion']
        listSpan[2].innerText = data[i]['price']
        listSpan[3].innerHTML = data[i]['link'] != " - " ? '<a href="' + data[i]['link'] + '">Haz clic aquí</a>' : data[i]['link']
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
  
      loading = false;
      loadingpage.classList.add("hidden");
    }
  }
  