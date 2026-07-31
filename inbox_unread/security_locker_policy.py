import time
import math

class SecurityLockerPolicy:
    def __init__(self, locker_capacity: int = 128):
        self.rule_max_jitter_ms = 48.0
        self.manner_min_frame_ms = 16.6
        self.locker_capacity = locker_capacity
        self.locker_registry = [0] * locker_capacity

    def enforce_manner_and_rules(self, delta_time_ms: float, raw_jitter: float) -> bool:
        if delta_time_ms < self.manner_min_frame_ms:
            return False
        if raw_jitter > self.rule_max_jitter_ms:
            return False
        return True

    def store_conduction_state_in_locker(self, slot_id: int, dt: float, jitter: float, gwei: float):
        if not (0 <= slot_id < self.locker_capacity):
            return

        if not self.enforce_manner_and_rules(dt * 1000.0, jitter):
            self.locker_registry[slot_id] = 0x00000000
            return

        haptic_freq_hz = 100.0 + min(150.0, math.log1p(jitter) * 45.0)
        voltage_uv = min(120.0, (math.log1p(jitter) * 35.0) + (10.0 / (dt + 0.05)))
        gwei_factor = int(min(255.0, (gwei / 1.5)))

        packed_locker_val = (
            ((gwei_factor & 0xFF) << 24) |
            ((int(haptic_freq_hz) & 0xFFF) << 12) |
            (int(voltage_uv * 10) & 0xFFF)
        )

        self.locker_registry[slot_id] = packed_locker_val

    def read_locker_debug_value(self, slot_id: int) -> dict:
        raw_val = self.locker_registry[slot_id]
        if raw_val == 0:
            return {"status": "SILENT / LOCKED"}

        gwei_f = (raw_val >> 24) & 0xFF
        freq_hz = (raw_val >> 12) & 0xFFF
        voltage = (raw_val & 0xFFF) / 10.0

        return {
            "status": "UNLOCKED",
            "raw_hex": f"0x{raw_val:08X}",
            "conduction_freq_hz": f"{freq_hz} Hz",
            "voltage_uv": f"{voltage:.1f} uV",
            "gwei_factor": gwei_f
        }

if __name__ == "__main__":
    locker = SecurityLockerPolicy()
    print("=== SECURITY LOCKER & MANNER POLICY INITIALIZED ===")
    
    locker.store_conduction_state_in_locker(slot_id=0, dt=0.15, jitter=1.8, gwei=140.0)
    res = locker.read_locker_debug_value(0)
    print(f"[SLOT #0] {res['status']} -> Hex: {res['raw_hex']} | Freq: {res['conduction_freq_hz']} | Voltage: {res['voltage_uv']}")

    locker.store_conduction_state_in_locker(slot_id=1, dt=0.005, jitter=2.0, gwei=140.0)
    res_m = locker.read_locker_debug_value(1)
    print(f"[SLOT #1] {res_m['status']} (Manner Violation)")
