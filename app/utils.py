"""
Utility functions for the ESG application
"""
import uuid
import shutil
from pathlib import Path
from typing import Optional, List
import logging
import pandas as pd
import re

logger = logging.getLogger(__name__)


def generate_unique_id() -> str:
    """Generate a unique ID for files and reports"""
    return str(uuid.uuid4())


def get_file_extension(filename: str) -> str:
    """Get file extension from filename"""
    return Path(filename).suffix.lower()


def is_allowed_file(filename: str, allowed_extensions: list) -> bool:
    """Check if file extension is allowed"""
    ext = get_file_extension(filename)
    return ext in allowed_extensions


def save_uploaded_file(file_content: bytes, filename: str, destination_dir: Path) -> Path:
    """
    Save uploaded file to destination directory
    
    Args:
        file_content: File content as bytes
        filename: Original filename
        destination_dir: Directory to save file
        
    Returns:
        Path to saved file
    """
    destination_dir.mkdir(exist_ok=True, parents=True)
    
    # Generate unique filename
    unique_id = generate_unique_id()
    file_ext = get_file_extension(filename)
    new_filename = f"{unique_id}_{filename}"
    
    file_path = destination_dir / new_filename
    
    with open(file_path, 'wb') as f:
        f.write(file_content)
    
    logger.info(f"File saved: {file_path}")
    return file_path


def cleanup_old_files(directory: Path, max_age_days: int = 7):
    """
    Clean up old files from a directory
    
    Args:
        directory: Directory to clean
        max_age_days: Maximum age of files in days
    """
    import time
    
    if not directory.exists():
        return
    
    current_time = time.time()
    max_age_seconds = max_age_days * 24 * 60 * 60
    
    for file_path in directory.iterdir():
        if file_path.is_file():
            file_age = current_time - file_path.stat().st_mtime
            if file_age > max_age_seconds:
                try:
                    file_path.unlink()
                    logger.info(f"Deleted old file: {file_path}")
                except Exception as e:
                    logger.error(f"Error deleting file {file_path}: {e}")


def format_file_size(size_bytes: int) -> str:
    """Format file size in human readable format"""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.2f} TB"


