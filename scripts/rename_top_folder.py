"""Repack a tools archive with its top folder renamed, every file otherwise kept as it is.

    python3 -I scripts/rename_top_folder.py <archive.zip> <from> <to> <out.zip>

Each entry under <from>/ is written under <to>/ with the same bytes, timestamp, attributes and compression; an entry
outside <from>/ stops it, so nothing is dropped or moved by accident. It then reads both archives back and fails
unless the trees under the two folders are identical (names, the SHA-256 of each file's bytes, timestamps, attributes),
and prints the new archive's SHA-256 and size, which is what timeLink's tools.lock pins.
Standard library only.
"""
import copy
import hashlib
import os
import sys
import zipfile


def tree(path, top):
    with zipfile.ZipFile(path) as z:
        return {i.filename[len(top):]: (hashlib.sha256(z.read(i)).hexdigest(), i.date_time, i.external_attr)
                for i in z.infolist()}


def main(argv):
    if len(argv) != 4:
        print(__doc__.strip().splitlines()[2].strip(), file=sys.stderr)
        return 2
    src, old, new, out = argv
    old, new = old.rstrip("/") + "/", new.rstrip("/") + "/"
    if os.path.exists(out):
        print(f"rename_top_folder: {out} already exists", file=sys.stderr)
        return 1
    with zipfile.ZipFile(src) as zi, zipfile.ZipFile(out, "w") as zo:
        for info in zi.infolist():
            if not info.filename.startswith(old):
                print(f"rename_top_folder: {info.filename} is not under {old}", file=sys.stderr)
                return 1
            renamed = copy.copy(info)
            renamed.filename = renamed.orig_filename = new + info.filename[len(old):]
            level = 9 if info.compress_type == zipfile.ZIP_DEFLATED else None
            zo.writestr(renamed, zi.read(info), compress_type=info.compress_type, compresslevel=level)
    if tree(src, old) != tree(out, new):
        print("rename_top_folder: the repacked tree differs from the original", file=sys.stderr)
        return 1
    with zipfile.ZipFile(out) as z:
        if z.testzip() is not None:
            print("rename_top_folder: the repacked archive fails its own check", file=sys.stderr)
            return 1
    digest = hashlib.sha256()
    with open(out, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            digest.update(chunk)
    print(f"{digest.hexdigest()} {os.path.getsize(out)} {len(tree(out, new))} files identical")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
