import numpy as np
import matplotlib.pyplot as plt


def box_blur(arr: np.ndarray, r: int) -> np.ndarray:
    if r <= 0:
        return arr.astype(np.float32, copy=False)

    a = arr.astype(np.float32, copy=False)
    h, w = a.shape
    k = 2 * r + 1
    p = np.pad(a, ((r, r), (r, r)), mode="edge")

    s = np.zeros((p.shape[0] + 1, p.shape[1] + 1), dtype=np.float32)
    s[1:, 1:] = p.cumsum(axis=0).cumsum(axis=1)

    total = (
        s[k : k + h, k : k + w]
        - s[0 : h,     k : k + w]
        - s[k : k + h, 0 : w]
        + s[0 : h,     0 : w]
    )
    return total / (k * k)

def normalize01(x: np.ndarray, eps: float = 1e-8) -> np.ndarray:
    x = x.astype(np.float32, copy=False)
    mn = float(x.min())
    mx = float(x.max())
    return (x - mn) / (mx - mn + eps)

def _pick_radii(n: int, island_count: int, land_frac: float, rng: np.random.Generator):
    land_frac = float(np.clip(land_frac, 0.02, 0.85))
    area_per = (land_frac * (n * n)) / max(1, island_count)
    r_eq = np.sqrt(area_per / np.pi)

    r_min = max(3, int(round(r_eq * 0.55)))
    r_max = max(r_min + 1, int(round(r_eq * 1.35)))

    r_max = min(r_max, max(8, n // 6))
    r_min = min(r_min, max(6, r_max - 2))

    return r_min, r_max

def generate_islands(
    n: int,
    seed: int,
    island_count: int,
    land_frac: float = 0.18,       
    margin_frac: float = 0.08,     
    coast_noise: float = 0.06,      
    smooth_frac: float = 0.004,     
    profile_power: float = 2.2,     
    aspect_min: float = 0.70,
    aspect_max: float = 1.55,
    max_outer_retries: int = 8,    
) -> np.ndarray:
    rng = np.random.default_rng(seed)

    r_min0, r_max0 = _pick_radii(n, island_count, land_frac, rng)

    yy, xx = np.mgrid[0:n, 0:n].astype(np.float32)
    smooth_px0 = max(1, int(round(smooth_frac * n)))

    for outer in range(max_outer_retries):
        shrink = 0.90 ** outer
        r_min = max(2, int(round(r_min0 * shrink)))
        r_max = max(r_min + 1, int(round(r_max0 * shrink)))
        margin = max(1, int(round(margin_frac * r_max)))

        smooth_px = max(1, int(round(smooth_px0 * (0.9 ** outer))))

        cell = max(4, r_max + margin)
        grid = {} 

        centers = []

        def ok_place(cy, cx, eff):
            gy = cy // cell
            gx = cx // cell
            for yy_ in range(gy - 2, gy + 3):
                for xx_ in range(gx - 2, gx + 3):
                    lst = grid.get((yy_, xx_))
                    if not lst:
                        continue
                    for (py, px, peff, _, _) in lst:
                        if (cy - py) ** 2 + (cx - px) ** 2 < (eff + peff) ** 2:
                            return False
            return True
        tries = 0
        max_tries = 40000 + island_count * 1500

        edge_pad = r_max + margin + 2

        while len(centers) < island_count and tries < max_tries:
            tries += 1

            rad = int(rng.integers(r_min, r_max + 1))
            aspect = float(rng.uniform(aspect_min, aspect_max))
            a = float(rad)
            b = float(max(2, int(round(rad * aspect))))
            eff = float(max(a, b) + margin)

            if edge_pad >= n // 2:
                break

            cy = int(rng.integers(edge_pad, n - edge_pad))
            cx = int(rng.integers(edge_pad, n - edge_pad))

            if ok_place(cy, cx, eff):
                centers.append((cy, cx, rad, a, b))
                gy = cy // cell
                gx = cx // cell
                grid.setdefault((gy, gx), []).append((cy, cx, eff, a, b))

        if len(centers) < island_count:
            continue

        height = np.zeros((n, n), dtype=np.float32)

        for (cy, cx, rad, a, b) in centers:
            ang = float(rng.uniform(0.0, 2.0 * np.pi))
            ca = np.cos(ang)
            sa = np.sin(ang)

            dy = yy - cy
            dx = xx - cx
            xr =  ca * dx + sa * dy
            yr = -sa * dx + ca * dy

            d = np.sqrt((xr / a) ** 2 + (yr / b) ** 2)
            island = np.clip(1.0 - d, 0.0, 1.0) ** profile_power
            amp = float(rng.uniform(0.8, 1.15))
            island *= amp

            height = np.maximum(height, island.astype(np.float32, copy=False))

        if coast_noise > 0:
            noise = rng.random((n, n), dtype=np.float32)
            noise = box_blur(noise, max(1, smooth_px // 2))
            height = height + coast_noise * noise * (height > 0).astype(np.float32)

        height = box_blur(height, smooth_px)

        land = height > 1e-4
        out = np.zeros((n, n), dtype=np.uint8)
        if np.any(land):
            lh = normalize01(height[land])
            out[land] = (np.floor((lh ** 1.15) * 9.0).astype(np.int32) + 1).clip(1, 9).astype(np.uint8)

        return out

    raise ValueError(
        f"Не вдалося згенерувати {island_count} островів на n={n} "
    )


grids = [
    generate_islands(256, seed=1, island_count=5),
    generate_islands(256, seed=2, island_count=5),
    generate_islands(256, seed=3, island_count=5)
]

plt.figure(figsize=(12,4))

for i, g in enumerate(grids):
    plt.subplot(1, 3, i+1)
    plt.imshow(g, cmap="terrain")
    plt.title(f"Map {i}")

plt.show()