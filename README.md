# Tarea 3 - Procesamiento de Señales e Imágenes

Implementación de filtro de difusión anisotrópica, basado en el artículo de Perona-Malik.

### Prerrequisitos

- Python 3.12
- pip 20.0 o superior

#### Instalación de dependencias

Este proyecto incluye un archivo `requirements.txt` con todas las dependencias necesarias. Para instalarlas ejecuta:

```bash
pip install -r requirements.txt
```

### Ejecución

1. Descargar código fuente o clonar repositorio.

2. Para ejecutar el programa, se debe abrir una terminal en el directorio de instalación y ejecutar:

```bash
python main.py
```

Luego seguir las indicaciones del menú interactivo del programa.

### Posibles errores

En sistemas Linux, puede ser que al intentar mostrar una imagen con el método `pyplot.imshow` arroje este error:

```shell
qt.qpa.plugin: From 6.5.0, xcb-cursor0 or libxcb-cursor0 is needed to load the Qt xcb platform plugin.
qt.qpa.plugin: Could not load the Qt platform plugin "xcb" in "" even though it was found.
This application failed to start because no Qt platform plugin could be initialized. Reinstalling the application may fix this problem.

Available platform plugins are: wayland, offscreen, minimalegl, xcb, minimal, eglfs, vnc, wayland-egl, linuxfb, vkkhrdisplay.

Aborted (core dumped)
```

Para esto se debe instalar la librería libxcb-cursor-dev la cual incluye la dependencia que este pide.

```shell
$ sudo apt install libxcb-cursor-dev
```

### Fuentes de las imágenes de prueba

- `2b2t_rick.png`: [2b2t Atlas](https://2b2tatlas.com/map)
- `canaletto.jpg`: [Art Institute of Chicago](https://www.artic.edu/artworks/159742/the-equestrian-monument-from-vedute)
- `Lichtenstein_test.png`: [Wikimedia Commons](https://commons.wikimedia.org/wiki/File:Lichtenstein_img_processing_test.png)
- `photographer.jpg`: [ResearchGate](https://www.researchgate.net/figure/The-cameraman-picture-with-256-256-size_fig3_329563816)