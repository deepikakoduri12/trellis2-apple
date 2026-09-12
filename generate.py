import os
import gc
import argparse

import torch
from PIL import Image

from trellis2.pipelines import Trellis2ImageTo3DPipeline
import o_voxel


# --------------------------------------------------
# Settings
# --------------------------------------------------

DEVICE = torch.device("mps")

# Same pipeline used by the app
PIPELINE_TYPE = "1024_cascade"

# Keep the same high-quality settings used by TRELLIS.2
MAX_NUM_TOKENS = 49152

# Decimate only if necessary; 0 means keep the generated mesh.
DECIMATION_TARGET = 16777216

TEXTURE_SIZE = 1024


# --------------------------------------------------
# Command-line arguments
# --------------------------------------------------

parser = argparse.ArgumentParser(
    description="Generate a 3D GLB from an image using TRELLIS.2"
)

parser.add_argument(
    "input_image",
    help="Path to the input image"
)

parser.add_argument(
    "-o",
    "--output",
    required=True,
    help="Path where the generated GLB should be saved"
)

args = parser.parse_args()

IMAGE_PATH = os.path.expanduser(args.input_image)
OUTPUT_PATH = os.path.expanduser(args.output)


# --------------------------------------------------
# Validate input
# --------------------------------------------------

if not os.path.isfile(IMAGE_PATH):
    raise FileNotFoundError(f"Input image not found: {IMAGE_PATH}")


# --------------------------------------------------
# Load model
# --------------------------------------------------

print("Loading TRELLIS.2...")

pipeline = Trellis2ImageTo3DPipeline.from_pretrained(
    "microsoft/TRELLIS.2-4B"
)

pipeline.to(DEVICE)

print("Model loaded on:", DEVICE)


# --------------------------------------------------
# Load image
# --------------------------------------------------

image = Image.open(IMAGE_PATH).convert("RGB")

print("Input image:", IMAGE_PATH)
print("Image size:", image.size)


# --------------------------------------------------
# Generate 3D
# --------------------------------------------------

print()
print("Generating 3D mesh...")
print("This can take several minutes on MPS.")
print()

outputs = pipeline.run(
    image,
    num_samples=1,
    seed=42,
    preprocess_image=True,
    return_latent=False,
    pipeline_type=PIPELINE_TYPE,
    max_num_tokens=MAX_NUM_TOKENS,
)

print()
print("3D generation complete.")


# --------------------------------------------------
# Get generated mesh
# --------------------------------------------------

mesh = outputs[0]

print("Vertices:", mesh.vertices.shape)
print("Faces:", mesh.faces.shape)


# --------------------------------------------------
# Postprocess / remesh / export
# --------------------------------------------------

print()
print("Creating GLB...")
print("Remeshing enabled.")

glb = o_voxel.postprocess.to_glb(
    vertices=mesh.vertices,
    faces=mesh.faces,
    attr_volume=mesh.attrs,
    coords=mesh.coords,
    attr_layout=pipeline.pbr_attr_layout,
    grid_size=mesh.voxel_shape[-1],
    aabb=[[-0.5, -0.5, -0.5], [0.5, 0.5, 0.5]],
    decimation_target=DECIMATION_TARGET,
    texture_size=TEXTURE_SIZE,
    remesh=True,
    remesh_band=1,
    remesh_project=0,
    use_tqdm=True,
)

glb.export(OUTPUT_PATH, extension_webp=True)

print()
print("========================================")
print("DONE!")
print("========================================")
print("Saved:", OUTPUT_PATH)


# --------------------------------------------------
# Cleanup
# --------------------------------------------------

gc.collect()

if hasattr(torch, "mps"):
    torch.mps.empty_cache()
