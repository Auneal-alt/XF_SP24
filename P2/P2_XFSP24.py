import numpy as np

from Polymer import macroMolecule, Position


def simulate_molecules(N, num_molecules):
    molecules = [macroMolecule(targetDegreeOfPolymerization=N) for _ in range(num_molecules)]
    for molecule in molecules:
        molecule.freelyJointedChainModel()

    centers_of_mass = [m.centerOfMass for m in molecules]
    avg_center_of_mass = sum(centers_of_mass, Position()) / len(centers_of_mass)
    end_to_end_distances = [m.endToEndDistance for m in molecules]
    radii_of_gyration = [m.radiusOfGyration for m in molecules]

    avg_end_to_end = np.mean(end_to_end_distances)
    std_end_to_end = np.std(end_to_end_distances)
    avg_radius_of_gyration = np.mean(radii_of_gyration)
    std_radius_of_gyration = np.std(radii_of_gyration)
    pdi = np.var([m.N for m in molecules]) / np.mean([m.N for m in molecules])

    return avg_center_of_mass.getTup(), avg_end_to_end, std_end_to_end, avg_radius_of_gyration, std_radius_of_gyration, pdi


def main():
    N = int(input("degree of polymerization (1000)? ") or 1000)
    num_molecules = int(input("How many molecules (50)? ") or 50)

    results = simulate_molecules(N, num_molecules)
    center_of_mass, avg_end_to_end, std_end_to_end, avg_radius_of_gyration, std_radius_of_gyration, pdi = results

    print(f"Metrics for {num_molecules} molecules of degree of polymerization = {N}")
    print(f"Avg. Center of Mass (nm) = {center_of_mass[0]:.3f}, {center_of_mass[1]:.3f}, {center_of_mass[2]:.3f}")
    print(
        f"End-to-end distance (μm):\n\tAverage = {avg_end_to_end * 1e6:.3f}\n\tStd. Dev. = {std_end_to_end * 1e6:.3f}")
    print(
        f"Radius of gyration (μm):\n\tAverage = {avg_radius_of_gyration * 1e6:.3f}\n\tStd. Dev. = {std_radius_of_gyration * 1e6:.3f}")
    print(f"PDI = {pdi:.2f}")


if __name__ == "__main__":
    main()
