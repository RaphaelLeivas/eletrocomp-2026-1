"""
Plota as funções de base MODAL (Koornwinder/Dubiner) e NODAL (tipo Lagrange)
no triângulo de referência, com os nós gerados pelo método warp&blend
(Warburton) usado no DGTD, para uma ordem N escolhida.

Uso:
    from plot_basis import plot_modal_and_nodal_basis
    plot_modal_and_nodal_basis(N=3)
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.tri import Triangulation
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401 (necessário p/ 3D)

from nodal_dg import warp_and_blend_nodes, Vandermonde2D, modes_ij


def _reference_triangle_mesh(n_per_side=40):
    """Malha fina (Delaunay) cobrindo o triângulo de referência
    com vértices (-1,-1), (1,-1), (-1,1)."""
    pts_r, pts_s = [], []
    for i in range(n_per_side + 1):
        for j in range(n_per_side + 1 - i):
            r = -1 + 2 * i / n_per_side
            s = -1 + 2 * j / n_per_side
            pts_r.append(r)
            pts_s.append(s)
    r = np.array(pts_r)
    s = np.array(pts_s)
    tri = Triangulation(r, s)
    return r, s, tri


def plot_modal_and_nodal_basis(N=3, n_per_side=60, cmap="RdBu_r", style="contour",
                                n_levels=20):
    """
    Gera duas figuras (matplotlib) com as Np = (N+1)(N+2)/2 funções
    de base modal e nodal do triângulo de referência, usando os nós
    warp&blend de ordem N.

    Parameters
    ----------
    N : int
        Ordem polinomial (grau máximo). Para N=3, Np = 10.
    n_per_side : int
        Resolução da malha fina usada para desenhar as funções.
    cmap : str
        Colormap usado.
    style : {"contour", "surface"}
        "contour" -> gráfico de contorno preenchido 2D (tricontourf).
        "surface" -> superfície 3D (plot_trisurf).
    n_levels : int
        Número de níveis de cor no gráfico de contorno.

    Returns
    -------
    (fig_modal, fig_nodal) : tupla de figuras matplotlib
    """
    Np = (N + 1) * (N + 2) // 2

    # 1) nós warp & blend no triângulo de referência
    rn, sn = warp_and_blend_nodes(N)

    # 2) matriz de Vandermonde nos nós -> define a base nodal
    V = Vandermonde2D(N, rn, sn)
    Vinv = np.linalg.inv(V)

    # 3) malha fina para desenhar as funções
    r_fine, s_fine, tri = _reference_triangle_mesh(n_per_side)
    V_fine = Vandermonde2D(N, r_fine, s_fine)      # phi_k(r,s) na malha fina
    L_fine = V_fine @ Vinv                          # l_m(r,s) = funções nodais

    ij_list = modes_ij(N)

    ncols = int(np.ceil(np.sqrt(Np)))
    nrows = int(np.ceil(Np / ncols))

    triangle_r = [-1, 1, -1, -1]
    triangle_s = [-1, -1, 1, -1]

    use_3d = (style == "surface")
    subplot_kw = {"projection": "3d"} if use_3d else {}

    # ---------- Figura 1: funções MODAIS ----------
    fig_modal = plt.figure(figsize=(3.2 * ncols, 3.0 * nrows))
    fig_modal.suptitle(f"Funções de base MODAL (Koornwinder/Dubiner) — N = {N}",
                        fontsize=14, y=1.02)
    for k in range(Np):
        ax = fig_modal.add_subplot(nrows, ncols, k + 1, **subplot_kw)
        phi_k = V_fine[:, k]
        i, j = ij_list[k]
        if use_3d:
            ax.plot_trisurf(tri.x, tri.y, phi_k, triangles=tri.triangles,
                             cmap=cmap, linewidth=0, antialiased=True)
            ax.set_zticks([])
            ax.view_init(elev=35, azim=-60)
        else:
            cs = ax.tricontourf(tri, phi_k, levels=n_levels, cmap=cmap)
            ax.tricontour(tri, phi_k, levels=n_levels, colors="k",
                           linewidths=0.3, alpha=0.5)
            ax.plot(triangle_r, triangle_s, "k-", lw=1.2)
            ax.plot(rn, sn, "o", color="k", ms=3)
            ax.set_aspect("equal")
            fig_modal.colorbar(cs, ax=ax, shrink=0.75, pad=0.02)
        ax.set_title(f"$\\phi_{{{i}{j}}}$", fontsize=10)
        ax.set_xticks([]); ax.set_yticks([])
    fig_modal.tight_layout()

    # ---------- Figura 2: funções NODAIS ----------
    fig_nodal = plt.figure(figsize=(3.2 * ncols, 3.0 * nrows))
    fig_nodal.suptitle(f"Funções de base NODAL (tipo Lagrange) — N = {N}\n"
                        "nós gerados por warp & blend (Warburton)",
                        fontsize=14, y=1.03)
    for m in range(Np):
        ax = fig_nodal.add_subplot(nrows, ncols, m + 1, **subplot_kw)
        l_m = L_fine[:, m]
        if use_3d:
            ax.plot_trisurf(tri.x, tri.y, l_m, triangles=tri.triangles,
                             cmap=cmap, linewidth=0, antialiased=True)
            # marca todos os nós no plano z=0 e destaca o nó "dono" da função
            ax.scatter(rn, sn, np.zeros_like(rn), color="k", s=8)
            ax.scatter([rn[m]], [sn[m]], [1.0], color="red", s=25)
            ax.set_zticks([])
            ax.view_init(elev=35, azim=-60)
        else:
            cs = ax.tricontourf(tri, l_m, levels=n_levels, cmap=cmap)
            ax.tricontour(tri, l_m, levels=n_levels, colors="k",
                           linewidths=0.3, alpha=0.5)
            ax.plot(triangle_r, triangle_s, "k-", lw=1.2)
            ax.plot(rn, sn, "o", color="k", ms=3)
            ax.plot([rn[m]], [sn[m]], "o", color="red", ms=6)
            ax.set_aspect("equal")
            fig_nodal.colorbar(cs, ax=ax, shrink=0.75, pad=0.02)
        ax.set_title(f"$\\ell_{{{m}}}$", fontsize=10)
        ax.set_xticks([]); ax.set_yticks([])
    fig_nodal.tight_layout()

    return fig_modal, fig_nodal


def plot_node_distribution(N=3, ax=None):
    """Plota apenas a distribuição de nós warp&blend no triângulo de referência."""
    rn, sn = warp_and_blend_nodes(N)
    if ax is None:
        fig, ax = plt.subplots(figsize=(5, 5))
    else:
        fig = ax.figure
    triangle_r = [-1, 1, -1, -1]
    triangle_s = [-1, -1, 1, -1]
    ax.plot(triangle_r, triangle_s, "k-", lw=1.5)
    ax.plot(rn, sn, "o", color="crimson", ms=8)
    for k, (x, y) in enumerate(zip(rn, sn)):
        ax.annotate(str(k), (x, y), textcoords="offset points",
                    xytext=(6, 6), fontsize=9)
    ax.set_aspect("equal")
    ax.set_title(f"Nós warp & blend — N = {N} ({len(rn)} pontos)")
    ax.set_xlabel("r"); ax.set_ylabel("s")
    return fig


if __name__ == "__main__":
    N = 3
    fig0 = plot_node_distribution(N)
    fig0.savefig("nodes.png", dpi=130, bbox_inches="tight")

    # gráficos de contorno 2D (padrão)
    fig_modal, fig_nodal = plot_modal_and_nodal_basis(N, style="contour")
    fig_modal.savefig("modal_basis_contour.png", dpi=130, bbox_inches="tight")
    fig_nodal.savefig("nodal_basis_contour.png", dpi=130, bbox_inches="tight")

    # opcional: também gera a versão em superfície 3D
    fig_modal_3d, fig_nodal_3d = plot_modal_and_nodal_basis(N, style="surface")
    fig_modal_3d.savefig("modal_basis_surface.png", dpi=130, bbox_inches="tight")
    fig_nodal_3d.savefig("nodal_basis_surface.png", dpi=130, bbox_inches="tight")

    print("Figuras salvas: nodes.png, modal_basis_contour.png, "
          "nodal_basis_contour.png, modal_basis_surface.png, nodal_basis_surface.png")
