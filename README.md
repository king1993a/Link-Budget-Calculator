RF-Link-Budget-Calculator (系統鏈路預算自動化計算工具)<br>
這是一個基於 Python 開發的射頻系統級分析工具，旨在自動化計算接收機或發射機鏈路的關鍵性能指標。本工具透過數學建模方式，模擬訊號在經過多級射頻元件（如 LNA、混頻器、濾波器、功率放大器）時的增益、雜訊與線性度變化。<br>
核心功能 (Core Features)<br>
級聯指標計算：Friis 方程式：精確計算多級級聯雜訊指數 (Cascaded NF)。<br>
非線性分析：基於功率倒數和模型估算級聯三階截斷點 (OIP3/IIP3) 與 1-dB 壓縮點 (P1dB)。<br>
系統動態範圍評估 (SFDR)：結合雜訊基底 (Noise Floor) 與線性度指標，自動評估系統的無雜散動態範圍。<br>
電平圖分析 (Level Plan)：追蹤並輸出每一級元件輸出端的訊號強度分佈，協助找出鏈路中的性能瓶頸。<br>
模組化設計：可自由定義各級元件參數（Gain, NF, IP3, P1dB），支援 5G 毫米波等高頻系統前期評估。<br>
應用價值規格分解 (Spec Decomposition)：在 IC 設計前期，將系統級目標分配至各個子電路模組。<br>
性能瓶頸診斷：快速識別限制系統 NF 或線性度的關鍵元件。<br>
數學模型 (Mathematical Models)本工具實作了射頻工程中的核心級聯公式：<br>
<img width="560" height="119" alt="image" src="https://github.com/user-attachments/assets/e7e4cf7d-d577-4573-a808-1beecab43eab" />
# 使用範例 (Usage Example)<br>
chain = [<br>
    RFStage("LNA",      gain_db=15, nf_db=1.5, oip3_db=25,  op1db_dbm=12),<br>
    RFStage("Filter",   gain_db=-2, nf_db=2.0, oip3_db=100, op1db_dbm=40),<br>
    RFStage("Mixer",    gain_db=-6, nf_db=7.0, oip3_db=15,  op1db_dbm=5),<br>
    RFStage("IF_Amp",   gain_db=20, nf_db=4.0, oip3_db=30,  op1db_dbm=18)<br>
]<br>

# 執行分析 (設定頻寬為 1MHz)<br>
results = calculate_link(chain, bandwidth_hz=1e6)<br>


<img width="554" height="297" alt="image" src="https://github.com/user-attachments/assets/fc2ae8cf-a46f-47a0-b1ab-f4060032f6da" />
