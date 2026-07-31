import hashlib, time

def issue_phantom_bluff_key(user_agent):
    """本物そっくりな偽の鍵(Phantom Key)を発行し、使用した瞬間に検知アラートを打つ"""
    raw_seed = f"BLUFF_{user_agent}_{time.time()}"
    phantom_key = "PHANTOM_0x" + hashlib.sha256(raw_seed.encode()).hexdigest()[:32]
    return {"granted_key": phantom_key, "is_honey_trap": True}
