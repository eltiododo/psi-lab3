import numpy as np
import matplotlib.pyplot as plt
from scipy import ndimage as ndi
from skimage import util, color, io
from utils import bulk_plot, params_to_str

def anisotropic_diffusion(image: np.ndarray, diffusion_function, 
                          iters: int = 10, kappa: float = 0.10, lambda_: float = 0.25,
                          kappa_percentile: None | float = None) -> np.ndarray:
    '''
    Método principal para realizar difusión anisotrópica en una imagen en escala de grises
    Args:
        image (np.ndarray): Imagen de entrada, arreglo numerico
        diffusion_function (function): Función de difusión
        iters (int): Número de iteraciones
        kappa (float): Umbral de contraste, clasifica gradientes como bordes o no.
        lambda_ (float): Factor de escala
        kappa_percentile (float): Si se especifica, se calcula kappa como el percentil de los gradientes de la imagen.
    Returns:
        current_image (np.ndarray): Imagen resultante después de la difusión anisotrópica.
        
    '''
    
    if image.ndim != 2:
        raise ValueError("La imagen debe ser en escala de grises.")

    current_image = image.copy()

    # En caso de que se especifique kappa_percentile, calcular kappa
    if (kappa_percentile):
        kappa = estimate_kappa(current_image, kappa_percentile)

    for i in range(iters):
        nabla_n, nabla_s, nabla_e, nabla_w = [np.zeros_like(current_image) for _ in range(4)]

        # Calcular gradientes en las cuatro direcciones, en orden (Ec. 8):
        #   norte:  I(i-1, j) - I(i, j)
        #   sur:    I(i+1, j) - I(i, j)
        #   este:   I(i, j+1) - I(i, j)
        #   oeste:  I(i, j-1) - I(i, j)
        nabla_n[1:, :] = current_image[:-1, :] - current_image[1:, :]
        nabla_s[:-1, :] = current_image[1:, :] - current_image[:-1, :]
        nabla_e[:, 1:] = current_image[:, :-1] - current_image[:, 1:]
        nabla_w[:, :-1] = current_image[:, 1:] - current_image[:, :-1]

        # Calcular coeficientes c(x,y,t) = g(|nabla|), aproximacion de (Ec. 10)
        c_n, c_s, c_e, c_w = [diffusion_function(np.abs(nabla_x), kappa) for nabla_x in (nabla_n, nabla_s, nabla_e, nabla_w)]

        # Calcular laplaciano discreto y actualizar imagen, (Ec. 7)
        laplacian = (c_n * nabla_n + c_s * nabla_s + c_e * nabla_e + c_w * nabla_w)
        current_image += lambda_ * laplacian

    params = {
        'iters': iters,
        'kappa': kappa,
        'lambda': lambda_
    }
    return current_image, params

## Funciones de difusión

def diffusion_type_1(nabla: np.ndarray, kappa: float) -> np.ndarray:
    return np.exp(-(nabla / kappa) ** 2)

def diffusion_type_2(nabla: np.ndarray, kappa: float) -> np.ndarray:
    return 1 / (1 + (nabla / kappa) ** 2)

def diffusion_charbonnier(nabla: np.ndarray, kappa: float) -> np.ndarray:
    return 1 / np.sqrt(1 + (nabla / kappa) ** 2)

# Estimación de kappa basada en el percentil del gradiente de la imagen
def estimate_kappa(image: np.ndarray, percentile: float = 90.0) -> float:
    # Calcular gradiente
    grad_x, grad_y = np.gradient(image)
    grad_magni = np.sqrt(grad_x ** 2 + grad_y ** 2) 

    # Calcular kappa como el percentil especificado
    k = np.percentile(grad_magni.flatten(), percentile)
    return k

# Testeo
if __name__ == '__main__':
    # Cargar una imagen de ejemplo
    image = io.imread('images/canaletto.jpg', as_gray = True)

    result, params = anisotropic_diffusion(image, diffusion_type_2, iters = 60, lambda_ = 0.095, kappa = 0.09)
    #result_2, params_2 = anisotropic_diffusion(image, diffusion_type_2, iters = 166, lambda_ = 0.15, kappa_percentile = 80.0)
    #result_ch, params_ch = anisotropic_diffusion(image, diffusion_charbonnier, iters = 60, lambda_ = 0.0999, kappa_percentile = 95.0)

    # Mostrar la imagen original y el resultado
    bulk_plot(
        [image, result],#, result_2, result_ch],
        
        titles = ['Imagen Original',
                  diffusion_type_1.__name__],#, 
                  #diffusion_type_2.__name__, 
                  #diffusion_charbonnier.__name__],
        
        xlabs = ["", 
                 params_to_str(params)],#,
                 #params_to_str(params_2),
                 #params_to_str(params_ch)],
        
        cols = 2,
        figsize = (10, 10),
        cmap = 'copper'
    )