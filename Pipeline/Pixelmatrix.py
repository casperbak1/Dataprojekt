import pandas as pd
import cv2
import os
import numpy as np
from tqdm import tqdm
import plotly.graph_objects as go


# === CONFIGURATION ===
# === PATHS (relative) ===
csv_path = "Predicted_keypoints.csv"
image_folder = os.path.join("Pipeline_data", "Clean data", "Overbite Data" )
output_csv_path = "Predicted_keypoints_pixel_matrix.csv"


# === LOAD CSV ===
df = pd.read_csv(csv_path)

# Prepare a list to store new refined points
refined_data = []

# === UTILITY FUNCTION ===
def refine_guess_with_pixel_matrix(image, x_center, y_center, window_size=15): # ÆNDRER MIG FOR MATRIX STØRRELSE
    half_size = window_size // 2
    x_min = int(max(x_center - half_size, 0))
    x_max = int(min(x_center + half_size + 1, image.shape[1]))
    y_min = int(max(y_center - half_size, 0))
    y_max = int(min(y_center + half_size + 1, image.shape[0]))

    sub_img = image[y_min:y_max, x_min:x_max]
    
    # Convert to grayscale for intensity checks
    gray = cv2.cvtColor(sub_img, cv2.COLOR_BGR2GRAY)
    
    # Find non-black pixels
    non_black_pixels = np.argwhere(gray > 0)
    if len(non_black_pixels) == 0:
        return x_center, y_center  # fallback: no adjustment

    # Find topmost (lowest y) non-black pixel(s)
    top_y = np.min(non_black_pixels[:, 0])
    top_pixels = non_black_pixels[non_black_pixels[:, 0] == top_y]
    
    # Among those, find the brightest
    brightness = [gray[pt[0], pt[1]] for pt in top_pixels]
    brightest_idx = np.argmax(brightness)
    top_pixel = top_pixels[brightest_idx]

    # Convert local (within sub-image) back to global coordinates
    refined_x = x_min + top_pixel[1]
    refined_y = y_min + top_pixel[0]
    return refined_x, refined_y

# === MAIN LOOP ===
for idx, row in tqdm(df.iterrows(), total=len(df)):
    filename = row['Filename'] + ".png"
    img_path = os.path.join(image_folder, filename)
    if not os.path.exists(img_path):
        print(f"Missing: {filename}")
        continue

    image = cv2.imread(img_path)
    if image is None:
        print(f"Could not read: {filename}")
        continue

    x_model = int(row['X_Model'])
    y_model = int(row['Y_Model'])

    x_refined, y_refined = refine_guess_with_pixel_matrix(image, x_model, y_model)


    # Load image
    im = cv2.imread(img_path)
    im_rgb = cv2.cvtColor(im, cv2.COLOR_BGR2RGB)
    height, width = im.shape[:2]

    # Set keypoints
    x_model, y_model = int(row['X_Model']), int(row['Y_Model'])
    x_refined, y_refined = int(x_refined), int(y_refined)

    # === Start Plotly Figure ===
    fig = go.Figure()

    # --- Background Image ---
    fig.add_trace(go.Image(z=im_rgb, name="Image"))


    # --- Model Guess Keypoint (Red) ---
    fig.add_trace(go.Scatter(
        x=[x_model], y=[y_model],
        mode='markers+text',
        name="Model Guess",
        text=["Model"],
        textposition="top right",
        marker=dict(color='red', size=5),
        showlegend=True
    ))

    # --- Refined Keypoint (Blue) ---
    fig.add_trace(go.Scatter(
        x=[x_refined], y=[y_refined],
        mode='markers+text',
        name="Refined Keypoint",
        text=["Refined"],
        textposition="top right",
        marker=dict(color='blue', size=5),
        showlegend=True
    ))

    # --- 15x15 Pixel Search Window (Yellow BBox) ---
    half_size = 15 // 2
    bbox_x0 = x_model - half_size
    bbox_y0 = y_model - half_size
    bbox_x1 = x_model + half_size
    bbox_y1 = y_model + half_size

    # Define bounding box as line loop
    fig.add_trace(go.Scatter(
        x=[bbox_x0, bbox_x1, bbox_x1, bbox_x0, bbox_x0],
        y=[bbox_y0, bbox_y0, bbox_y1, bbox_y1, bbox_y0],
        mode='lines',
        name="15x15 Window",
        line=dict(color='yellow', dash='dash', width=1),
        showlegend=True
    ))

    # === Layout ===
    fig.update_layout(
        title=f"Pixel Matrix Refinement: {row['Filename']}",
        xaxis=dict(visible=False, range=[0, width], scaleanchor="y", constrain="domain"),
        yaxis=dict(visible=False, range=[height, 0], scaleanchor="x", constrain="domain"),
        showlegend=True,
        height=height,
        width=width,
        margin=dict(l=0, r=0, t=40, b=0),
        plot_bgcolor='white',
        paper_bgcolor='white'
    )

    #fig.show(renderer="browser")
    # Create output folder if needed
    output_html_dir = os.path.join("Output_after_pixel_matrix")
    os.makedirs(output_html_dir, exist_ok=True)

    # Save to HTML
    html_path = os.path.join(output_html_dir, f"{row['Filename']}.html")
    fig.write_html(html_path)


    # === Append Data ===
    refined_data.append({
        'Filename': row['Filename'],
        'X_Model': x_model,
        'Y_Model': y_model,
        'X_Refined': x_refined,
        'Y_Refined': y_refined,
    })


# === SAVE OUTPUT ===
refined_df = pd.DataFrame(refined_data)
refined_df.to_csv(output_csv_path, index=False)
print(f"Saved refined results to {output_csv_path}")