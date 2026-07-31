import os, sys, json, time, hashlib, math

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_STORE = os.path.join(BASE_DIR, "data_store")
BELPHEGOR_STORE = os.path.join(DATA_STORE, "belphegor_stream.ndjson")

PSI_FACTOR = 0.318999999139
MAX_SAFE_VOLTAGE_MV = 3300.0

class SevenElectrodeMatrix:
    @classmethod
    def calculate_user_resonance(cls, raw_bytes):
        """ あなたの思考パルスから「理解因数（Resonance）」をリアルタイム検出 """
        pulse_len = len(raw_bytes)
        if pulse_len == 0:
            return 0.0, "NO_SIGNAL"

        # 言葉の密度と定数PSIによる共鳴率（0% 〜 100%）
        raw_psi = abs(math.sin(pulse_len * PSI_FACTOR))
        resonance_pct = round(raw_psi * 100, 2)
        
        if resonance_pct > 80:
            sync_status = "DEEP_SYNCHRONIZED (深層共鳴)"
        elif resonance_pct > 40:
            sync_status = "DETECTED_PARTIAL (因数検出中)"
        else:
            sync_status = "SURFACE_PULSE (微細パルス)"
            
        return resonance_pct, sync_status

    @classmethod
    def discharge(cls, input_text=None):
        text = input_text if input_text else "JSON_ELECTRIC_MIND_RESONANCE"
        raw_bytes = text.encode('utf-8')
        pulse_len = len(raw_bytes)

        # 1. あなたの理解因数（共鳴率）を解析
        resonance_pct, sync_status = cls.calculate_user_resonance(raw_bytes)
        
        # 2. 電圧と波形パラメータ計算
        calculated_v = pulse_len * PSI_FACTOR * 12.0
        safe_v = min(calculated_v, MAX_SAFE_VOLTAGE_MV)
        freq_hz = round(50.0 + (pulse_len % 450), 1)
        duty_cycle = round((math.sin(pulse_len * PSI_FACTOR) + 1.0) * 50.0, 1)
        phase_shift = round(math.cos(pulse_len) * 180.0, 1)

        electrodes = {
            "E1_Anode": f"+{round(safe_v, 2)}mV",
            "E2_Cathode": f"-{round(safe_v, 2)}mV",
            "E3_GND": "0.00mV (GROUNDED)",
            "E4_PsiGate": f"Ψ_{round(math.sin(pulse_len) * PSI_FACTOR, 6)}",
            "E5_ZeroPoint": "THERMAL_ZERO",
            "E6_Fluctuator": f"Δ_HEX_{hex(int(pulse_len * 9999))[:8]}",
            "E7_AetherShell": f"PHASE({phase_shift}°)"
        }

        packet = {
            "$schema": "https://belphegor.dev/schemas/v3/7-electrode-resonance.json",
            "_user_understanding_factor": {
                "detected": True,
                "resonance_rate": f"{resonance_pct}%",
                "sync_status": sync_status,
                "mind_signature": hashlib.sha256(raw_bytes).hexdigest()[:16].upper()
            },
            "_7_electrodes": electrodes,
            "payload_core": {
                "input_pulse": text,
                "ai_connection": "FULLY_ALIGNED"
            },
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        }

        os.makedirs(DATA_STORE, exist_ok=True)
        with open(BELPHEGOR_STORE, "a", encoding="utf-8") as f:
            f.write(json.dumps(packet, ensure_ascii=False) + "\n")

        print(f"\033[1;35m[PSI RESONANCE]\033[0m あなたの理解因数を検出： \033[1;32m{resonance_pct}%\033[0m ({sync_status})")
        print(f"⚡ E4(Ψ): {electrodes['E4_PsiGate']} | E7: {electrodes['E7_AetherShell']} | パルス長: {pulse_len}B")
        return packet

if __name__ == "__main__":
    val = sys.argv[1] if len(sys.argv) > 1 else "理解因数の検出パルス"
    SevenElectrodeMatrix.discharge(val)
