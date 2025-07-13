# Phong Ray Tracer in Python

## Overview  
This project is a simple yet complete ray tracer implemented in Python. It supports:
- Vector and matrix math for 3D geometry  
- Ray–sphere and ray–plane intersections (including “inverted” background spheres)  
- Phong shading (ambient, diffuse, shadows)  
- Directional, point, and ambient lights with attenuation  
- Automatic camera framing and FOV adjustment based on scene content  
- Text-based scene description parser  
- Image output via Pillow (PNG)

## Why Use It?  
- **Educational**  
  Understand the fundamentals of ray tracing: rays, intersections, shading, shadows.  
- **Modular**  
  Clear separation of concerns: Vector, Ray, Object, Light, Scene, Camera, Screen, Parser.  
- **Extensible**  
  Easily add reflections, refractions, new primitives, acceleration structures.  
- **Configurable**  
  Define scenes in plain-text files; experiment with camera, materials, and lighting.  
- **Self-Contained**  
  Minimal dependencies: only `numpy` (optional for some math) and `Pillow` for image saving.

## Features  
- Single-bounce Phong shading with soft shadows  
- Support for infinite planes and finite spheres (positive or negative radius)  
- Conservative defaults and heuristics in the parser for robust scene setup  
- Automatic camera repositioning and adaptive FOV for good framing  
- Lightweight—ideal for demonstration or as a teaching tool

---

# Python Environment Setup

## 1. Create & Activate a Virtual Environment  
```bash
# Create a new virtual environment
python -m venv myenv

# Windows (cmd.exe)
myenv\Scripts\activate

# Windows (PowerShell)
myenv\Scripts\Activate.ps1

# macOS/Linux
source myenv/bin/activate
```

## 2. Install Dependencies  
```bash
pip install numpy pillow
# or, if you already have requirements.txt:
pip install -r requirements.txt
```

## 3. Freeze Requirements  
After installing additional packages, lock them in:
```bash
pip freeze > requirements.txt
```

## 4. Deactivate the Environment  
```bash
deactivate
```

---

# Usage

1. Prepare your scene description file, e.g. `scene1.txt`.  
2. Run the renderer:
   ```bash
   python main.py scene1.txt
   ```
3. The rendered image will be saved as `render_scene1_fixed.png`.

---

# Example Scene

Below is a complete minimal scene file named `example_scene.txt`. Copy these lines into that file:

```text
e 0.0 0.0 4.0 1.0        # Camera at (0,0,4), w=1.0 (unused)
a 0.1 0.2 0.3 1.0        # Ambient light RGB(0.1,0.2,0.3), ka=1.0
o 0.0 -0.5 -1.0 -3.5     # Plane with normal (0,-0.5,-1), d=3.5
o -0.7 0.7 -2.0 0.5      # Sphere at (-0.7,0.7,-2), r=0.5
o 0.6 0.5 -1.0 0.5       # Sphere at (0.6,0.5,-1), r=0.5
c 0.0 1.0 1.0 10.0       # Color for first object: cyan, shininess=10
c 1.0 0.0 0.0 10.0       # Color for second object: red, shininess=10
c 0.6 0.0 0.8 10.0       # Color for third object: purple, shininess=10
d 0.5 0.0 -1.0 1.0       # Directional light from (0.5,0,-1), intensity multiplier=1
d 0.0 0.5 -1.0 0.0       # Directional light from (0,0.5,-1), intensity multiplier=0
p 2.0 1.0 3.0 0.6        # Point light at (2,1,3), attenuation/flag=0.6
i 0.2 0.5 0.7 1.0        # Light intensity entries
i 0.7 0.5 0.0 1.0
```

Render it by running:

```bash
python main.py example_scene.txt
```

You should see output like:

```
Loading scene file: example_scene.txt

=== FINAL RENDER SETTINGS ===
Camera Position: Vector3D(0.000, 0.000, 4.000)
Look Direction : Vector3D(0.000, 0.000, -1.000)
Field of View  : 60.0
Resolution     : 800x800
Background     : Vector3D(0.100, 0.100, 0.200)
Total Objects  : 3
Total Lights   : 3
==============================

Starting render of 640000 pixels...
Rendering row 0/800
...
[Unified] 123456/640000 meaningful pixels (19.29%)
Image saved as: render_example_scene_fixed.png
```

The resulting image `render_example_scene_fixed.png` will show two colored spheres hovering above a plane under ambient and directional/point lights.

---

# Project Structure

```
.
├── main.py
├── Models
│   ├── Vector3D.py
│   ├── Screen.py
│   ├── Camera.py
│   ├── Scene.py
│   ├── Material.py
│   └── Objects
│       ├── Object.py
│       ├── Sphere.py
│       ├── Plane.py
│       └── Ray.py
├── Handler
│   └── ScreenHandler.py
├── Service
│   ├── Parser.py
│   ├── RayCaster.py
│   └── ParserServices.py
├── requirements.txt
└── README.md
```

---

# Contributing  
Feel free to submit pull requests for:  
- Recursive reflections/refractions  
- Spatial acceleration (BVH, grids)  
- Anti-aliasing or tone mapping  
- New primitives (triangles, meshes)  

---

# License  
This project is released under the MIT License.