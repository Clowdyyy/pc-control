import platform
import psutil

def get_cpu_info() -> dict:
    cpu_freq = psutil.cpu_freq()
    return {
        "model": platform.processor() or "Неизвестно",
        "cores_physical": psutil.cpu_count(logical=False) or "Неизвестно",
        "cores_logical": psutil.cpu_count(logical=True) or "Неизвестно",
        "freq_current": f"{cpu_freq.current:.0f} МГц" if cpu_freq else "Неизвестно",
        "freq_max": f"{cpu_freq.max:.0f} МГц" if cpu_freq and cpu_freq.max else "Неизвестно",
    }

def get_ram_info() -> dict:
    vm = psutil.virtual_memory()
    return {
        "total": f"{vm.total / (1024**3):.1f} ГБ",
        "available": f"{vm.available / (1024**3):.1f} ГБ",
        "used": f"{vm.used / (1024**3):.1f} ГБ",
        "percent": f"{vm.percent}%",
    }

def get_gpu_info() -> dict:
    try:
        import subprocess
        result = subprocess.run(
            ["wmic", "path", "win32_videocontroller", "get", "name,AdapterRAM", "/format:list"],
            capture_output=True, text=True, timeout=5
        )
        name = None
        vram = "Неизвестно"
        for line in result.stdout.splitlines():
            line = line.strip()
            if line.startswith("Name="):
                name = line.split("=", 1)[1].strip()
            elif line.startswith("AdapterRAM="):
                try:
                    vram_bytes = int(line.split("=", 1)[1].strip())
                    vram = f"{vram_bytes / (1024**3):.1f} ГБ" if vram_bytes > 0 else "Неизвестно"
                except (ValueError, TypeError):
                    pass
        return {"name": name or "Не обнаружено", "vram": vram}
    except Exception:
        return {"name": "Не обнаружено", "vram": "Неизвестно"}

def get_disk_info() -> list:
    disks = []
    for part in psutil.disk_partitions():
        try:
            usage = psutil.disk_usage(part.mountpoint)
            disks.append({
                "device": part.device,
                "mountpoint": part.mountpoint,
                "total": f"{usage.total / (1024**3):.1f} ГБ",
                "used": f"{usage.used / (1024**3):.1f} ГБ",
                "free": f"{usage.free / (1024**3):.1f} ГБ",
                "percent": f"{usage.percent}%",
            })
        except PermissionError:
            pass
    return disks

def get_windows_info() -> dict:
    return {
        "system": platform.system(),
        "release": platform.release(),
        "version": platform.version(),
        "build": platform.version().split(".")[-1] if "." in platform.version() else "Неизвестно",
        "machine": platform.machine(),
    }
