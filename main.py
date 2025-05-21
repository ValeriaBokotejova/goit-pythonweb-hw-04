import asyncio
import logging
from argparse import ArgumentParser
from pathlib import Path
import shutil
import os
from colorama import Fore, init

# Initialize colorama
init(autoreset=True)

# Configure logging
logging.basicConfig(
    filename='file_sorter.log',
    level=logging.ERROR,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

async def copy_file(file_path: Path, output_dir: Path):
    try:
        extension = file_path.suffix.lower().lstrip('.') or 'no_extension'
        target_dir = output_dir / extension
        await asyncio.to_thread(os.makedirs, target_dir, exist_ok=True)
        target_path = target_dir / file_path.name

        if not target_path.exists():
            await asyncio.to_thread(shutil.copy2, file_path, target_path)
            print(Fore.GREEN + f"Copied: {file_path.name} -> {target_dir}/")
        else:
            print(Fore.YELLOW + f"Skipped (already exists): {file_path.name}")
    except Exception as e:
        logging.error(f"Error copying file {file_path}: {e}")
        print(Fore.RED + f"Error copying file {file_path}: {e}")

async def read_folder(source_dir: Path, output_dir: Path):
    try:
        for path in source_dir.rglob('*'):
            if path.is_file():
                await copy_file(path, output_dir)
    except Exception as e:
        logging.error(f"Error reading folder {source_dir}: {e}")
        print(Fore.RED + f"Error reading folder {source_dir}: {e}")

def parse_arguments():
    parser = ArgumentParser(description="Asynchronously sort files by extension.")
    parser.add_argument("source", type=str, help="Path to the source directory (already contains files)")
    parser.add_argument("output", type=str, help="Path to the output directory (will be created if not exists)")
    return parser.parse_args()

async def main():
    args = parse_arguments()
    source = Path(args.source)
    output = Path(args.output)

    if not source.exists():
        logging.error(f"Source directory {source} does not exist.")
        print(Fore.RED + f"Source directory {source} does not exist.")
        return

    await asyncio.to_thread(output.mkdir, parents=True, exist_ok=True)
    await read_folder(source, output)

if __name__ == "__main__":
    asyncio.run(main())