def load_sme_csv_to_dataframe(
    csv_file_path: str,
    num_columns: Optional[int] = None,
    preserve_brackets: bool = True,
    merge_excess_into_notes: bool = True,
    notes_merge_start_idx: int = 7,
    fixed_suffix_count: int = 2,
    encoding: str = 'utf-8',
    verbose: bool = False
) -> pd.DataFrame:
    """
    Robustly loads a malformed SME CSV (unquoted commas, bracketed units) into a clean DataFrame.

    • Works with **any** number of columns – auto-detects the real column count.
    • Preserves `[…]` as atomic units.
    • Optionally merges excess middle fields into the "Notes" column.
    • Pads missing fields with empty strings.

    Args:
        csv_file_path (str): Path to the CSV file
        num_columns (int, optional): Expected number of columns. Auto-detected from header if None.
        preserve_brackets (bool): Treat [content] as single unit during split
        merge_excess_into_notes (bool): Merge extra fields in middle into Notes column
        notes_merge_start_idx (int): Column index where "Notes" section begins (0-indexed)
        fixed_suffix_count (int): Number of columns at the end to keep intact
        encoding (str): File encoding
        verbose (bool): Print progress and diagnostics

    Returns:
        pd.DataFrame: Cleaned dataframe with consistent columns
    """
    if verbose:
        logger.info(f"Loading CSV from: {csv_file_path}")

    # ------------------------------------------------------------------ #
    # 1. Read raw lines
    # ------------------------------------------------------------------ #
    try:
        with open(csv_file_path, 'r', encoding=encoding) as f:
            lines = [ln.rstrip('\n\r') for ln in f if ln.strip()]
    except FileNotFoundError:
        raise FileNotFoundError(f"CSV file not found: {csv_file_path}")
    except Exception as e:
        raise IOError(f"Error reading file: {e}")

    if not lines:
        raise ValueError("CSV file is empty.")
    if len(lines) == 1:
        raise ValueError("CSV has only a header row – no data.")

    if verbose:
        logger.info(f"Read {len(lines)} lines (including header)")

    # ------------------------------------------------------------------ #
    # 2. Core splitter – respects brackets, works without a target count
    # ------------------------------------------------------------------ #
    def smart_split_csv_line(
        line: str,
        target_cols: Optional[int] = None,
        *,
        preserve_brackets: bool = True
    ) -> List[str]:
        """
        Split a line while honouring nested `[…]`.  
        If *target_cols* is None → return everything that can be split.
        """
        if not preserve_brackets:
            parts = [p.strip() for p in line.split(',')]
        else:
            parts = []
            cur = []
            depth = 0
            for ch in line:
                if ch == '[':
                    depth += 1
                    cur.append(ch)
                elif ch == ']':
                    depth -= 1
                    cur.append(ch)
                elif ch == ',' and depth == 0:
                    parts.append(''.join(cur).strip())
                    cur = []
                else:
                    cur.append(ch)
            if cur:
                parts.append(''.join(cur).strip())

        # -------------------------------------------------------------- #
        # 2a. If we have a target → enforce it (pad / merge)
        # -------------------------------------------------------------- #
        if target_cols is None:
            return parts

        if len(parts) == target_cols:
            return parts

        if len(parts) > target_cols and merge_excess_into_notes:
            # keep prefix + suffix, collapse middle excess into first middle field
            prefix = parts[:notes_merge_start_idx]
            suffix = parts[-fixed_suffix_count:] if fixed_suffix_count else []
            middle = parts[notes_merge_start_idx : -fixed_suffix_count if fixed_suffix_count else None]

            expected_mid = target_cols - len(prefix) - len(suffix)
            if len(middle) > expected_mid:
                excess = middle[: len(middle) - expected_mid + 1]
                notes = ', '.join(excess)
                middle = [notes] + middle[len(middle) - expected_mid + 1 :]
            return prefix + middle + suffix

        # too few → pad
        parts += [''] * (target_cols - len(parts))
        return parts[:target_cols]

    # ------------------------------------------------------------------ #
    # 3. Detect the *real* column count (two-pass)
    # ------------------------------------------------------------------ #
    # First pass: split header without a target → raw header tokens
    raw_header = smart_split_csv_line(lines[0], target_cols=None,
                                      preserve_brackets=preserve_brackets)

    # If the user forced a count → honour it
    if num_columns is not None:
        detected_cols = num_columns
        if verbose:
            logger.info(f"User forced {detected_cols} columns.")
    else:
        # Heuristic: longest *well-formed* row (including header) defines the schema
        candidate_lengths = []
        for ln in lines:
            cand = smart_split_csv_line(ln, target_cols=None,
                                        preserve_brackets=preserve_brackets)
            # ignore rows that are obviously garbage (e.g., a single huge field)
            if len(cand) > 1:
                candidate_lengths.append(len(cand))

        if candidate_lengths:
            detected_cols = max(candidate_lengths)
        else:
            detected_cols = len(raw_header) or 1

        if verbose:
            logger.info(f"Auto-detected {detected_cols} columns (max well-formed row).")

    # ------------------------------------------------------------------ #
    # 4. Build final header (respect detected_cols)
    # ------------------------------------------------------------------ #
    header = smart_split_csv_line(lines[0], target_cols=detected_cols,
                                  preserve_brackets=preserve_brackets)
    # If header is shorter than detected → pad with generic names
    while len(header) < detected_cols:
        header.append(f'Unnamed_{len(header)}')

    if verbose:
        logger.info(f"Final header length: {len(header)}")

    # ------------------------------------------------------------------ #
    # 5. Parse data rows
    # ------------------------------------------------------------------ #
    data_rows = []
    bad_rows = []

    for idx, raw_line in enumerate(lines[1:], start=2):
        row = smart_split_csv_line(raw_line, target_cols=detected_cols,
                                   preserve_brackets=preserve_brackets)
        if len(row) != detected_cols:
            bad_rows.append((idx, len(row), row[:5]))  # keep a tiny preview
            if verbose and len(bad_rows) <= 5:
                logger.warning(f"Row {idx}: {len(row)} fields (expected {detected_cols})")
        data_rows.append(row)

    # ------------------------------------------------------------------ #
    # 6. Build DataFrame
    # ------------------------------------------------------------------ #
    df = pd.DataFrame(data_rows, columns=header)

    # ------------------------------------------------------------------ #
    # 7. Final sanity check & summary
    # ------------------------------------------------------------------ #
    if df.shape[1] != detected_cols:
        if verbose:
            logger.info(f"DataFrame column mismatch ({df.shape[1]} vs {detected_cols}). Fixing...")
        if df.shape[1] > detected_cols:
            df = df.iloc[:, :detected_cols]
            df.columns = header[:detected_cols]
        else:
            for j in range(df.shape[1], detected_cols):
                df[header[j]] = ''

    if verbose:
        logger.info(f"CSV loaded successfully! Shape: {df.shape[0]} rows × {df.shape[1]} columns")
        if bad_rows:
            logger.warning(f"{len(bad_rows)} rows had wrong column counts.")

    return df
