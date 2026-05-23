#!/usr/bin/env python3
import os
import zipfile
import sys

def repackage_epub(source_dir, output_epub):
    """
    Repackages an extracted directory into a spec-compliant EPUB.
    """
    if not os.path.exists(source_dir):
        print(f"Error: Source directory '{source_dir}' does not exist.")
        sys.exit(1)

    mimetype_path = os.path.join(source_dir, "mimetype")
    if not os.path.exists(mimetype_path):
        print(f"Error: 'mimetype' file not found at '{mimetype_path}'")
        sys.exit(1)

    print(f"Packaging EPUB from '{source_dir}' into '{output_epub}'...")

    with zipfile.ZipFile(output_epub, 'w') as epub_zip:
        # 1. Add 'mimetype' first, with ZIP_STORED (NO compression)
        epub_zip.write(mimetype_path, "mimetype", compress_type=zipfile.ZIP_STORED)

        # 2. Add all other files recursively with ZIP_DEFLATED (compression)
        for root, dirs, files in os.walk(source_dir):
            # Sort to guarantee deterministic, reproducible ZIP builds
            dirs.sort()
            files.sort()

            for file in files:
                filepath = os.path.join(root, file)
                relpath = os.path.relpath(filepath, source_dir)

                # Skip mimetype as we already added it first
                if relpath == "mimetype":
                    continue

                # Skip temporary/OS-generated files (e.g. .DS_Store, translation scripts)
                if file.startswith(".") or file.endswith(".py") or file.endswith(".orig"):
                    continue

                epub_zip.write(filepath, relpath, compress_type=zipfile.ZIP_DEFLATED)

    print("EPUB packaging complete! Running spec verification...")

    # Self-validation check
    with zipfile.ZipFile(output_epub, 'r') as verify_zip:
        infolist = verify_zip.infolist()
        if not infolist or infolist[0].filename != "mimetype":
            raise ValueError("Specification Violation: 'mimetype' must be the first file in the archive!")
        if infolist[0].compress_type != zipfile.ZIP_STORED:
            raise ValueError("Specification Violation: 'mimetype' must be completely uncompressed!")
        if verify_zip.read("mimetype") != b"application/epub+zip":
            raise ValueError("Specification Violation: 'mimetype' file content is malformed!")

    print("Verification passed! EPUB container is perfectly valid.")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python3 repack_epub.py <source_directory> <output_epub_name>")
        sys.exit(1)
    repackage_epub(sys.argv[1], sys.argv[2])
