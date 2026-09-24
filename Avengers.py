# ╔════════════════════════════════════╗
# ║       Avengers Checker/Cleaner     ║
# ╚════════════════════════════════════╝

import os
import sys
import time
import shutil
import subprocess
import importlib.util
import platform
import traceback
from pathlib import Path


# ═══════════════════════════════════
#          si / sp
# ═══════════════════════════════════

def si(prompt=""):
    """Safe input wrapper."""
    try:
        return input(prompt)
    except (EOFError, KeyboardInterrupt):
        print()
        raise


def sp(*objects, sep=" ", end="\n", file=None, flush=False):
    """Full-compatible print wrapper."""
    return print(*objects, sep=sep, end=end, file=file, flush=flush)


# ═══════════════════════════════════
#        SYSTEM SELECTOR
# ═══════════════════════════════════

def choose_system():
    while True:
        sp("\nSelect Platform:")
        sp("1. Windows")
        sp("2. Linux")
        sp("3. Termux")

        try:
            choice = si("System : ").strip().lower()
        except (EOFError, KeyboardInterrupt):
            sp("\nExiting...")
            raise SystemExit(130)

        if choice in ("1", "windows", "win"):
            return "windows"
        elif choice in ("2", "linux", "gnu/linux"):
            return "linux"
        elif choice in ("3", "termux", "android"):
            return "termux"

        sp("\n❌ Invalid System")

# This is intentionally selected before any platform-specific work.
SYSTEM = choose_system()
IS_WINDOWS = SYSTEM == "windows"
IS_LINUX = SYSTEM == "linux"
IS_TERMUX = SYSTEM == "termux"

BASE_DIR = Path(__file__).resolve().parent

# Sync the selection with every child process launched by this program.
os.environ["AVENGERS_OS"] = SYSTEM
os.environ["AVENGERS_ROOT"] = str(BASE_DIR)
os.environ["AVENGERS_PYTHON"] = sys.executable or "python"


# ═══════════════════════════════════
#         TERMINAL ENCODING
# ═══════════════════════════════════

def configure_terminal():
    # Python 3.7+ supports reconfigure on standard streams.
    for stream in (sys.stdout, sys.stderr):
        try:
            if hasattr(stream, "reconfigure"):
                stream.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass


configure_terminal()


# ═══════════════════════════════════
#          PATH / COMMANDS
# ═══════════════════════════════════

def get_path(relative_path):
    """Resolve all project paths relative to this launcher."""
    return BASE_DIR.joinpath(*Path(relative_path).parts).resolve()


def which(command):
    """Safe shutil.which wrapper."""
    try:
        return shutil.which(command)
    except Exception:
        return None


def command_exists(command):
    return which(command) is not None


# ═══════════════════════════════════
#       REAL HOST CONSISTENCY
# ═══════════════════════════════════

def detected_host():
    """Detect Windows, Linux, Android/Termux correctly."""

    system = platform.system().strip().lower()

    # Windows
    if system == "windows":
        return "windows"

    # Android / Termux
    if system in ("android", "linux"):
        if (
            os.environ.get("TERMUX_VERSION")
            or "com.termux" in os.environ.get("PREFIX", "")
            or "com.termux" in sys.prefix
            or "com.termux" in sys.executable
            or os.path.isdir("/data/data/com.termux")
        ):
            return "termux"

        # Android environment detected by getprop
        getprop = shutil.which("getprop")

        if getprop:
            try:
                result = subprocess.run(
                    [getprop, "ro.build.version.release"],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.DEVNULL,
                    text=True,
                    timeout=2,
                    check=False,
                )

                if result.returncode == 0 and result.stdout.strip():
                    return "termux"

            except Exception:
                pass

        return "linux"

    return system or "unknown"


def host_matches_selection():
    actual = detected_host()

    if IS_WINDOWS:
        return actual == "windows"

    if IS_LINUX:
        return actual == "linux"

    if IS_TERMUX:
        # Termux may be reported as Android/Linux by the host.
        return actual in ("termux", "android")

    return False


DETECTED_SYSTEM = detected_host()

