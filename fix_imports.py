from pathlib import Path

def fix_imports(root_dir=".", include_venv=True):
    """
    Fix outdated nomad imports in Python files.
    """
    # Define individual fixes
    fixes = [
        # Single imports
        ("from nomad.metainfo import EntryArchive", "from nomad.datamodel.datamodel import EntryArchive"),
        ("from nomad.metainfo import ArchiveSection", "from nomad.datamodel.metainfo.basesections import ArchiveSection"),
        ("from nomad.metainfo import EntryData", "from nomad.datamodel.datamodel import EntryData"),
        ("from nomad.metainfo import Results", "from nomad.datamodel.results import Results"),
        
        # Multi-line import - fix the combined one
        ("from nomad.datamodel.metainfo.basesections import ArchiveSection, EntryArchive, EntryData, Results",
         "from nomad.datamodel.metainfo.basesections import ArchiveSection\nfrom nomad.datamodel.datamodel import EntryArchive, EntryData\nfrom nomad.datamodel.results import Results"),
        
        # Another common multi-import pattern
        ("from nomad.metainfo import ArchiveSection, EntryArchive, EntryData, Results",
         "from nomad.datamodel.metainfo.basesections import ArchiveSection\nfrom nomad.datamodel.datamodel import EntryArchive, EntryData\nfrom nomad.datamodel.results import Results"),
    ]
    
    count = 0
    paths_to_check = [Path(root_dir) / "packages"]
    
    if include_venv:
        venv_path = Path(root_dir) / ".venv" / "lib"
        if venv_path.exists():
            paths_to_check.append(venv_path)
    
    for search_path in paths_to_check:
        if not search_path.exists():
            continue
            
        print(f"\nSearching in: {search_path}")
        for py_file in search_path.rglob("*.py"):
            try:
                content = py_file.read_text()
                original_content = content
                
                # Apply fixes in order (multi-line first to avoid partial replacements)
                for old_import, new_import in fixes:
                    content = content.replace(old_import, new_import)
                
                if content != original_content:
                    py_file.write_text(content)
                    print(f"Fixed: {py_file}")
                    count += 1
                    
            except Exception as e:
                print(f"Error processing {py_file}: {e}")
    
    print(f"\nTotal files fixed: {count}")

if __name__ == "__main__":
    fix_imports()