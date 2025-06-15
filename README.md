# Tarea 3 - Procesamiento de Señales e Imágenes

Implementación de filtro de difusión anisotrópica, basado en el artículo de Perona-Malik.

#### Posibles errores

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