if not host_matches_selection():
    sp("\n⚠️ Platform mismatch.")
    sp(f"Selected : {SYSTEM}")
    sp(f"Detected : {DETECTED_SYSTEM}")
    sp("Please restart and select the current platform.")
    raise SystemExit(2)

# ═══════════════════════════════════
#          SCREEN CLEAR
# ═══════════════════════════════════

def clear_screen():
    try:
        if IS_WINDOWS:
            subprocess.run(
                ["cmd", "/c", "cls"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                check=False,
            )
            return

        clear_bin = which("clear")
        if clear_bin:
            subprocess.run(
                [clear_bin],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                check=False,
            )
            return
    except Exception:
        pass

    # ANSI fallback
    try:
        sp("\033[2J\033[H", end="")
    except Exception:
        pass


# ═══════════════════════════════════
#          PROCESS ENGINE
# ═══════════════════════════════════

def run_process(args, *, cwd=None, capture=False, timeout=None, env=None):
    """Centralized subprocess handling."""
    try:
        return subprocess.run(
            args,
            cwd=str(cwd) if cwd else None,
            capture_output=capture,
            text=True,
            timeout=timeout,
            env=env,
            check=False,
        )
    except subprocess.TimeoutExpired:
        return None
    except (FileNotFoundError, PermissionError, OSError):
        return None
    except Exception:
        return None


def child_environment():
    """Environment shared with Avengers child scripts."""
    env = os.environ.copy()
    env["AVENGERS_OS"] = SYSTEM
    env["AVENGERS_ROOT"] = str(BASE_DIR)
    env["AVENGERS_PYTHON"] = PYTHON

    # Make project-root imports work for child Python scripts.
    old_pythonpath = env.get("PYTHONPATH", "")
    env["PYTHONPATH"] = (
        str(BASE_DIR)
        if not old_pythonpath
        else str(BASE_DIR) + os.pathsep + old_pythonpath
    )
    return env


# ═══════════════════════════════════
#          PYTHON RESOLUTION
# ═══════════════════════════════════

def get_python():
    # Current interpreter is the most reliable choice.
    current = sys.executable
    if current and Path(current).exists():
        return current

    if IS_WINDOWS:
        return which("python") or which("py") or "python"

    return which("python3") or which("python") or "python"


PYTHON = get_python()


# ═══════════════════════════════════
#          CHILD RUNNERS
# ═══════════════════════════════════

def run_python(relative_path):
    path = get_path(relative_path)

    if not path.is_file():
        sp(f"\nERROR: File not found: {relative_path}")
        return 1

    result = run_process(
        [PYTHON, str(path)],
        # IMPORTANT: child programs start from project root,
        # not from their own subfolder.
        cwd=BASE_DIR,
        env=child_environment(),
    )

    if result is None:
        sp(f"\nERROR: Could not start Python: {relative_path}")
        return 1

    return result.returncode


def run_bash(relative_path):
    path = get_path(relative_path)

    if not path.is_file():
        sp(f"\nERROR: File not found: {relative_path}")
        return 1

    bash = which("bash")

    if IS_WINDOWS and not bash:
        sp("\nERROR: Bash is not installed or not in PATH.")
        sp("Install Git Bash/WSL or run this module on Linux/Termux.")
        return 1
    if not bash:
        sp("\nERROR: Bash is not installed or not in PATH.")
        return 1

    result = run_process(
        [bash, str(path)],
        cwd=BASE_DIR,
        env=child_environment(),
    )

    if result is None:
        sp(f"\nERROR: Could not start Bash: {relative_path}")
        return 1

    return result.returncode


def run_go(relative_path):
    path = get_path(relative_path)

    if not path.is_file():
        sp(f"\nERROR: File not found: {relative_path}")
        return 1

    go = which("go")
    if not go:
        sp("\nERROR: Go is not installed or not in PATH.")
        return 1

    result = run_process(
        [go, "run", str(path)],
        cwd=BASE_DIR,
        env=child_environment(),
    )

    if result is None:
        sp("\nERROR: Could not start Go.")
        return 1

    return result.returncode


# ═══════════════════════════════════
#             URL ENGINE
# ═══════════════════════════════════

def open_url(url):
    """Use only the opener appropriate to the selected platform."""
    try:
        if IS_TERMUX:
            opener = which("termux-open-url")
            if opener:
                result = run_process([opener, url])
                return result.returncode if result else 1

            # Android fallback if termux-open-url is unavailable.
            am = which("am")
            if am:
                result = run_process(
                    [
                        am,
                        "start",
                        "-a",
                        "android.intent.action.VIEW",
                        "-d",
                        url,
                    ]
                )
                return result.returncode if result else 1

            sp("\nERROR: termux-open-url not found.")
            return 1

        if IS_WINDOWS:
            os.startfile(url)  # type: ignore[attr-defined]
            return 0

        if IS_LINUX:
            for opener in ("xdg-open", "gio", "wslview"):
                binary = which(opener)
                if not binary:
                    continue

                if opener in ("xdg-open", "wslview"):
                    args = [binary, url]
                else:
                    args = [binary, "open", url]
                result = run_process(args)
                return result.returncode if result else 1

            sp("\nERROR: xdg-open/gio not found.")
            return 1

    except Exception as exc:
        sp(f"\nERROR: Could not open URL: {exc}")
        return 1

    return 1


# ═══════════════════════════════════
#          PACKAGE MANAGEMENT
# ═══════════════════════════════════

def package_installed(module_name):
    try:
        return importlib.util.find_spec(module_name) is not None
    except (ImportError, AttributeError, ValueError):
        return False
    except Exception:
        return False


def install_python_package(package):
    # Use the exact interpreter running this launcher.
    commands = [
        [PYTHON, "-m", "pip", "install", package]
    ]

    # User install is useful on normal Linux without root.
    if IS_LINUX:
        commands.append(
            [PYTHON, "-m", "pip", "install", "--user", package]
        )

    for command in commands:
        # Capture pip internals so broken network/cache conditions do not
        # flood the Avengers UI with unrelated warnings.
        result = run_process(command, capture=True)
        if result and result.returncode == 0:
            return True

    return False


def check_colorama():
    package = "colorama"
    sp(f"\n🔍 Checking 🕵️ {package}")

    if package_installed(package):
        sp("Founded ✅")
        return True

    sp("Not Found ⛔")
    sp(f"Installing 📦 {package}...")

    if install_python_package(package):
        sp("Installed ✅")
        return True

    sp("Install Failed ❌")
    sp(f"Run manually: {PYTHON} -m pip install {package}")
    return False


# ═══════════════════════════════════
#          COLORAMA / FALLBACK
# ═══════════════════════════════════

COLORAMA_OK = check_colorama()

try:
    import colorama
    from colorama import Fore, Style

    try:
        colorama.just_fix_windows_console()
    except Exception:
        pass

    colorama.init()

except ImportError:
    # The program can still run without colors.
    class _Fore:
        RED = GREEN = YELLOW = RESET = ""
        BLUE = CYAN = MAGENTA = WHITE = BLACK = ""

    class _Style:
        RESET_ALL = ""

    Fore = _Fore()
    Style = _Style()


# ═══════════════════════════════════
#          TERMUX TOOLS
# ═══════════════════════════════════

def termux_pkg_install(package):
    if not IS_TERMUX:
        return False

    pkg = which("pkg")
    if not pkg:
        return False

    result = run_process(
        [pkg, "install", "-y", package]
    )
    return bool(result and result.returncode == 0)


def prepare_termux_tools():
    if not IS_TERMUX:
        return

    # These packages are Termux-only.
    if not which("mpv"):
        sp("\n🔍 Checking 🕵️ mpv...")
        termux_pkg_install("mpv")

    if not which("go"):
        sp("\n🔍 Checking 🕵️ Go...")
        termux_pkg_install("golang")


prepare_termux_tools()


# ═══════════════════════════════════
#          SHIZUKU CHECKER
# ═══════════════════════════════════

sp("\n🔍 Checking 🕵️ Shizuku...")

if IS_TERMUX and which("rish"):
    result = run_process(
        ["rish", "-c", "echo OK"],
        capture=True,
        timeout=3,
    )

    if (
        result
        and result.returncode == 0
        and "OK" in (result.stdout or "")
    ):
        sp("Shizuku Running ✅")
    else:
        sp("Shizuku Not Running ⛔")
else:
    sp("Shizuku Not Running ⛔")


# ═══════════════════════════════════
#          DEVICE FUNCTIONS
# ═══════════════════════════════════

def getprop(name):
    if not IS_TERMUX:
        return ""

    getprop_bin = which("getprop") or "getprop"
    result = run_process(
        [getprop_bin, name],
        capture=True,
        timeout=2,
    )

    if not result:
        return ""

    return (result.stdout or "").strip()


def get_android_version():
    return getprop("ro.build.version.release") or "N/A"


def get_total_ram_mb():
    if IS_WINDOWS:
        try:
            import ctypes

            class MEMORYSTATUSEX(ctypes.Structure):
                _fields_ = [
                    ("dwLength", ctypes.c_ulong),
                    ("dwMemoryLoad", ctypes.c_ulong),
                    ("ullTotalPhys", ctypes.c_ulonglong),
                    ("ullAvailPhys", ctypes.c_ulonglong),
                    ("ullTotalPageFile", ctypes.c_ulonglong),
                    ("ullAvailPageFile", ctypes.c_ulonglong),
                    ("ullTotalVirtual", ctypes.c_ulonglong),
                    ("ullAvailVirtual", ctypes.c_ulonglong),
                    ("ullAvailExtendedVirtual", ctypes.c_ulonglong),
                ]

            memory = MEMORYSTATUSEX()
            memory.dwLength = ctypes.sizeof(memory)

            ok = ctypes.windll.kernel32.GlobalMemoryStatusEx(
                ctypes.byref(memory)
            )

            if ok:
                return int(memory.ullTotalPhys // (1024 ** 2))
        except Exception:
            return 0

    try:
        with open("/proc/meminfo", "r", encoding="utf-8") as file:
            for line in file:
                if line.startswith("MemTotal:"):
                    parts = line.split()
                    if len(parts) >= 2 and parts[1].isdigit():
                        return int(parts[1]) // 1024
                    break
    except Exception:
        pass

    return 0


def get_disk_total_gb():
    try:
        usage = shutil.disk_usage(BASE_DIR)
        return usage.total / (1024 ** 3)
    except Exception:
        return 0.0


def read_linux_frequency():
    candidates = [
        "/sys/devices/system/cpu/cpu0/cpufreq/cpuinfo_max_freq",
        "/sys/devices/system/cpu/cpu0/cpufreq/scaling_max_freq",
    ]

    for candidate in candidates:
        try:
            raw = Path(candidate).read_text(encoding="utf-8").strip()
            if raw.isdigit():
                return float(raw) / 1000.0
        except Exception:
            continue

    return 0.0


def get_cpu_mhz():
    if IS_TERMUX or IS_LINUX:
        max_mhz = read_linux_frequency()
        if max_mhz:
            return max_mhz

        # Last Linux fallback: first reported CPU frequency.
        try:
            text = Path("/proc/cpuinfo").read_text(
                encoding="utf-8",
                errors="ignore"
            )
            for line in text.splitlines():
                if line.lower().startswith("cpu mhz") and ":" in line:
                    raw = line.split(":", 1)[1].strip()
                    try:
                        return float(raw)
                    except ValueError:
                        pass
        except Exception:
            pass

    if IS_WINDOWS:
        try:
            import winreg
            key_path = r"HARDWARE\DESCRIPTION\System\CentralProcessor\0"
            with winreg.OpenKey(
                winreg.HKEY_LOCAL_MACHINE,
                key_path
            ) as key:
                value, _ = winreg.QueryValueEx(key, "~MHz")
                return float(value)
        except Exception:
            pass

        # Modern Windows PowerShell fallback.
        powershell = which("powershell") or which("pwsh")
        if powershell:
            result = run_process(
                [
                    powershell,
                    "-NoProfile",
                    "-Command",
                    "(Get-CimInstance Win32_Processor | Select-Object -First 1).MaxClockSpeed",
                ],
                capture=True,
                timeout=5,
            )
            if result:
                raw = (result.stdout or "").strip()
                try:
                    return float(raw)
                except ValueError:
                    pass

    return 0.0


def get_cpu_name():
    if IS_TERMUX:
        return (
            getprop("ro.product.cpu.abi")
            or getprop("ro.product.cpu.abilist")
            or platform.machine()
            or "Unknown"
        )

    if IS_WINDOWS:
        try:
            import winreg
            with winreg.OpenKey(
                winreg.HKEY_LOCAL_MACHINE,
                r"HARDWARE\DESCRIPTION\System\CentralProcessor\0"
            ) as key:
                value, _ = winreg.QueryValueEx(key, "ProcessorNameString")
                return str(value).strip() or platform.machine() or "Unknown"
        except Exception:
            pass

    return platform.processor() or platform.machine() or "Unknown"


def get_gpu():
    if IS_TERMUX:
        return (
            getprop("ro.hardware.egl")
            or getprop("ro.hardware")
            or "Unknown"
        )

    # Portable GPU discovery without extra dependencies is limited.
    return "Unknown"


def get_root_status():
    if not IS_TERMUX:
        return False

    # Actual UID check is more meaningful than mere existence of su.
    id_bin = which("id")
    if id_bin:
        result = run_process(
            [id_bin, "-u"],
            capture=True,
            timeout=2,
        )
        if result and result.returncode == 0:
            return (result.stdout or "").strip() == "0"

    # Fallback: a callable su executable is only evidence that su exists,
    # not proof of root, so we leave it false here.
    return False


android = get_android_version()
ram_mb = get_total_ram_mb()
ram_gb = ram_mb / 1024 if ram_mb else 0.0
rom_gb = get_disk_total_gb()
cpu = get_cpu_name()
cpu_mhz = get_cpu_mhz()
gpu = get_gpu()
root = get_root_status()


# ═══════════════════════════════════
#          PHONE RATE
# ═══════════════════════════════════

rate = 100

if android.isdigit() and int(android) <= 7:
    rate -= 25

if root:
    rate -= 5

if ram_mb and ram_mb <= 512:
    rate -= 35
elif ram_mb and ram_mb <= 1024:
    rate -= 20
elif ram_mb and ram_mb <= 2048:
    rate -= 10

if rom_gb and rom_gb <= 4:
    rate -= 20
elif rom_gb and rom_gb <= 8:
    rate -= 10

if cpu_mhz and cpu_mhz <= 1200:
    rate -= 15

rate = max(1, min(100, rate))


# ═══════════════════════════════════
#           PHONE INFO
# ═══════════════════════════════════

print("\n╭━━━╾ 📱 ANDROID DEVICE CHECKER ╼━━╮")
print(f"┃ Android    : {android}")
print(f"┃ RAM        : {ram_mb} MB")
print(f"┃ ROM        : {rom_gb:.1f} GB")
print(f"┃ CPU        : {cpu} / {cpu_mhz:.0f} MHz")
print(f"┃ GPU        : {gpu}")
print(f"┃ Root       : {'Yes 🔓' if root else 'No 🔒'}")
print(f"┃ Phone Rate : {rate}/100")
print("╰━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╯")


# ═══════════════════════════════════
#          STOP CONDITIONS
# ═══════════════════════════════════

stop = False

# The original thresholds are Android-specific.
# Windows/Linux are allowed to reach the menu.
if IS_TERMUX:
    if android.isdigit() and int(android) <= 7:
        print("\n⛔ Android version too old.")
        stop = True

    if ram_mb and ram_mb <= 1024:
        print("\n⛔ RAM is too low.")
        stop = True

    if rom_gb and rom_gb <= 16:
        print("\n⛔ ROM is too small.")
        stop = True

    if cpu_mhz and cpu_mhz <= 1405:
        print("\n⛔ CPU is too slow.")
        stop = True

if stop:
    print("\n🛑 Avengers stopped.")
    raise SystemExit(1)


print("\n✅ Device passed the requirements.")
print("🚀 Avengers started.")
time.sleep(5)


# ═══════════════════════════════════
#             MUSIC
# ═══════════════════════════════════

PlayMusic = si('Hey Boss Play Hacker Music? [y/n] ').strip().lower()

if PlayMusic == "y":
    music = get_path("Sounds/Music.mp3")

    if music.is_file():
        mpv = which("mpv")

        if mpv:
            try:
                subprocess.Popen(
                    [
                        mpv,
                        "--no-video",
                        "--no-terminal",
                        "--loop=inf",
                        str(music),
                    ],
                    cwd=str(BASE_DIR),
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                    env=child_environment(),
                )
                sp("Hacker Music Started!")
            except Exception as exc:
                sp("ERROR: Could not start MPV")
                sp(f"Reason: {exc}")
        else:
            sp("ERROR: MPV Not Found")
    else:
        sp("ERROR: Music.mp3 Not Found")

elif PlayMusic == "n":
    sp("Ok")

else:
    sp("Hey What Don't Play Music")


# ═══════════════════════════════════
#          AVENGERS MENU
# ═══════════════════════════════════
import os
os.system('clear')
os.system('cls')
# Run By The Avengers Os Engine (Ty9+)
clear_screen()
print(Fore.GREEN + """
╔══════════════════════╗
║T H E  A V E N G E R S║
╚══════════════════════╝
""")

print(Fore.RED + "1.DDoS [Distributed Denial of Service]")
print(Fore.RED + "2.Sms Bomber [Iran]")
print(Fore.RED + "3.RAT [Remote Access Trojan]")
print(Fore.RED + "4.CCTv Hack [IP Camera]")
print(Fore.RED + "5.Birds [Better Dirb]")
print(Fore.RED + "6.Pishing Page [Fake Login Page]")
print(Fore.RED + "7.Word Gen Pro [WordList Generator]")
print(Fore.RED + "8.Ultra Fast Download Speed [Marge DownLoaders]")
print(Fore.RED + "9.OP Compressor [6.7GB TXT To 256MB]")
print(Fore.RED + "10.NFC Drop [Android Air Drop]")
print(Fore.RED + "11.Web Chat [Via Flask]")
print(Fore.RED + "12.NanoGen Ai [Ask Ai]")
print(Fore.RED + "13.Thor Browser [ThorLe]")
print(Fore.RED + "14.HDB Boost [Heavy Dynamic Booster]")
print(Fore.RED + "15.Net Scanners [Scan WiFi Connection]")
print(Fore.RED + "16.HDB Chats [FreeDom Chat]")
print(Fore.RED + "17.Subscribe Telegram [Sub Telegram Channel]")
print(Fore.RED + "18.Subscribe GitHub [Sub GitHub Account]")
print(Fore.RED + "19.Settings [Avengers Settings]")
print(Fore.RED + "20.Exit [Don't Select This]")


User = si(Fore.YELLOW + "ẞelect Ñumber : ").strip()

# ═══════════════════════════════════
import os
os.system('clear')
os.system('cls')

#Ifer Elifer Elseer
if User == "1":
    # Existing local launcher; the payload itself is not modified here.
    run_python("HTools/ddos/ddos.py")
elif User == "2":
    run_go("HTools/GoSms/SMS.go")
elif User == "3":
    open_url("https://appteka.store/apps/fb0r169006/download")
elif User == "4":
    run_python("HTools/webhack/WebHack.py")
elif User == "5":
    run_python("HTools/Birds/main.py")
elif User == "6":
    run_python("HTools/UC/User.py")
elif User == "7":
    run_python("HTools/WordGenPro/Ban.py")
elif User == "8":
    run_python("HTools/UFIS/main.py")
elif User == "9":
    run_python("HTools/OPC/iop.py")
elif User == "10":
    run_bash("HTools/NFCD/NFCDrop.sh")
elif User == "11":
    run_python("HTools/FlaskChat/app.py")
elif User == "12":
    run_python("HTools/NanoGen/main.py")
elif User == "13":
    run_python("HTools/ThorBrowser/main.py")
elif User == "14":
    run_bash("HTools/HDB/HDB.sh")
elif User == "15":
    run_python("HTools/NetScanner/app.py")
elif User == "16":
    run_python("HTools/HDBChat/app.py")
elif User == "17":
    open_url("https://eitaa.com/HackerDot")
elif User == "18":
    open_url("https://github.com/banban965")
elif User == "19":
    run_python("Settings/S.py")
elif User == "20":
    run_python("Exit/Exit.py")
else:
    sp("\n❌ Invalid Selection")

