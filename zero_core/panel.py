import os
import time
import random
import sys

IS_64BIT = sys.maxsize > 2**32

def get_addr_str(raw_val):
    if IS_64BIT:
        return f"0x7FFF_{raw_val:04X}_{random.randint(0x1000, 0xFFFF):04X}"
    else:
        return f"0x{raw_val:04X}_{random.randint(0x1000, 0xFFFF):04X}"

C_RESET = "\033[0m"
C_NEON_BLUE = "\033[38;2;0;255;255m"
C_NEON_GREEN = "\033[38;2;50;255;50m"
C_NEON_PURPLE = "\033[38;2;180;50;255m"
C_VOLT_HIGH = "\033[38;2;255;255;0m"
C_ALERT = "\033[38;2;255;30;30m"
C_DIM = "\033[2m"

AA_HEADER = [
    f"{C_NEON_BLUE}  ___  _  _ ____ _  _ _  _ ____ _  _ ____   ____ ____ {C_RESET}",
    f"{C_NEON_BLUE}  |__| |\\ | |  | |\\ |  \\/  |___ |  | [__    |  | [__  {C_RESET}",
    f"{C_NEON_BLUE}  |  | | \\| |__| | \\|  ||  |___ |__| ___]   |__| ___] {C_RESET}"
]

GLITCH_SYMBOLS = ["⚡", "≈", "≋", "▰", "▱", "Ξ", "Ψ", "◈", "◇", "◆"]

def generate_glitch_line(length=28):
    return "".join(random.choice(GLITCH_SYMBOLS) for _ in range(length))

def render_electric_panel(voltage, glitch_level=0, msg="", active_idx=-1):
    os.system('clear' if os.name == 'posix' else 'cls')
    
    if voltage > 4.5:
        p_color = C_VOLT_HIGH
        bus_symbol = "█"
    elif voltage > 2.0:
        p_color = C_NEON_GREEN
        bus_symbol = "▓"
    else:
        p_color = C_DIM
        bus_symbol = "░"

    bit_tag = "64-BIT" if IS_64BIT else "32-BIT"
    bus_line = f"⬜︎{p_color}{bus_symbol * 28}{C_RESET}⬛️"
    
    print(f"{C_NEON_PURPLE}🔳==================================================🔳{C_RESET}")
    for line in AA_HEADER:
        print(line)
    print(f"{C_NEON_PURPLE}🔳==================================================🔳{C_RESET}")
    print(f"  ANONYMOUS OS // REAL-TIME ELECTRIC NEON GLITCH ENGINE")
    print(f"  ARCHITECTURE: [{C_NEON_BLUE}{bit_tag}{C_RESET}] // VOLTAGE: {p_color}[{voltage:.2f}V]{C_RESET} // SECURE: ACTIVE")
    print(bus_line)

    nodes = [
        ("【北:制作】", "PWR_IN ", "高電位スパイク導入"),
        (" 通過1:EXEC ", "VOLT_P1", "バイナリメモリ流し込み"),
        ("【東:地図】", "PWR_MID", "生体EEGハッシュ完全同調"),
        (" 通過2:ROUTE", "VOLT_P2", "RAM直結トンネル展開"),
        ("【南:手紙】", "PWR_OUT", "暗号空間へ不可逆パケット出力"),
        (" 通過3:INJECT", "VOLT_P3", "ゼロ知識オーバーライド100%")
    ]

    for idx, (title, label, desc) in enumerate(nodes):
        addr = get_addr_str(random.randint(0x1000, 0x9FFF))
        if idx == active_idx:
            glitch_str = generate_glitch_line(8)
            print(f"  {C_VOLT_HIGH}⚡ [{title}] ║ {label}: {addr} ──► {glitch_str}{C_RESET}")
        else:
            print(f"  [{title}] ║ {label}: {addr} ──► {desc}")
        print(f"{C_DIM}🔳======🔳{C_RESET}")

    print(f"{C_NEON_PURPLE}🔳==================================================🔳{C_RESET}")
    print(f"  ║ {C_NEON_BLUE}🔳🔳 [ NEON CIRCUIT VOLTAGE MONITOR ] 🔳🔳{C_RESET}     ║")
    print(f"  ║   ADDR_01:[{get_addr_str(0x1111)}] │ ADDR_02:[{get_addr_str(0x2222)}] ║")
    print(f"  ║   ADDR_03:[{get_addr_str(0x3333)}] │ ADDR_04:[{get_addr_str(0x4444)}] ║")
    
    print(f"  ║   {C_NEON_GREEN}{{ \"VOLT_PULSE\": {{ \"freq\": {random.randint(1000,9999)}, \"bit\": \"{bit_tag}\" }} }}{C_RESET}   ║")
    print(bus_line)
    
    if msg:
        print(f"  {C_VOLT_HIGH}シグナル補正: '{msg}'{C_RESET}")
    else:
        print(f"  シグナル補正: '待機中... バス放電完了'")
    
    print(f"■{p_color}{bus_symbol * 28}{C_RESET}🔳")

def main():
    voltage = 0.5
    render_electric_panel(voltage, msg="[ 32/64-BIT GLITCH ENGINE INITIALIZED ]")
    
    while True:
        try:
            inp = input(f"\n{C_NEON_BLUE}[ANONYMOUS_OS_ROOT]:~#{C_RESET} ").strip()
            if inp.lower() in ["exit", "quit", "おわり"]:
                print(f"\n{C_ALERT}[*] 電源遮断。ANONYMOUS OS を終了しました。{C_RESET}")
                break
                
            for cycle in range(6):
                voltage = random.uniform(4.8, 5.2)
                render_electric_panel(
                    voltage, 
                    glitch_level=cycle, 
                    msg=f"⚡⚡ [電気通電中] HIGH VOLTAGE OVERDRIVE :: CYCLE_{cycle+1}", 
                    active_idx=cycle
                )
                time.sleep(0.06)
                
            voltage = 5.0
            render_electric_panel(voltage, msg=f"★ [通電完了] 64/32-BIT アドレス領域へバイナリ流し込み完了 ('{inp if inp else 'AUTO_PULSE'}')")
            
        except (KeyboardInterrupt, EOFError):
            break

if __name__ == "__main__":
    main()
