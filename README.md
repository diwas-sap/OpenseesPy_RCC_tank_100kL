# 100 kL RCC Elevated Water Tank - Seismic Model in OpenSeesPy

A three-dimensional finite-element model of a **100,000-litre reinforced-concrete (RCC) elevated water tank** built in [OpenSeesPy](https://openseespydoc.readthedocs.io/). The model reproduces the frame staging, the tank container, and the sloshing water, and supports **gravity, modal, pushover, and nonlinear time-history (NLTHA)** analyses  with an optional **Lead-Rubber-Bearing (LRB) base-isolation** layer that can be toggled on or off.

The project is aimed at studying the seismic response of elevated tanks and quantifying the benefit of base isolation, using ground-motion sets that span near-field and far-field records.

---

## Highlights

- **3-D fiber-section model** (`ndm = 3`, `ndf = 6`) built entirely from explicit node/element definitions, so every member is traceable.
- **Housner two-mass water idealization** - impulsive and convective masses, with the convective (sloshing) mode captured by a spring + dashpot.
- **Optional base isolation** via the `LeadRubberX` element, switched with a single `LRB_inclusion` flag.
- **Full analysis pipeline** — gravity, eigenvalue (mode shapes and periods), monotonic pushover in X and Y, and batch nonlinear time-history analysis.
- **Automated result export** to CSV: base shear, overturning moment, inter-story drift, peak floor acceleration, and bearing displacement.

---

## Structural model at a glance

| Property | Value |
|---|---|
| Tank capacity | 100 kL (100,000 L) |
| Staging | RCC moment frame, 4 columns in plan (3.85 m × 3.85 m grid) |
| Levels | 8 elevations, base at Z = 0 to roof at Z = 25.0 m |
| Concrete | M25 (f′c = 25 MPa), `Concrete02` confined + unconfined fibers |
| Reinforcement | Fe500 (fy = 500 MPa), `Steel02` |
| Units | mm, s, N (mass in tonne = N·s²/mm) |
| Water masses | Impulsive ≈ 34.6 t, convective ≈ 61.3 t, empty tank ≈ 60.7 t |
| Isolation | Lead-Rubber Bearing (`LeadRubberX`), optional |

---

## Repository layout

| File | Purpose |
|---|---|
| `Dimensions_and_nodes.py` | Geometry, units, LRB dimensions, and all node coordinates |
| `Material.py` | Concrete, steel, and viscous/elastic material definitions |
| `Section.py` | Fiber sections for beams and columns |
| `Element.py` | Geometric transforms, beam integration, mass, and element assembly |
| `LRB_elements.py` | Lead-Rubber-Bearing properties and isolator elements |
| `mass_applied.py` | Gravity loads and nodal mass distribution |
| `Gravity_analysis.py` | Gravity solve + eigenvalue/mode-shape plotting |
| `model_bare.py` | Bare-frame model driver and eigenvalue check |
| `model_try_1.py` | Full assembled model (main model script) |
| `pushover.py` | Displacement-controlled pushover (X / Y) |
| `combined_pushover_try.py` | Combined/standalone pushover build |
| `NLTHA.py` | Nonlinear time-history analysis with CSV output |
| `Data/` | Sample analysis results (CSV) |
| `GM/` | Ground-motion records, grouped by set + target spectrum |
| `Result_comparsion.txt` | Reference periods, base shear, and drift results |

---

## Getting started

### Requirements

```bash
pip install openseespy opsvis numpy matplotlib
```

Tested with Python 3.9+.

### Running an analysis

Each script is self-contained and imports the shared model modules. From the repository root:

```bash
# Gravity + modal analysis (periods and mode shapes)
python Gravity_analysis.py

# Pushover analysis
python pushover.py

# Nonlinear time-history analysis (writes results to Data/)
python NLTHA.py
```

To enable or disable base isolation, set the flag near the top of `Dimensions_and_nodes.py`:

```python
LRB_inclusion = 1   # 1 = isolated model, 0 = fixed base
```

> **Note:** `NLTHA.py` writes output to a hard-coded `DATA_DIR` path. Update that path to a folder on your machine before running.

---

## Ground motions

The `GM/` directory holds acceleration records organized into near-field and far-field sets (plus scaled subsets `A`–`D`) with an accompanying target spectrum. Records are referenced by their RSN (Record Sequence Number). `GM/plot.py` plots individual records and set means against the target spectrum.

---

## Sample results

From `Result_comparsion.txt`, the fixed-base model gives a fundamental period near **3.9 s**, a maximum induced base shear around **280 kN**, and a peak roof displacement of roughly **400 mm** under the studied excitation — with maximum inter-story drift close to **1.9%**. See the file for the full period list and per-story drifts.

---

## Notes & possible improvements

- The ground-motion library is large (~150 MB committed). For a lighter clone, consider moving records to [Git LFS](https://git-lfs.com/) or an external release.
- Output paths in `NLTHA.py` are absolute — parameterizing them (e.g. via a config or CLI argument) would make the scripts portable across machines.

---

## Author

**Diwas** — [@diwas-sap](https://github.com/diwas-sap)

Structural / earthquake engineering research using OpenSeesPy.
