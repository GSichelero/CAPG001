import numpy as np
from skimage.transform import hough_line, hough_line_peaks
from skimage.transform import rotate
from skimage.feature import canny
from skimage.io import imread
from skimage.color import rgb2gray
import matplotlib.pyplot as plt
from scipy.stats import mode

# Carregar e converter a imagem para escala de cinza
image = rgb2gray(imread("20241217_141417.jpg")[:,:,:3])

# Detecção de bordas
edges = canny(image)

# Aplicando a transformada de Hough
tested_angles = np.deg2rad(np.arange(0.1, 180.0))
h, theta, d = hough_line(edges, theta=tested_angles)

# Exibindo a transformada de Hough (acumulador)
plt.figure(figsize=(8, 6))
plt.imshow(h, cmap='gray', aspect='auto', extent=[theta.min(), theta.max(), d.min(), d.max()])
plt.title('Transformada de Hough')
plt.xlabel('Theta (radianos)')
plt.ylabel('Distância (ρ)')
plt.colorbar()
plt.show()

# Função para determinar o ângulo de inclinação (skew)
def skew_angle_hough_transform(image):
    edges = canny(image)
    tested_angles = np.deg2rad(np.arange(0.1, 180.0))
    h, theta, d = hough_line(edges, theta=tested_angles)
    accum, angles, dists = hough_line_peaks(h, theta, d)
    
    # Exibindo os picos da transformada de Hough
    print("Picos da Transformada de Hough:")
    for angle, dist in zip(angles, dists):
        print(f"Ângulo: {np.rad2deg(angle):.2f}°, Distância: {dist:.2f}")
    
    # Calculando o ângulo de rotação (skew)
    most_common_angle = mode(np.around(angles, decimals=2), keepdims=False)[0]
    skew_angle = np.rad2deg(most_common_angle - np.pi/2)  # Ajuste para 90 graus
    print(f"Ângulo de rotação (skew): {skew_angle:.2f}°")
    return skew_angle

# Aplicando a função de skew e exibindo a imagem original e rotacionada
fig, ax = plt.subplots(ncols=2, figsize=(20, 20))
ax[0].imshow(image, cmap="gray")
ax[0].set_title('Imagem Original')

# Corrigir a rotação (skew)
skew_angle = skew_angle_hough_transform(image)
ax[1].imshow(rotate(image, skew_angle, cval=1), cmap="gray")
ax[1].set_title(f'Imagem Corrigida (Rotacionada por {skew_angle:.2f}°)')

plt.show()