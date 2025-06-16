import utils
import anisotropic as aniso
from skimage import io

# Variables globales
image = None
image_path = None
diffusion_function = None
params = {}

# Mostrar opciones y leer seleccionada (general)
def options_prompt(options: list) -> int:
    for i, option in enumerate(options, 1):
        print(f"{i}. {option}")
    
    print("==========================================================")
    print("Seleccione una opción:", end = " ")

    # Loop para leer entrada
    while True:
        try:
            choice = int(input())
            
            # Validar que esté dentro del rango de opciones
            if 1 <= choice <= len(options):
                return choice
            else:
                print(f"Por favor, ingrese un número entre 1 y {len(options)}.")

        except ValueError:
            print("Entrada inválida. Por favor, ingrese un número:", end = " ")

# ========== Funciones del menu principal ==========

# Opcion 1: Subir imagen
def upload_image():
    global image, image_path
    image_path = input("Ingrese la ruta de la imagen: ")
    
    try:
        image = io.imread(image_path, as_gray=True)
        image = utils.util.img_as_float(image)  # Convertir a float si es necesario
        print(f"Imagen cargada con éxito. Dimensiones: {image.shape}")
    
    except Exception as e:
        print(f"Error al cargar la imagen: {e}")
        return None

# Opcion 2: Casos de ejemplo
def example_images():
    global image, image_path, params
    # Cargar imágenes de ejemplo

    options = ["Rick Astley", "Canaletto", "Castillo de Lichtenstein", "Fotografo"]
    paths = ["2b2t_rick.png", "canaletto.jpg", "Lichtenstein_test.png", "photographer.jpg"]
    params = [
        {'iters': 266, 'kappa': 0.0666, 'lambda': 0.24},
        {'iters': 60, 'kappa': 0.09, 'lambda': 0.095},
        {'iters': 50, 'kappa': 0.1, 'lambda': 0.15},
        {'iters': 60, 'kappa': 0.0999, 'lambda': 0.15}
    ]

    choice = options_prompt(options) - 1 # 0 indexed
    image_path = f"images/{paths[choice]}"
    image = io.imread(image_path, as_gray = True)
    params = params[choice]

    
# Opcion 3. Editar Parametros del filtro
def edit_filter_params():
    global params

    print("Ingrese los nuevos parámetros del filtro")
    try:
        iters = int(input("Número de iteraciones: "))
        kappa = float(input("Valor de kappa (ingresar 0 para estimarlo): "))
        lambda_ = float(input("Valor de lambda: "))

        params = {
            'iters': iters,
            'kappa': kappa,
            'lambda': lambda_
        }
        print("Parámetros actualizados correctamente.")
    
    except ValueError as e:
        print(f"Error al ingresar los parámetros: {e}")
    
# Opcion 4. Aplicar filtro
def apply_filter():
    global image, params, diffusion_function

    if image is None:
        print("No hay imagen cargada. Por favor, suba una imagen primero.")
        return

    # Seleccionar función de difusión
    options = [
        "Difusión tipo 1: exp(-|x|^2 / K^2)", 
        "Difusión tipo 2: 1 / (1 + |x|^2 / K^2)", 
        "Difusión Charbonnier: 1 / sqrt(1 + |x|^2 / K^2)"
    ]
    choice = options_prompt(options) - 1  # 0 indexed

    switcher = {
        0: aniso.diffusion_type_1,
        1: aniso.diffusion_type_2,
        2: aniso.diffusion_charbonnier
    }

    diffusion_function = switcher.get(choice)

    # Aplicar filtro anisotrópico
    print("Aplicando filtro anisotrópico...")
    result_image, applied_params = aniso.anisotropic_diffusion(
        image,
        diffusion_function,
        iters = params['iters'],
        lambda_ = params['lambda'],
        kappa = params['kappa'],
        kappa_percentile = 90.0 if params['kappa'] == 0 else None
    )

    # Mostrar resultados
    print("Filtro aplicado, mostrando resultados...")
    print("\tCierra la ventana emergente para continuar.")
    utils.bulk_plot(
        [image, result_image],
        titles = ['Imagen Original', diffusion_function.__name__],
        xlabs = ["", utils.params_to_str(applied_params)],
        cols = 2,
        figsize = (10, 5),
        cmap = 'gray'
    )

# Menu de opciones
def menu_loop():
    print("\n============= Filtro de Difusión Anisotrópica =============")
    
    # Imagen actual
    if image is None:
        print("No hay imagen cargada.")
    else:
        print(f"Imagen cargada: {image_path} (Dimensiones: {image.shape})")

    # Mostrar parámetros actuales
    if not params:
        print("No hay parámetros de filtro definidos,", end = " ")
        print("se usarán valores por defecto (iters = 10, kappa = 0.1, lambda = 0.25).")
    else:
        print("Parámetros actuales del filtro:")
        for key, value in params.items():
            
            # mostrar texto especial si kappa es 0
            if key == 'kappa' and value == 0:
                print(f"\t{key} estimado con el percentil 90% del gradiente de la imagen.")
            
            else:
                print(f"\t{key}: {value}")

        print()

    options = ["Subir imagen", "Casos de ejemplo", "Editar parametros del filtro", "Aplicar filtro", "Salir"]
    choice = options_prompt(options)

    switcher = {
        1: upload_image,
        2: example_images,
        3: edit_filter_params,
        4: apply_filter,
        5: exit
    }

    switcher.get(choice)()


if __name__ == "__main__":
    while True:
        menu_loop()