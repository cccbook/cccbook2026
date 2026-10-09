from sympy import symbols, Interval, oo
from sympy.physics.quantum.hilbert import ComplexSpace, L2

def demonstrate_hilbert_space():
    print("=== 1. 有限維空間 (Qubit) ===")
    # 定義一個 2維空間 (C^2)
    h_qubit = ComplexSpace(2)
    print(f"空間: {h_qubit}")
    print(f"維度: {h_qubit.dimension}")
    
    print("\n=== 2. 多粒子系統 (Tensor Product) ===")
    # 定義三個 Qubit 的合成空間: C^2 ⊗ C^2 ⊗ C^2
    h_3_qubits = h_qubit * h_qubit * h_qubit
    print(f"合成空間: {h_3_qubits}")
    print(f"總維度: {h_3_qubits.dimension}") # 應該是 2*2*2 = 8

    print("\n=== 3. 無限維空間 (波函數) ===")
    # 定義 L2 空間
    h_wave = L2(Interval(-oo, oo))
    print(f"空間: {h_wave}")
    print(f"維度: {h_wave.dimension}")

    print("\n=== 4. 混合空間 ===")
    # 例如：一個自旋粒子在空間中移動 (Spin ⊗ Position)
    # C(2) ⊗ L2(-∞, ∞)
    h_mixed = h_qubit * h_wave
    print(f"混合空間: {h_mixed}")
    print(f"混合維度: {h_mixed.dimension}")

if __name__ == "__main__":
    demonstrate_hilbert_space()