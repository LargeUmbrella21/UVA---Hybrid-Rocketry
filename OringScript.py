import matplotlib.pyplot as plt

def calculate_o_ring_params(ring_thickness, ring_ID, ring_OD, groove_depth=None, machine_gap=None, compression_range=(8, 35)):
    o_tank_ID = 3.25  # inches
    
    # --- Case 3: Both groove depth and machine gap are given ---
    if groove_depth is not None and machine_gap is not None:
        bulkhead_ID = o_tank_ID - (groove_depth * 2) - machine_gap
        stretch = (bulkhead_ID - ring_ID) / bulkhead_ID
        crossR = .5*stretch
        new_OD = (bulkhead_ID) + (ring_thickness * 2 * (1 - crossR))
        compression =  (((new_OD-o_tank_ID)) / (ring_thickness *(1 - crossR)* 2) * 100)
        return compression
    
    # --- Case 2: Groove depth given, but not machine gap ---
    elif groove_depth is not None:
        machine_gaps = [j * 0.001 for j in range(0, 101)]  # 0 to 0.1 inches
        compressions = []

        for machine_gap in machine_gaps:
            bulkhead_ID = o_tank_ID - (groove_depth * 2) - machine_gap
            stretch = (bulkhead_ID - ring_ID) / bulkhead_ID
            crossR = .5*stretch
            new_OD = (bulkhead_ID) + (ring_thickness * 2 * (1 - crossR))
            compression = 100 - (((ring_thickness*(1-crossR) * 2) - (new_OD - o_tank_ID)) / (ring_thickness *(1 - crossR)* 2) * 100)
            compressions.append(compression)

        plt.plot(machine_gaps, compressions, marker='o', linestyle='-')
        plt.xlabel("Machine Gap (inches)")
        plt.ylabel("Compression (%)")
        plt.title(f"Machine Gap vs Compression for Groove Depth {groove_depth:.3f} in")
        plt.grid(True)
        plt.show()
        return None

    # --- Case 1: No groove depth given (auto search valid combinations) ---
    else:
        valid_combinations = []
        for groove_depth in [i * 0.001 for i in range(1, int(ring_thickness * 1000))]:
            for machine_gap in [j * 0.001 for j in range(10, 101)]:  # 0.01 to 0.1 inches
                bulkhead_ID = o_tank_ID - (groove_depth * 2) - machine_gap
                stretch = (bulkhead_ID - ring_ID) / bulkhead_ID
                crossR = .5*stretch
                new_OD = (bulkhead_ID) + (ring_thickness * 2 * (1 - crossR))
                compression = 100 - (((ring_thickness*(1-crossR) * 2) - (new_OD - o_tank_ID)) / (ring_thickness *(1 - crossR)* 2) * 100)
                if compression_range[0] <= compression <= compression_range[1]:
                    valid_combinations.append((groove_depth, machine_gap, compression))
        return valid_combinations


# === Interactive Input ===
ring_thickness = float(input("Enter O-ring thickness (in inches): "))
ring_ID = float(input("Enter O-ring ID (in inches): "))
ring_OD = float(input("Enter O-ring OD (in inches): "))

groove_depth_input = input("Enter groove depth (or press Enter to auto-calculate valid combinations): ")
groove_depth = float(groove_depth_input) if groove_depth_input else None

machine_gap_input = None
if groove_depth is not None:
    machine_gap_input = input("Enter machine gap (or press Enter to plot vs gap): ")
    machine_gap = float(machine_gap_input) if machine_gap_input else None
else:
    machine_gap = None

# === Run Calculation ===
result = calculate_o_ring_params(ring_thickness, ring_ID, ring_OD, groove_depth, machine_gap)

# --- Output depending on case ---
if groove_depth is None:
    print("\nValid Groove Depth and Machine Gap Combinations for Desired Compression:")
    for combo in result:
        print(f"Groove Depth: {combo[0]:.4f} in, Machine Gap: {combo[1]:.4f} in, Compression: {combo[2]:.2f}%")
elif groove_depth is not None and machine_gap is not None:
    print(f"\nCompression at Groove Depth {groove_depth:.4f} in and Machine Gap {machine_gap:.4f} in: {result:.2f}%")
