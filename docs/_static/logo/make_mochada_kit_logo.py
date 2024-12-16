"""Make the favicon, dark and light logos for mochada_kit docs."""

# ruff: noqa: D103

import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

# %% favicon function


def plot_favicon(ax):
    ax.set_xlim((0, 512))
    ax.set_ylim((0, 512))
    # ax.set_facecolor([0.784, 0.784, 0.784])
    ax.set_axis_off()
    # ax.add_artist(ax.patch)
    # ax.patch.set_zorder(-1)

    gg = "#646363"
    # gg = [0.784, 0.784, 0.784]
    ax.plot([256, 256], [312, 256], lw=2.0, color=gg)
    ax.plot([130, 130], [256, 200], lw=2.0, color=gg)
    ax.plot([382, 382], [256, 200], lw=2.0, color=gg)

    ax.plot([130, 382], [256, 256], lw=2.0, color=gg)

    rect_width = 220
    rect_height = 180
    cols = ["#B71E3F", "palegreen", "skyblue"]
    anchor_points = [(146, 312), (20, 20), (272, 20)]
    for i, j in enumerate(cols):
        r_p = FancyBboxPatch(
            anchor_points[i],
            rect_width,
            rect_height,
            "Round, rounding_size=50.0",
            facecolor=j,
            ec=gg,
            lw=1.0,
            zorder=20,
        )
        ax.add_patch(r_p)


# %% make favicon
fig, ax = plt.subplots(figsize=(512 / 300, 512 / 300), alpha=0.0, facecolor=None)
ax.set_position([0, 0, 1, 1])
plot_favicon(ax)

fig.savefig("mochada_kit_favicon.png", transparent=True)

# %% light logo

fig, ax = plt.subplots(figsize=(2048 / 300, 512 / 300), alpha=0.0)
ax.set_position([0, 0, 0.25, 1])
plot_favicon(ax)
fig.text(0.26, 0.35, "mochada_kit", {"size": 56, "color": "#646363"})
fig.savefig("mochada_kit_logo.png")

# %% dark logo

fig, ax = plt.subplots(figsize=(2048 / 300, 512 / 300), alpha=0.0, facecolor=None)
ax.set_position([0, 0, 0.25, 1])
plot_favicon(ax)
fig.text(0.26, 0.35, "mochada_kit", {"size": 56, "color": [0.784, 0.784, 0.784]})
fig.savefig("mochada_kit_logo_dark.png", transparent=True)
