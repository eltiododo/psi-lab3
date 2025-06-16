import matplotlib.pyplot as plt
import numpy as np

from skimage import io, color, util

def bulk_plot(images, titles = None, xlabs = None, cols = 3, figsize = (15, 15), cmap = 'gray'):
    """
    Grafica un cjto. de imágenes con títulos y etiquetas opcionales.
    
    Args:
        images (list): Lista de imagenes
        titles (list): Lista de strings para usar como títulos de las imágenes.
        cols (int): Number of columns in the grid.
        figsize (tuple): Tamaño de la figura (ancho, alto).
        cmap (str): Mapa de colores a usar para las imágenes.
        xlabs (list): Lista de strings para usar como etiquetas de los ejes x.
    """
    # resetear para evitar errores al usar filtro mas de una vez
    plt.close('all')
    plt.rcParams['text.usetex'] = False

    # calcular dimensiones para el grafico
    n_images = len(images)
    rows = (n_images + cols - 1) // cols
    fig, axs = plt.subplots(rows, cols, figsize = figsize)
    
    # Caso de una sola imagen
    if n_images == 1:
        axs = np.array([[axs]])

    for i, ax in enumerate(axs.flat):
        # Si hay más ejes que imágenes, ocultar los ejes sobrantes
        if i >= n_images:
            ax.axis('off')
            continue
            
        if titles:
            ax.set_title(titles[i])

        if xlabs:
            ax.set_xlabel(xlabs[i], fontsize = 8)

        ax.set_xticks([])
        ax.set_yticks([])
        ax.imshow(images[i], cmap = cmap)

    plt.rcParams['text.usetex'] = True # usar LaTeX para los títulos
    plt.rcParams['font.family'] = 'sans-serif'
    plt.subplots_adjust(wspace = 0.05, hspace = 0.35)
    plt.show()

def params_to_str(params: dict) -> str:
    
    # mostrar floats con 3 decimales
    # floats -> tienen como key una letra griega (\lambda, \kappa)
    # el otro es iters, mostrar normalmente
    params_str = [f"$\\{k} = {v:.3f}$" if isinstance(v, float) else f"${k} = {v}$" for k, v in params.items()]
    return ', '.join(params_str)

# Test
if __name__ == '__main__':
    img = io.imread('images/2b2t_rick.png', as_gray = True)

    print("Image shape:", img.shape)
    bulk_plot([img], titles=['Test Image'], cols = 1, figsize = (5, 5), cmap = 'gray')
    