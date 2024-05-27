# Game Wallet 
Es una proyecto desarrollado para la asignaruta Ingerieria de sistemas de la información en la cual mediante web scraping se obtienen los precios de los juegos en las diferentes plataformas la aplicación esta desarrollada en python y como framework web flask+Jinja y javascript.

Como parte fundamental del proyecto se pedia el deploy en algun servicio cloud El que elegí fue google cloud a continuacion hay un tutorial para conseguir hacer funcionar la aplicacion en Google app engine con una maquina flexible. Tambien he incluido un tutorial basico para poder ejecutar la aplición en local.

Esta aplicacion aunque es funcional y cumple todos los requisitos de la practica faltan cosa por pulir como: añadir una base de datos para agilizar los tiempos de carga y añadir otra pagina de web scraping la cual no esta implementada G2A(Debido a falta de tiempo para la entrega)

Creditos a @Pierre y @Thibault ya que el frontend esta basado en su proyecto.



## Features

- Web scraping:
    - Beatiful soup 4 para Steam
    - Selenium Webdriver para G2A e Instant Gaming 
- APIs
    - Epic games: https://github.com/Tectors/EpicGraphQL.git
- Pantalla de cargar.
- Interfaz intuitiva y responsive


## Run Locally : Como instalar y ejecutar en local

Importante tener python instalado

```bash
pip --version
```

```bash
git clone https://github.com/DmCerezo/Proyecto-Web-Scraping-ISI-UGR.git
```
## Abrir el entorno de trabajo
```bash
 python -m venv env  
```
```bash
.\env\Scripts\activate 
```
```bash
pip install -r requirements.txt
```

## Encender la aplicacion

```bash
python app.py
```

## Para ver la aplicacion en local
Ir a `http://127.0.0.1:5555`


## Deployment google cloud
iniciar shell de google cloud
```bash
git clone https://github.com/DmCerezo/Proyecto-Web-Scraping-ISI-UGR.git
```

o si ya esta copiado solo
```bash
git pull
```

Lanzar la aplicación
```bash
gcloud app deploy
```

Obtener link de la aplicación
```bash
gcloud app browse
```

## Demo
![cap1](https://github.com/DmCerezo/Proyecto-Web-Scraping-ISI-UGR/assets/127233730/3c0acf63-158e-4351-978d-75fcc24be7c2)
![cap2](https://github.com/DmCerezo/Proyecto-Web-Scraping-ISI-UGR/assets/127233730/ed85e6bf-bbcd-4a9a-9cb8-cc7adc83a415)
