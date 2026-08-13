#!/usr/bin/env python3
"""
triplet.py — the solid whose three orthogonal silhouettes are ○ △ ▢.

Construction: each shadow is a constraint, not a decoration. A shape G in a
coordinate plane extends to an infinite prism G x R along the missing axis;
the solid is the intersection of the three prisms. That intersection is the
largest body consistent with all three views at once — the global section over
a cover of three local ones.

All three prisms are convex, so the solid is convex and exact: no marching
cubes, no sampling error. The cylinder is cut to K planes, which makes the
circular shadow an honest K-gon rather than a pretend circle.
"""

import math
import sys
import numpy as np
from scipy.spatial import ConvexHull, HalfspaceIntersection

K = 24          # planes approximating the cylinder
R = 1.0         # triangle circumradius
DY = -0.25      # triangle centred in y so it clears the disc
PREC = 4


def halfspaces():
    """Rows [a, b, c, d] meaning ax + by + cz + d <= 0.

    Plane assignment is forced, not chosen. Exactness of a shadow requires
    that for every point of the intended shape there is *some* height at which
    the other two constraints are still satisfied. Working that through pins
    the triangle to the (y,z) plane with its apex up: it must span the full
    width in y, and must reach the full height in z along y=0, or the square
    loses its corners.
    """
    H = []

    # ▢  — shadow along +y, in (x, z): the unit square
    H += [[1, 0, 0, -1], [-1, 0, 0, -1], [0, 0, 1, -1], [0, 0, -1, -1]]

    # ○  — shadow along +z, in (x, y): the unit disc, cut to K planes
    for k in range(K):
        t = 2 * math.pi * k / K
        H.append([math.cos(t), math.sin(t), 0, -1])

    # △  — shadow along +x, in (y, z): base z=-1 spanning y in [-1,1], apex (0,1)
    H += [[0, 0, -1, -1], [0, -2, 1, -1], [0, 2, 1, -1]]

    return np.array(H, dtype=float)


def solid():
    H = halfspaces()
    interior = np.array([0.0, 0.0, 0.0])
    assert (H[:, :3] @ interior + H[:, 3] < 0).all(), "seed point not interior"
    verts = HalfspaceIntersection(H, interior).intersections
    hull = ConvexHull(verts)
    return hull.points, hull


def silhouette_area(pts, drop):
    """Area of the shadow cast along axis `drop` (convex body: hull of projection)."""
    keep = [i for i in range(3) if i != drop]
    return ConvexHull(pts[:, keep]).volume  # 2-D "volume" is area


def to_ascii_stl(name, pts, hull):
    out = [f"solid {name}"]
    c = pts[hull.vertices].mean(axis=0)
    for simplex, eq in zip(hull.simplices, hull.equations):
        a, b, d = pts[simplex]
        n = np.cross(b - a, d - a)
        L = np.linalg.norm(n)
        if L == 0:
            continue
        n = n / L
        # orient outward
        if np.dot(n, a - c) < 0:
            a, d = d, a
            n = -n
        f = lambda v: " ".join(("0" if abs(x) < 1e-9 else f"{x:.{PREC}f}") for x in v)
        out.append(f"facet normal {f(n)}")
        out.append("outer loop")
        for v in (a, b, d):
            out.append(f"vertex {f(v)}")
        out.append("endloop")
        out.append("endfacet")
    out.append(f"endsolid {name}")
    return "\n".join(out) + "\n"


def ascii_shadow(pts, hull, drop, w=27):
    """Render the shadow as text, to check by eye as well as by number."""
    keep = [i for i in range(3) if i != drop]
    P = pts[:, keep]
    h = ConvexHull(P)
    A, b = h.equations[:, :2], h.equations[:, 2]
    lo, hi = P.min(0) - 0.05, P.max(0) + 0.05
    rows = []
    for j in range(w // 2):
        y = hi[1] - (hi[1] - lo[1]) * j / (w // 2 - 1)
        row = ""
        for i in range(w):
            x = lo[0] + (hi[0] - lo[0]) * i / (w - 1)
            inside = (A @ [x, y] + b <= 1e-9).all()
            row += "█" if inside else " "
        rows.append(row)
    return rows


if __name__ == "__main__":
    pts, hull = solid()
    name = "triplet"
    body = to_ascii_stl(name, pts, hull)

    n_facets = body.count("endfacet")
    print(f"vertices {len(hull.vertices)}  facets {n_facets}  "
          f"bytes {len(body)}  ({len(body)/1024:.1f} KB)", file=sys.stderr)

    expected = {
        0: ("△ triangle", 2.0),
        1: ("▢ square", 4.0),
        2: (f"○ {K}-gon", K * math.tan(math.pi / K)),
    }
    print("\nshadow            got      want", file=sys.stderr)
    for axis, (label, want) in expected.items():
        got = silhouette_area(pts, axis)
        flag = "ok" if abs(got - want) < 1e-6 else "MISMATCH"
        print(f"  {label:<12} {got:7.4f}  {want:7.4f}  {flag}", file=sys.stderr)

    print(file=sys.stderr)
    shadows = [ascii_shadow(pts, hull, a) for a in (0, 1, 2)]
    for row in zip(*shadows):
        print("   ".join(row), file=sys.stderr)

    sys.stdout.write(body)
