import subprocess
import psutil
from pathlib import Path, WindowsPath
import argparse
from elevate import elevate
from psutil import Process
import time

DEFAULT_STEAM_PATH = Path('C:\Program Files (x86)\Steam\Steam.exe')
DEFAULT_GAME_PATH = Path('C:\Program Files (x86)\Steam\steamapps\common\Call of Duty Black Ops III\BlackOps3.exe')
START_FILENAME = 'blackops3.start'
BLACK_OPS_III_STEAM_APP_ID = 311210
GAME_ALIVE_CHECK_INTERVAL_SECONDS = 5
GAME_STARTED_CHECK_INTERVAL_SECONDS = 0.5

def create_parser():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        description='Launches Black Ops III with the T7 patch attached to it and closes the patch when the game is closed.'
    )

    parser.add_argument('--steam', default=DEFAULT_STEAM_PATH, help='Path to the Steam executable', metavar='STEAM_PATH', dest='steam_executable_path', type=Path)
    parser.add_argument('--game', default=DEFAULT_GAME_PATH, help='Path to the Black Ops III game executable', metavar='GAME_PATH', dest='game_executable_path', type=Path)
    parser.add_argument('--t7', help='Path to the T7 patch executable', metavar='T7_PATH', dest='t7_executable_path', required=True, type=Path)

    return parser

def start_t7_patch(t7_executable_path: Path):
    subprocess.Popen(str(t7_executable_path))

def stop_r7_patch(r7_executable_path: Path) -> int:
    subprocess.Popen(['taskkill', '/IM', r7_executable_path.name, '/F'])

def start_game(steam_executable_path: Path):
    subprocess.Popen([steam_executable_path, f'steam://rungameid/{BLACK_OPS_III_STEAM_APP_ID}'])

def game_is_running(game_executable_path: Path) -> bool:
    try:
        return game_executable_path.name in map(Process.name, psutil.process_iter())
    except psutil.NoSuchProcess:
        return True

def close_patch_when_game_closed(game_executable_path: Path, r7_executable_path: Path):
    while game_is_running(game_executable_path):
        time.sleep(GAME_ALIVE_CHECK_INTERVAL_SECONDS)

    stop_r7_patch(r7_executable_path)

if __name__ == "__main__":
    parser = create_parser()
    args = parser.parse_args()

    for arg in vars(args).values():
        if type(arg) == WindowsPath and not arg.exists():
            raise argparse.ArgumentTypeError(f'Path {arg} does not exist')

    start_path: Path = args.game_executable_path.parent / START_FILENAME
    start_path.unlink(missing_ok=True)

    # Escalate privileges required to execute the T7 patch
    elevate(show_console=False)

    start_t7_patch(args.t7_executable_path)
    start_game(args.steam_executable_path)

    # T7 creates a file called "blackops3.start" when the game is started, wait for it to exist
    while not start_path.exists():
        time.sleep(GAME_STARTED_CHECK_INTERVAL_SECONDS)

    # Wait for the game to close
    close_patch_when_game_closed(args.game_executable_path, args.t7_executable_path)

    # Delete the start file in case it still exists after closing T7
    start_path.unlink(missing_ok=True)
