import gradio as gr #type: ignore
import numpy as np
from PIL import Image
from tensorflow.keras.models import load_model #type: ignore
from tensorflow.keras.preprocessing.image import img_to_array #type: ignore
import json

# Load model dan label encoding
model = load_model("D3(4HL+0.2D).h5", compile=False)

with open("label_encodings2.json", "r") as f:
    label_encodings = json.load(f)

# Balikkan encoding (index ke label)
reverse_encodings = {
    key: {int(v): k for k, v in value.items()}
    for key, value in label_encodings.items()
}

taxonomy_labels = ["kelas", "ordo", "famili", "genus", "spesies"]

def predict_taxonomy(image_array: np.ndarray):
    image = Image.fromarray(image_array.astype("uint8")).convert("RGB")
    image = image.resize((256, 256))
    array = img_to_array(image) / 255.0
    array = np.expand_dims(array, axis=0)
    predictions = model.predict(array)

    result = {}
    for i, label in enumerate(taxonomy_labels):
        pred_probs = predictions[i][0]
        pred_index = np.argmax(pred_probs)
        pred_label = reverse_encodings[label][pred_index]
        confidence = float(pred_probs[pred_index])
        result[label] = {"label": pred_label, "confidence": confidence}
    return result

interface = gr.Interface(
    fn=predict_taxonomy,
    inputs=gr.Image(type="numpy"),  # Ganti type ke "numpy"
    outputs=gr.JSON(),
    title="Klasifikasi Taksonomi Hewan",
    description="Upload gambar hewan untuk mendapatkan prediksi kelas taksonominya (kelas → spesies)."
)

if __name__ == "__main__":
    interface.launch(share=True)
