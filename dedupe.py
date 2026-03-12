import os
import hashlib
import shutil
from datetime import datetime

SOURCE_FOLDER = r"C:\Your\Photos\Folder"
DUPLICATES_FOLDER = r"C:\Your\Duplicates\Folder"
LOG_FILE = r"C:\dedupe_log.txt"

def get_file_hash(filepath):
    hasher = hashlib.md5()
    try:
        with open(filepath, 'rb') as f:
            while chunk := f.read(65536):
                hasher.update(chunk)
        return hasher.hexdigest()
    except:
        return None

def main():
    print("=" * 60)
    print("DUPLICATE FILE FINDER")
    print(f"Scanning: {SOURCE_FOLDER}")
    print("=" * 60)
    print()
    os.makedirs(DUPLICATES_FOLDER, exist_ok=True)
    seen_hashes = {}
    duplicates = []
    total_files = 0
    skipped = 0
    print("Scanning... this will take a while for large collections.")
    print()
    for root, dirs, files in os.walk(SOURCE_FOLDER):
        dirs[:] = [d for d in dirs if os.path.join(root, d) != DUPLICATES_FOLDER]
        for filename in files:
            filepath = os.path.join(root, filename)
            total_files += 1
            if total_files % 500 == 0:
                print(f"  Scanned {total_files} files... ({len(duplicates)} duplicates so far)")
            file_hash = get_file_hash(filepath)
            if file_hash is None:
                skipped += 1
                continue
            if file_hash in seen_hashes:
                duplicates.append((filepath, seen_hashes[file_hash]))
            else:
                seen_hashes[file_hash] = filepath
    print()
    print(f"Scan complete. {total_files} files scanned, {len(duplicates)} duplicates found.")
    print()
    if not duplicates:
        print("No duplicates found.")
        return
    confirm = input(f"Move {len(duplicates)} duplicates to {DUPLICATES_FOLDER}? (yes/no): ").strip().lower()
    if confirm != "yes":
        print("Cancelled.")
        return
    moved = 0
    log_lines = [f"Dedupe Log — {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", f"Total scanned: {total_files}", f"Duplicates found: {len(duplicates)}", ""]
    for dup_path, original_path in duplicates:
        try:
            dest_filename = os.path.basename(dup_path)
            dest_path = os.path.join(DUPLICATES_FOLDER, dest_filename)
            counter = 1
            base, ext = os.path.splitext(dest_filename)
            while os.path.exists(dest_path):
                dest_path = os.path.join(DUPLICATES_FOLDER, f"{base}_{counter}{ext}")
                counter += 1
            shutil.move(dup_path, dest_path)
            moved += 1
            log_lines.append(f"MOVED: {dup_path}")
            log_lines.append(f"KEPT:  {original_path}")
            log_lines.append("")
        except Exception as e:
            log_lines.append(f"ERROR: {dup_path} — {e}")
    with open(LOG_FILE, 'w', encoding='utf-8') as f:
        f.write('\n'.join(log_lines))
    print(f"Done. {moved} duplicates moved to {DUPLICATES_FOLDER}")
    print(f"Log saved to {LOG_FILE}")

if __name__ == "__main__":
    main()
