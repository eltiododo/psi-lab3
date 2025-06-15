import numpy as np
import matplotlib.pyplot as plt
from scipy import ndimage as ndi
from skimage import util, color, io

def anisotropic_diffusion(image: np.ndarray, diffusion_function, 
                          iters: int = 10, kappa: float = 30.0, lambda_: float = 0.25,
                          estimate_k: bool = False) -> np.ndarray:
    '''
    Método principal para realizar difusión anisotrópica en una imagen en escala de grises
    Args:
        image (np.ndarray): Imagen de entrada, arreglo numerico
        g (function): Función de difusión
        iters (int): Número de iteraciones
        kappa (float): Umbral de contraste, clasifica gradientes como bordes o no.
        lambda_ (float): Factor de escala
    '''
    
    if image.ndim != 2:
        raise ValueError("La imagen debe ser en escala de grises.")

    current_image = image.copy()

    if (estimate_k):
        kappa = estimate_kappa(current_image, 90.0)

    for i in range(iters):
        nabla_n, nabla_s, nabla_e, nabla_w = [np.zeros_like(current_image) for _ in range(4)]

        # Calcular gradientes en las cuatro direcciones, en orden:
        #   norte:  I(i-1, j) - I(i, j)
        #   sur:    I(i+1, j) - I(i, j)
        #   este:   I(i, j+1) - I(i, j)
        #   oeste:  I(i, j-1) - I(i, j)
        nabla_n[1:, :] = current_image[:-1, :] - current_image[1:, :]
        nabla_s[:-1, :] = current_image[1:, :] - current_image[:-1, :]
        nabla_e[:, 1:] = current_image[:, :-1] - current_image[:, 1:]
        nabla_w[:, :-1] = current_image[:, 1:] - current_image[:, :-1]

        # Calcular coeficientes g(|nabla|)
        c_n, c_s, c_e, c_w = [diffusion_function(nabla_x, kappa) for nabla_x in (nabla_n, nabla_s, nabla_e, nabla_w)]

        # Calcular laplaciano discreto y actualizar imagen, Ec. 7
        laplacian = (c_n * nabla_n + c_s * nabla_s + c_e * nabla_e + c_w * nabla_w)
        current_image += lambda_ * laplacian

    return current_image, kappa

## Funciones de difusión

def diffusion_type_1(nabla: np.ndarray, kappa: float) -> np.ndarray:
    return np.exp(-(nabla / kappa) ** 2)

def diffusion_type_2(nabla: np.ndarray, kappa: float) -> np.ndarray:
    return 1 / (1 + (nabla / kappa) ** 2)

def diffusion_charbonnier(nabla: np.ndarray, kappa: float) -> np.ndarray:
    return 1 / np.sqrt(1 + (nabla / kappa) ** 2)

def estimate_kappa(image: np.ndarray, percentile: float = 90.0) -> float:
    # Calcular gradiente con filtros de Sobel
    grad_x = np.gradient(image, axis = 1)
    grad_y = np.gradient(image, axis = 0)
    grad_magni = np.sqrt(grad_x ** 2 + grad_y ** 2) 
    
    # Calcular kappa como el percentil especificado del gradiente
    k = np.percentile(grad_magni, percentile)
    return k

# Testeo
if __name__ == '__main__':
    # Cargar una imagen de ejemplo
    np.random.seed(1984)
    #image = np.random.rand(100, 100)  # Imagen aleatoria para el ejemplo

    image = io.imread('images/2b2t_rick.png', as_gray = True)

    ITERS = 250
    LAMBDA = 0.24
    KAPPA = 0.0666666
    result, k = anisotropic_diffusion(image, diffusion_type_1, iters = ITERS, lambda_ = LAMBDA, kappa = KAPPA)

    # Mostrar la imagen original y el resultado
    fig, axs = plt.subplots(1, 2, figsize=(12, 6))
    
    axs[0].set_title('Imagen Original')
    axs[0].imshow(image, cmap = 'copper')
    
    axs[1].set_title('Resultado de Difusión Anisotrópica')

    axs[1].set_xlabel(f"{ITERS} iteraciones, lambda = {LAMBDA}, kappa = {k:.3f}")
    axs[1].imshow(result, cmap = 'copper')
    
    plt.show()