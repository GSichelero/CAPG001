import glm
import math

def calculate_frustum_parameters(fov_degrees, aspect_ratio, near, far):
    fov_radians = math.radians(fov_degrees)
    h = 2 * math.tan(fov_radians / 2) * near
    w = h * aspect_ratio

    top = h / 2
    bottom = -h / 2
    right = w / 2
    left = -w / 2
    
    return left, right, bottom, top, near, far


fov = 30
aspect_ratio = 1.5
near = 2
far = 100

perspective_matrix = glm.perspective(glm.radians(fov), aspect_ratio, near, far)
print("Perspective Matrix:")
print(perspective_matrix)

left, right, bottom, top, near, far = calculate_frustum_parameters(fov, aspect_ratio, near, far)

frustum_matrix = glm.frustum(left, right, bottom, top, near, far)
print("\nFrustum Matrix:")
print(frustum_matrix)

# print the frustum parameters
print("\nFrustum Parameters:")
print(f"Left: {left}")
print(f"Right: {right}")
print(f"Bottom: {bottom}")
print(f"Top: {top}")
print(f"Near: {near}")
print(f"Far: {far}")