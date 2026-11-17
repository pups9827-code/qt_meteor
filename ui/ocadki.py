def draw_precipitation(axes, dates, values):
    axes.bar(dates, values, color="#73baff")
    axes.set_ylabel("мм", color="white", fontsize=8)
    axes.grid(True, alpha=0.15)
