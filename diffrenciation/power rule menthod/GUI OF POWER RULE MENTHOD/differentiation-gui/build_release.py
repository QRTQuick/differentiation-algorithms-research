import platform
import shutil
import subprocess
import sys
import zipfile
from pathlib import Path


APP_DIR = Path(__file__).resolve().parent
MAIN_SCRIPT = APP_DIR / "main.py"
DIST_DIR = APP_DIR / "dist"
BUILD_DIR = APP_DIR / "build"
ARTIFACTS_DIR = APP_DIR / "build_artifacts"
APP_NAME = "QuickRedTechDifferentiator"


def _run(command: list[str]):
    subprocess.run(command, cwd=APP_DIR, check=True)


def _clean():
    for path in (DIST_DIR, BUILD_DIR, ARTIFACTS_DIR):
        if path.exists():
            shutil.rmtree(path)
    ARTIFACTS_DIR.mkdir(parents=True, exist_ok=True)


def _build_with_pyinstaller():
    command = [
        sys.executable,
        "-m",
        "PyInstaller",
        "--noconfirm",
        "--clean",
        "--windowed",
        "--name",
        APP_NAME,
        "--paths",
        str(APP_DIR),
        "--add-data",
        f"{APP_DIR / 'resources'}{';' if platform.system() == 'Windows' else ':'}resources",
        "--collect-submodules",
        "gui",
        "--collect-submodules",
        "core",
        str(MAIN_SCRIPT),
    ]

    if platform.system() == "Darwin":
        command.extend(["--osx-bundle-identifier", "com.quickredtech.differentiator"])

    _run(command)


def _package_windows():
    app_dir = DIST_DIR / APP_NAME
    exe_path = app_dir / f"{APP_NAME}.exe"
    if not exe_path.exists():
        raise FileNotFoundError(f"Expected Windows executable at {exe_path}")

    archive_path = ARTIFACTS_DIR / f"{APP_NAME}-windows-exe.zip"
    with zipfile.ZipFile(archive_path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for path in app_dir.rglob("*"):
            if path.is_file():
                archive.write(path, arcname=path.relative_to(app_dir.parent))


def _package_macos():
    app_bundle = DIST_DIR / f"{APP_NAME}.app"
    if not app_bundle.exists():
        raise FileNotFoundError(f"Expected macOS app bundle at {app_bundle}")

    zip_path = ARTIFACTS_DIR / f"{APP_NAME}-macos-app.zip"
    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for path in app_bundle.rglob("*"):
            if path.is_file():
                archive.write(path, arcname=path.relative_to(app_bundle.parent))

    dmg_path = ARTIFACTS_DIR / f"{APP_NAME}-macos.dmg"
    _run(
        [
            "hdiutil",
            "create",
            "-volname",
            APP_NAME,
            "-srcfolder",
            str(app_bundle),
            "-ov",
            "-format",
            "UDZO",
            str(dmg_path),
        ]
    )


def main():
    _clean()
    _build_with_pyinstaller()

    system_name = platform.system()
    if system_name == "Windows":
        _package_windows()
    elif system_name == "Darwin":
        _package_macos()
    else:
        raise RuntimeError(f"Unsupported packaging platform: {system_name}")


if __name__ == "__main__":
    main()
