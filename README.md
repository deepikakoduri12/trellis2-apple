# TRELLIS.2 for Apple Silicon

Run **TRELLIS.2 image-to-3D generation locally on Apple Silicon Macs**.

This repository builds on **Microsoft's TRELLIS.2** and the Apple Silicon work from **Pedro Augusto's [`trellis2-apple`](https://github.com/pedronaugusto/trellis2-apple)**.

The goal of this repository is to provide a practical way to run TRELLIS.2 locally on Apple Silicon and generate 3D models from images.

---

## 🍎 Apple Silicon

This repository builds on:

* [Microsoft TRELLIS.2](https://github.com/microsoft/TRELLIS.2)
* [Pedro Augusto's `trellis2-apple`](https://github.com/pedronaugusto/trellis2-apple)

Pedro's work adds an Apple Silicon implementation of TRELLIS.2 using MLX and Metal acceleration.

During testing on Apple Silicon, we were able to run the TRELLIS.2 generation pipeline, but encountered CUDA-dependent issues in parts of the interactive preview/rendering path.

Rather than modify the entire rendering stack, this repository uses a focused command-line workflow through `generate.py` for the part needed to generate a 3D model and export it as a GLB.

The tested workflow is:

```text
Image
  ↓
TRELLIS.2
  ↓
Apple Silicon / MPS
  ↓
3D Mesh
  ↓
O-Voxel
  ↓
GLB
```

This workflow has been successfully tested on an Apple Silicon M5 Max with 64 GB unified memory.

---

# 🚀 Quick Start

## 1. Clone the repository

Clone the repository with its submodules:

```bash
git clone --recursive <YOUR_REPOSITORY_URL>
cd trellis2-apple
```

If you already cloned the repository without submodules:

```bash
git submodule update --init --recursive
```

---

## 2. Create the Conda environment

Python 3.11 is recommended.

```bash
conda create -n trellis2-apple311 python=3.11 -y
conda activate trellis2-apple311
```

---

## 3. Install dependencies

Install the macOS dependencies:

```bash
pip install -r requirements_macos.txt
```

Install the required `utils3d` version:

```bash
pip install "git+https://github.com/EasternJournalist/utils3d.git@9a4eb15e4021b67b12c460c7057d642626897ec8"
```

Install O-Voxel:

```bash
pip install -e ./o_voxel --no-build-isolation
```

Verify the O-Voxel installation:

```bash
python -c "import o_voxel; print('o_voxel OK')"
```

---

# 🎨 Generate a 3D Model

The recommended Apple Silicon workflow uses `generate.py`.

Provide an input image and an output GLB path

For example:

```bash
python generate.py ~/Desktop/my-image.png --output ~/Desktop/my-model.glb
```

The script will:

1. Load the TRELLIS.2 model
2. Run image-to-3D generation using Apple MPS
3. Generate the 3D mesh
4. Post-process the mesh using O-Voxel
5. Export the result as a GLB

The generated file will be saved at the path provided with `--output`.

---

# 📦 Output

The result is a standard `.glb` file:

```text
my-model.glb
```

The GLB can be opened in applications such as Blender and exported into other formats, such as STL, for use in 3D-printing software such as Bambu Studio.

The generated model is not guaranteed to be immediately 3D-printable and may require additional mesh processing in Blender.

