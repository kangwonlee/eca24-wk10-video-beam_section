import matplotlib.pyplot as plt
import exercise as beam


def sample_main():
    w0_m, h0_m = 50e-3, 12e-3
    w1_m, h1_m = 7.5e-3, 70e-3
    w2_m, h2_m = 90e-3, 10e-3

    area_m2 = beam.area(w0_m, h0_m, w1_m, h1_m, w2_m, h2_m)
    centroid_m = beam.centroid_y(w0_m, h0_m, w1_m, h1_m, w2_m, h2_m)
    moment_m4 = beam.moment_of_inertia(w0_m, h0_m, w1_m, h1_m, w2_m, h2_m)
    bending_stress_max_pa = beam.bending_stress(100, w0_m, h0_m, w1_m, h1_m, w2_m, h2_m)

    print(f'T-beam area: {area_m2:.6f} m^2')
    print(f'T-beam centroid: {centroid_m:.6f} m')
    print(f'T-beam moment of inertia: {moment_m4:.6f} m^4')
    print(f'T-beam max bending stress: {bending_stress_max_pa:.6f} Pa')

    a_above_below = beam.area_above_below_equal(w0_m, h0_m, w1_m, h1_m, w2_m, h2_m)

    print(f"Area above the centroid {a_above_below['a_above']:.6g} m^2")
    print(f"Area below the centroid {a_above_below['a_below']:.6g} m^2")
    print(f"Are these areas close? {a_above_below['close']}")

    q_above_below = beam.area_moment_above_below_equal(w0_m, h0_m, w1_m, h1_m, w2_m, h2_m)

    print(f"Area moment above the centroid {q_above_below['a_moment_above']:.6g} m^2")
    print(f"Area moment below the centroid {q_above_below['a_moment_below']:.6g} m^2")
    print(f"Are these area moments close? {q_above_below['close']}")

    ax = plt.gca()
    ax = plot_section(ax, centroid_m, w0_m, w1_m, w2_m, h0_m, h1_m, h2_m)

    plt.savefig('section.png')


def plot_section(ax, centroid_m, w0_m, w1_m, w2_m, h0_m, h1_m, h2_m):
    ax.fill_between(
        x=[(-0.5) * w0_m, (0.5) * w0_m],
        y1=[0, 0],
        y2=[h0_m, h0_m],
        color='blue', alpha=0.5)
    ax.fill_between(
        x=[(-0.5) * w1_m, (0.5) * w1_m],
        y1=[h0_m, h0_m],
        y2=[h1_m+h0_m, h1_m+h0_m],
        color='blue', alpha=0.5)
    ax.fill_between(
        x=[(-0.5) * w2_m, (0.5) * w2_m],
        y1=[h1_m+h0_m, h1_m+h0_m],
        y2=[h2_m+h1_m+h0_m, h2_m+h1_m+h0_m],
        color='blue', alpha=0.5)
    ax.axhline(y=centroid_m, color='red', linestyle='--')
    ax.grid(True)
    ax.axis('equal')


if __name__ == "__main__":
    sample_main()
