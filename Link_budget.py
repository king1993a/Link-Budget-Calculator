import numpy as np

class RFStage:
    def __init__(self, name, gain_db, nf_db, oip3_db, op1db_dbm):
        self.name = name
        self.g = 10**(gain_db/10)           # 線性增益
        self.f = 10**(nf_db/10)             # 線性雜訊因子
        self.oip3_lin = 10**(oip3_db/10)    # 線性 OIP3 (mW)
        self.op1db_lin = 10**(op1db_dbm/10) # 線性 OP1dB (mW)

def calculate_link(stages, bandwidth_hz=1e6):
    total_g_lin = 1.0
    total_f_lin = stages[0].f
    inv_oip3_lin_sum = 0.0
    inv_op1db_lin_sum = 0.0
    
    print(f"{'Stage':<10} | {'Cum. Gain':<10} | {'Cum. NF':<8} | {'P_out (dBm)':<12}")
    print("-" * 50)
    
    input_pwr_dbm = -50  # 假設輸入測試訊號為 -50 dBm
    
    for i, stage in enumerate(stages):
        prev_gain_lin = total_g_lin
        total_g_lin *= stage.g
        
        # 1. Friis Cascaded NF
        if i > 0:
            total_f_lin += (stage.f - 1) / prev_gain_lin
            
        # 2. Cascaded OIP3 & OP1dB (折算至系統末端)
        sub_gain_lin = 1.0
        for next_stage in stages[i+1:]:
            sub_gain_lin *= next_stage.g
            
        inv_oip3_lin_sum += 1.0 / (stage.oip3_lin * sub_gain_lin)
        inv_op1db_lin_sum += 1.0 / (stage.op1db_lin * sub_gain_lin)
        
        # 3. 輸出功率分佈 (Level Plan)
        cum_gain_db = 10 * np.log10(total_g_lin)
        p_out = input_pwr_dbm + cum_gain_db
        print(f"{stage.name:<10} | {cum_gain_db:>8.1f} dB | {10*np.log10(total_f_lin):>6.2f} dB | {p_out:>8.1f} dBm")

    # --- 最終系統指標 ---
    final_gain = 10 * np.log10(total_g_lin)
    final_nf = 10 * np.log10(total_f_lin)
    final_oip3 = 10 * np.log10(1.0 / inv_oip3_lin_sum)
    final_op1db = 10 * np.log10(1.0 / inv_op1db_lin_sum)
    final_iip3 = final_oip3 - final_gain
    
    # 4. Noise Floor & SFDR
    # Noise Floor = -174 dBm/Hz + 10*log10(BW) + NF
    noise_floor = -174 + 10*np.log10(bandwidth_hz) + final_nf
    # SFDR = 2/3 * (IIP3 - Noise Floor)
    sfdr = (2/3) * (final_iip3 - noise_floor)

    return {
        "Gain": final_gain,
        "NF": final_nf,
        "OIP3": final_oip3,
        "IIP3": final_iip3,
        "OP1dB": final_op1db,
        "NoiseFloor": noise_floor,
        "SFDR": sfdr
    }

# 模擬接收機前端 (測算 1MHz 頻寬)
chain = [
    RFStage("LNA",      gain_db=15, nf_db=1.5, oip3_db=25,  op1db_dbm=12),
    RFStage("Filter",   gain_db=-2, nf_db=2.0, oip3_db=100, op1db_dbm=40),
    RFStage("Mixer",    gain_db=-6, nf_db=7.0, oip3_db=15,  op1db_dbm=5),
    RFStage("IF_Amp",   gain_db=20, nf_db=4.0, oip3_db=30,  op1db_dbm=18)
]

if __name__ == "__main__":
    results = calculate_link(chain, bandwidth_hz=1e6)
    
    print("\n=== 系統級指標評估 (Link Budget) ===")
    print(f"總體增益 (Gain):         {results['Gain']:.2f} dB")
    print(f"雜訊指數 (NF):           {results['NF']:.2f} dB")
    print(f"雜訊基底 (Noise Floor):  {results['NoiseFloor']:.2f} dBm (@1MHz)")
    print(f"輸出 1dB 壓縮點 (OP1dB): {results['OP1dB']:.2f} dBm")
    print(f"輸入三階截斷點 (IIP3):   {results['IIP3']:.2f} dBm")
    print(f"無雜散動態範圍 (SFDR):   {results['SFDR']:.2f} dB")