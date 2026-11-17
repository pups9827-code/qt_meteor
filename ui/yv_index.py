def draw_uv_index(axes, dates, values):
    axes.plot(dates, values, marker="o", markersize=3, color="#73baff")
    axes.set_ylabel("", color="white", fontsize=8)
    axes.grid(True, alpha=0.15)
