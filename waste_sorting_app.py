"""Streamlit app for image-based waste sorting recommendations."""
from __future__ import annotations

from typing import List

import streamlit as st
import torch
from PIL import Image
from torchvision import models, transforms

from waste_classifier import Prediction, pick_waste_bin


@st.cache_resource
def load_model() -> tuple[torch.nn.Module, List[str]]:
    weights = models.ResNet18_Weights.DEFAULT
    model = models.resnet18(weights=weights)
    model.eval()
    labels = list(weights.meta["categories"])
    return model, labels


def classify_image(image: Image.Image, top_k: int = 5) -> List[Prediction]:
    model, labels = load_model()
    preprocess = transforms.Compose(
        [
            transforms.Resize(256),
            transforms.CenterCrop(224),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
        ]
    )

    tensor = preprocess(image).unsqueeze(0)
    with torch.no_grad():
        logits = model(tensor)
        probabilities = torch.nn.functional.softmax(logits[0], dim=0)

    top_probs, top_indices = torch.topk(probabilities, k=top_k)
    return [
        Prediction(label=labels[index], confidence=float(prob))
        for prob, index in zip(top_probs.tolist(), top_indices.tolist())
    ]


def main() -> None:
    st.set_page_config(page_title="Waste Sorter", page_icon="♻️")
    st.title("♻️ Waste Sorting Assistant")
    st.write(
        "Upload a photo of an item and this app will suggest whether it belongs in recycling, compost, or trash."
    )

    uploaded = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png", "webp"])

    if uploaded is None:
        st.info("Add an image to get started.")
        return

    image = Image.open(uploaded).convert("RGB")
    st.image(image, caption="Uploaded image", use_container_width=True)

    with st.spinner("Analyzing image..."):
        predictions = classify_image(image)
        recommendation, reason = pick_waste_bin(predictions)

    badge = {
        "recycling": "♻️ Recycling",
        "compost": "🌱 Compost",
        "trash": "🗑️ Trash",
    }[recommendation]

    st.subheader(f"Recommendation: {badge}")
    st.write(reason)

    st.markdown("### Top visual matches")
    for pred in predictions:
        st.write(f"- {pred.label}: {pred.confidence:.1%}")

    st.caption("This is a best-effort assistant. Follow your local municipality guidelines when in doubt.")


if __name__ == "__main__":
    main()
