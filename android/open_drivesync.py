#!/usr/bin/env python3

import argparse
import os
import re
import subprocess
import sys
import time
from typing import List, Optional


def adb(*args: str, check: bool = True) -> subprocess.CompletedProcess:
    return subprocess.run(["adb", *args], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, check=check)


def ensure_device() -> None:
    out = adb("devices").stdout.strip().splitlines()
    lines = [ln for ln in out if "\t" in ln]
    if not lines:
        print("No devices attached. Connect your Android and run again.")
        sys.exit(1)
    status = lines[0].split("\t", 1)[1]
    if status != "device":
        print(f"Device status is '{status}'. Authorize device and retry.")
        sys.exit(1)


def list_installed_packages() -> List[str]:
    out = adb("shell", "cmd", "package", "list", "packages").stdout
    pkgs: List[str] = []
    for line in out.splitlines():
        line = line.strip()
        if line.startswith("package:"):
            pkgs.append(line.split(":", 1)[1])
    return pkgs


def find_drivesync_package() -> Optional[str]:
    candidates = list_installed_packages()
    # Prefer exact-ish known ids first
    known = [
        "com.ttxapps.drivesync",              # legacy DriveSync
        "com.ttxapps.autosync",               # generic Autosync (older)
        "com.ttxapps.autosync.gdrive",        # Autosync for Google Drive (variant)
        "com.ttxapps.autosync.for.google.drive",  # verbose variant
        "com.metactrl.autosync",              # vendor rename possibilities
        "com.metactrl.autosync.gdrive",
    ]
    for k in known:
        if k in candidates:
            return k

    # Heuristic search: look for packages that clearly indicate autosync + drive
    lowered = [(p, p.lower()) for p in candidates]
    scored: List[tuple[int, str]] = []
    for original, low in lowered:
        score = 0
        if "autosync" in low:
            score += 2
        if "drive" in low:
            score += 2
        if "drivesync" in low:
            score += 3
        if "ttxapps" in low or "metactrl" in low:
            score += 2
        if score > 0:
            scored.append((score, original))
    if not scored:
        return None
    scored.sort(key=lambda t: t[0], reverse=True)
    return scored[0][1]


def launch_package(package: str) -> None:
    # Use monkey with LAUNCHER intent for reliability
    print(f"Launching '{package}' via monkey…")
    adb("shell", "monkey", "-p", package, "-c", "android.intent.category.LAUNCHER", "1")
    time.sleep(1.5)


def tap(x: int, y: int) -> None:
    print(f"tap: ({x}, {y})")
    adb("shell", "input", "tap", str(x), str(y))


def stop_package(package: str) -> None:
    print(f"Stopping '{package}'…")
    adb("shell", "am", "force-stop", package)


def main() -> None:
    parser = argparse.ArgumentParser(description="Open DriveSync/Autosync, tap, wait, close; then open LienePhoto and run one gallery loop")
    parser.add_argument("--package", dest="package", help="DriveSync/Autosync package name to launch (skips auto-discovery)")
    parser.add_argument("--liene-package", dest="liene_package", help="LienePhoto package name (skips auto-discovery)")
    args = parser.parse_args()

    ensure_device()

    package: Optional[str] = args.package
    if not package:
        package = find_drivesync_package()

    if not package:
        print("Could not find DriveSync/Autosync package automatically.")
        print("Try running: adb shell pm list packages | egrep -i 'autosync|drivesync' ")
        print("Then re-run with --package <found.package.id>")
        sys.exit(2)

    try:
        launch_package(package)
        # After app opens, perform the requested tap
        tap(930, 2250)
        time.sleep(5.0)
        # Close the app
        stop_package(package)
        print("DriveSync step: opened, tapped at 930,2250, waited 20s, then closed.")
    except subprocess.CalledProcessError as e:
        print("Failed to launch DriveSync/Autosync. Try specifying --package explicitly.")
        print(e.stdout or str(e))
        sys.exit(3)

    # Next: open LienePhoto and run 1 loop via gallery_loop.py
    # Discover Liene package if not provided
    liene_pkg: Optional[str] = args.liene_package

    if not liene_pkg:
        # Strict search: prefer known Liene/Hannto ids; otherwise require 'liene' or 'hannto' in id
        candidates = list_installed_packages()
        known_liene = [
            "com.liene.photo",
            "com.liene.lienephoto",
            "com.liene.mobile",
            "com.hannto.fennel.overseas",
            "com.hannto.fennel",
        ]
        for k in known_liene:
            if k in candidates:
                liene_pkg = k
                break
        if not liene_pkg:
            liene_like = [p for p in candidates if ("liene" in p.lower() or "hannto" in p.lower() or "fennel" in p.lower())]
            if liene_like:
                # Prefer shortest package name containing 'liene'
                liene_like.sort(key=len)
                liene_pkg = liene_like[0]

    if not liene_pkg:
        print("Could not find LienePhoto package automatically.")
        print("Try: adb shell pm list packages | egrep -i 'liene|hannto|fennel' ")
        print("Then re-run with --liene-package <found.package.id>")
        sys.exit(4)

    try:
        print(f"Launching LienePhoto package '{liene_pkg}'…")
        launch_package(liene_pkg)
        time.sleep(2.0)
    except subprocess.CalledProcessError as e:
        print("Failed to launch LienePhoto. Try specifying --liene-package explicitly.")
        print(e.stdout or str(e))
        sys.exit(5)

    # Invoke one iteration of the gallery loop (start=1, count=1)
    gallery_loop_path = os.path.join(os.path.dirname(__file__), "gallery_loop.py")
    if not os.path.exists(gallery_loop_path):
        print(f"gallery_loop.py not found at {gallery_loop_path}")
        sys.exit(6)
    print("Running one gallery loop (start=1, count=1)…")
    try:
        # Use the same Python interpreter to run the loop script
        subprocess.run([sys.executable, gallery_loop_path, "1", "1"], check=True)
        print("Gallery loop completed.")
    except subprocess.CalledProcessError as e:
        print("gallery_loop.py exited with an error.")
        print(e.stdout if hasattr(e, 'stdout') else str(e))
        sys.exit(7)


if __name__ == "__main__":
    main()


