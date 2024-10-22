import numpy as np

# Definindo os vetores u, v e w
u = np.array([1, 1, 0])
v = np.array([0, 2, 3])
w = np.array([2, 4, 3])

# Função para calcular o ângulo entre dois vetores
def angle_between(v1, v2):
    dot_product = np.dot(v1, v2)
    print(dot_product, v1, v2)
    norm_v1 = np.linalg.norm(v1)
    norm_v2 = np.linalg.norm(v2)
    cos_theta = dot_product / (norm_v1 * norm_v2)
    print(cos_theta)
    return np.arccos(cos_theta) * (180 / np.pi)  # Convertendo para graus

# Calculando os ângulos
angle_uv = angle_between(u, v)
angle_uw = angle_between(u, w)
angle_vw = angle_between(v, w)

angle_uv, angle_uw, angle_vw

print(angle_uv, angle_uw, angle_vw)

cross_uv = np.cross(u, v)
cross_uw = np.cross(u, w)
cross_vw = np.cross(v, w)

cross_uv, cross_uw, cross_vw

print(cross_uv, cross_uw, cross_vw)

u_new = np.array([-2, 3, 1])
v_new = np.array([0, 4, 1])

# Calculando o produto vetorial
cross_product = np.cross(u_new, v_new)

# Calculando a magnitude do produto vetorial (área do paralelogramo)
area = np.linalg.norm(cross_product)
cross_product, area
print(cross_product, area)