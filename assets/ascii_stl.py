#!/usr/bin/env python3
"""
ascii_stl.py — emit compact ASCII STL for GitHub markdown ```stl blocks.

GitHub's stl fenced block takes ASCII STL only, inlined into the document.
That makes facet count a byte budget, not a fidelity choice. This generates
parametric tube-meshes at a chosen resolution so the budget is explicit.
"""

import math
import sys

PREC = 3  # decimal places; each digit dropped saves ~4% of file size


def _f(x):
    s = f"{x:.{PREC}f}"
    return "0" if s in ("-0.000", "0.000") else s


def facet(a, b, c, out):
    """One triangle, normal computed from winding."""
    ux, uy, uz = (b[i] - a[i] for i in range(3))
    vx, vy, vz = (c[i] - a[i] for i in range(3))
    nx, ny, nz = uy * vz - uz * vy, uz * vx - ux * vz, ux * vy - uy * vx
    L = math.sqrt(nx * nx + ny * ny + nz * nz) or 1.0
    out.append(f"facet normal {_f(nx/L)} {_f(ny/L)} {_f(nz/L)}")
    out.append("outer loop")
    for v in (a, b, c):
        out.append(f"vertex {_f(v[0])} {_f(v[1])} {_f(v[2])}")
    out.append("endloop")
    out.append("endfacet")


def tube(curve, radius, M, N, out):
    """
    Sweep a circular cross-section along a closed parametric curve.
    curve(t) -> (x,y,z) for t in [0,1). M segments along, N around.
    Frame is parallel-transported so the tube doesn't twist or flip.
    """
    pts = [curve(i / M) for i in range(M)]

    # tangents by central difference
    tangents = []
    for i in range(M):
        p, q = pts[(i - 1) % M], pts[(i + 1) % M]
        t = [q[j] - p[j] for j in range(3)]
        L = math.sqrt(sum(c * c for c in t)) or 1.0
        tangents.append([c / L for c in t])

    # seed a normal not parallel to the first tangent
    t0 = tangents[0]
    seed = [1, 0, 0] if abs(t0[0]) < 0.9 else [0, 1, 0]
    n = [seed[j] - t0[j] * sum(seed[k] * t0[k] for k in range(3)) for j in range(3)]
    L = math.sqrt(sum(c * c for c in n)) or 1.0
    n = [c / L for c in n]

    normals = []
    for i in range(M):
        t = tangents[i]
        # project previous normal onto the plane perpendicular to t
        d = sum(n[k] * t[k] for k in range(3))
        n = [n[j] - d * t[j] for j in range(3)]
        L = math.sqrt(sum(c * c for c in n)) or 1.0
        n = [c / L for c in n]
        normals.append(n)

    rings = []
    for i in range(M):
        t, nv = tangents[i], normals[i]
        bv = [t[1] * nv[2] - t[2] * nv[1],
              t[2] * nv[0] - t[0] * nv[2],
              t[0] * nv[1] - t[1] * nv[0]]
        ring = []
        for j in range(N):
            a = 2 * math.pi * j / N
            ca, sa = math.cos(a), math.sin(a)
            ring.append(tuple(pts[i][k] + radius * (ca * nv[k] + sa * bv[k])
                              for k in range(3)))
        rings.append(ring)

    for i in range(M):
        r0, r1 = rings[i], rings[(i + 1) % M]
        for j in range(N):
            k = (j + 1) % N
            facet(r0[j], r1[j], r1[k], out)
            facet(r0[j], r1[k], r0[k], out)


PHI = (1 + math.sqrt(5)) / 2


def borromean(M=26, N=6, radius=0.13, a=PHI, b=1.0):
    """Three mutually perpendicular golden ellipses — the classic Brunnian link."""
    out = []

    def mk(perm):
        def curve(t):
            u = 2 * math.pi * t
            v = (a * math.cos(u), b * math.sin(u), 0.0)
            return tuple(v[perm[i]] for i in range(3))
        return curve

    for perm in ((0, 1, 2), (2, 0, 1), (1, 2, 0)):
        tube(mk(perm), radius, M, N, out)
    return out


def trefoil(M=48, N=6, radius=0.28):
    def curve(t):
        u = 2 * math.pi * t
        return (math.sin(u) + 2 * math.sin(2 * u),
                math.cos(u) - 2 * math.cos(2 * u),
                -math.sin(3 * u))
    out = []
    tube(curve, radius, M, N, out)
    return out


def emit(name, facets):
    return "\n".join([f"solid {name}"] + facets + [f"endsolid {name}"]) + "\n"


if __name__ == "__main__":
    which = sys.argv[1] if len(sys.argv) > 1 else "borromean"
    kw = {}
    for arg in sys.argv[2:]:
        k, v = arg.split("=")
        kw[k] = int(v) if v.isdigit() else float(v)
    facets = {"borromean": borromean, "trefoil": trefoil}[which](**kw)
    body = emit(which, facets)
    sys.stdout.write(body)
    n = len(facets) // 7
    print(f"[{which}] {n} facets, {len(body)/1024:.1f} KB", file=sys.stderr)
