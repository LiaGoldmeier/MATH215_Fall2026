import streamlit as st
import numpy as np
from PIL import Image


# Transformation matrices

I = np.array([[1, 0],
              [0, 1]])

R90 = np.array([[0, -1],
                [1,  0]])

R180 = np.array([[-1,  0],
                 [ 0, -1]])

R270 = np.array([[ 0, 1],
                 [-1, 0]])

FV = np.array([[1,  0],
               [0, -1]])

FH = np.array([[-1, 0],
               [ 0, 1]])

FD1 = np.array([[0, 1],
                [1, 0]])

FD2 = np.array([[ 0, -1],
                [-1,  0]])


# General transformation function

def transform_image(image_array, M):

    height = image_array.shape[0]
    width = image_array.shape[1]

    corners = np.array([[0, 0],
                        [width - 1, 0],
                        [0, -(height - 1)],
                        [width - 1, -(height - 1)]])

    new_corners = (M @ corners.T).T

    min_x = int(np.min(new_corners[:, 0]))
    max_x = int(np.max(new_corners[:, 0]))
    min_y = int(np.min(new_corners[:, 1]))
    max_y = int(np.max(new_corners[:, 1]))

    new_width = max_x - min_x + 1
    new_height = max_y - min_y + 1

    transformed_array = np.zeros(
        (new_height, new_width, image_array.shape[2]),
        dtype=image_array.dtype
    )

    for y in range(height):
        for x in range(width):

            point = np.array([x, -y])
            new_point = M @ point

            new_x = int(new_point[0] - min_x)
            new_y = int(max_y - new_point[1])

            transformed_array[new_y, new_x] = image_array[y, x]

    return transformed_array


# Dictionary of transformations

transformations = {
    "Identity": I,
    "90-degree counterclockwise rotation": R90,
    "180-degree rotation": R180,
    "270-degree counterclockwise rotation": R270,
    "Vertical flip": FV,
    "Horizontal flip": FH,
    "Diagonal reflection (y = x)": FD1,
    "Diagonal reflection (y = -x)": FD2
}


# Website

st.title("Image Transformations Using Linear Algebra")

st.write("Explore rotations, reflections, and composition of transformation matrices.")

uploaded_file = st.file_uploader(
    "Upload an image",
    type=["png", "jpg", "jpeg"]
)

if uploaded_file is not None:

    image = Image.open(uploaded_file).convert("RGBA")
    image_array = np.array(image)

    # Select transformations

    first = st.selectbox(
        "First transformation",
        list(transformations.keys())
    )

    second = st.selectbox(
        "Second transformation",
        list(transformations.keys())
    )

    A = transformations[first]
    B = transformations[second]

    # Compose transformation matrices

    C = B @ A

    # Apply the composed transformation

    result = transform_image(image_array, C)

    # Display images side by side

    col1, col2 = st.columns(2)

    with col1:
        st.image(image_array, caption="Original Image")

    with col2:
        st.image(result, caption="Transformed Image")

    # Display transformation matrices side by side

    st.subheader("Transformation Matrices")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.write("First transformation")
        st.latex(rf"A=\begin{{pmatrix}}{A[0,0]}&{A[0,1]}\\{A[1,0]}&{A[1,1]}\end{{pmatrix}}")

    with col2:
        st.write("Second transformation")
        st.latex(rf"B=\begin{{pmatrix}}{B[0,0]}&{B[0,1]}\\{B[1,0]}&{B[1,1]}\end{{pmatrix}}")

    with col3:
        st.write("Composition")
        st.latex(rf"BA=\begin{{pmatrix}}{C[0,0]}&{C[0,1]}\\{C[1,0]}&{C[1,1]}\end{{pmatrix}}")

