import argparse
import logging
import os
import sys
import time

import polars as pl
import psutil

# ------------------------- Logging Setup ------------------------- #


def setup_logging(verbose: bool = False) -> None:
    """
    Configure logging to write to file and console.
    Console logs INFO level by default, DEBUG if verbose.
    """
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG if verbose else logging.INFO)

    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

    # File handler
    file_handler = logging.FileHandler('extractor.log', mode='a', encoding='utf-8')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    # Console handler
    console_handler = logging.StreamHandler()
    console_level = logging.DEBUG if verbose else logging.INFO
    console_handler.setLevel(console_level)
    console_handler.setFormatter(logging.Formatter('%(message)s'))
    logger.addHandler(console_handler)


# ------------------------- Filter Parsing ------------------------- #


def parse_cli_filters(filters_raw: list[str]) -> dict[str, list[str]]:
    """
    Parse CLI filter arguments of form 'field=value1,value2,...' into a dict.

    Args:
        filters_raw: List of raw filter strings.

    Returns:
        Dictionary mapping field names to list of filter values.
    """
    filters = {}
    for arg in filters_raw:
        if '=' not in arg:
            logging.warning(f"Skipping invalid filter argument (no '='): {arg}")
            continue
        key, value = arg.split('=', 1)
        filters[key.strip()] = [v.strip() for v in value.split(',') if v.strip()]
    return filters


def prompt_filters(columns: list[str]) -> dict[str, list[str]]:
    """
    Prompt user interactively to enter filters for columns.

    Args:
        columns: List of valid column names.

    Returns:
        Dictionary of filters from user input.
    """
    print('\n📌 Available fields:', ', '.join(columns))
    filters = {}
    while True:
        field = input('Field name (leave empty to stop): ').strip()
        if not field:
            break
        if field not in columns:
            print(f"❌ '{field}' is not a valid column.")
            continue
        values = input(f'Enter comma-separated values for {field}: ').strip()
        filters[field] = [v.strip() for v in values.split(',') if v.strip()]
    return filters


# ------------------------- Prompt Options ------------------------- #


def prompt_unique_field(columns: list[str]) -> str:
    """
    Prompt user to select a unique field from available columns.

    Args:
        columns: List of valid column names.

    Returns:
        Selected unique field as string.
    """
    print('\n🎯 Available fields:', ', '.join(columns))
    while True:
        field = input('Select the field to extract unique values from: ').strip()
        if field in columns:
            return field
        print(f"❌ Invalid field '{field}'. Try again.")


def prompt_separator(default_sep: str = ';') -> str:
    """
    Prompt user for separator, return default if empty.

    Args:
        default_sep: Default separator string.

    Returns:
        Separator string.
    """
    sep = input(f"Enter separator for unique values (default '{default_sep}'): ").strip()
    return sep if sep else default_sep


def prompt_column_name(default_col: str) -> str:
    """
    Prompt user for custom output column name.

    Args:
        default_col: Default column name.

    Returns:
        Column name string.
    """
    name = input(f"Enter custom column name (default '{default_col}'): ").strip()
    return name if name else default_col


def prompt_row_format() -> str:
    """
    Prompt user for output row format (single or multi).

    Returns:
        'single' or 'multi'
    """
    while True:
        choice = input("Row format? (single/multi) [default=single]: ").strip().lower()
        if choice in {'', 'single'}:
            return 'single'
        if choice == 'multi':
            return 'multi'
        print("Invalid option. Choose 'single' or 'multi'.")


# ------------------------- Core Processing ------------------------- #


def filter_and_extract(
    input_file: str,
    filters: dict[str, list[str]],
    unique_field: str,
    delimiter: str,
) -> pl.Series:
    """
    Filter the CSV file by filters and extract unique values from the unique_field.

    Special handling for 'contact_ids' field (split, trim, explode).

    Args:
        input_file: Path to input CSV file.
        filters: Dictionary of filters.
        unique_field: Field to extract unique values from.
        delimiter: CSV delimiter.

    Returns:
        Polars Series with unique values.
    """
    filter_columns = list(filters.keys())
    needed_columns = set(filter_columns + [unique_field])

    lf = pl.read_csv(input_file, separator=delimiter, columns=list(needed_columns)).lazy()

    for col in needed_columns:
        lf = lf.with_columns(pl.col(col).cast(pl.Utf8).str.strip_chars().alias(col))
        lf = lf.filter(pl.col(col).is_not_null() & (pl.col(col) != ''))

    for field, vals in filters.items():
        lf = lf.filter(pl.col(field).is_in(vals))

    if unique_field == 'contact_ids':
        lf = (
            lf.with_columns(pl.col('contact_ids').str.split(',').alias('contact_list'))
            .explode('contact_list')
            .with_columns(pl.col('contact_list').str.strip_chars().alias('contact'))
            .filter(pl.col('contact').is_not_null() & (pl.col('contact') != ''))
        )
        result = lf.select(pl.col('contact').unique()).collect()
        return result['contact']

    result = lf.select(pl.col(unique_field).unique()).collect()
    return result[unique_field]


# ------------------------- Output Save ------------------------- #


def save_output(
    series: pl.Series,
    filters: dict[str, list[str]],
    unique_field: str,
    output_file: str,
    separator: str,
    row_format: str,
    column_name: str,
) -> None:
    """
    Save the extracted unique values to CSV file with overwrite confirmation.

    Args:
        series: Polars Series containing unique values.
        filters: Filters applied (for metadata).
        unique_field: Field name extracted from.
        output_file: Path to output CSV file.
        separator: Separator for single-row output.
        row_format: 'single' or 'multi' row output.
        column_name: Output CSV column name.
    """
    try:
        if os.path.exists(output_file):
            confirm = input(f"⚠️ File '{output_file}' exists. Overwrite? (y/n): ").strip().lower()
            if confirm != 'y':
                print('❌ Aborted by user.')
                return

        if row_format == 'single':
            out_df = pl.DataFrame({
                'filters': [', '.join(f"{k}={','.join(v)}" for k, v in filters.items())],
                column_name: [separator.join(series.to_list())],
            })
        else:
            out_df = pl.DataFrame({column_name: series})

        out_df.write_csv(output_file)
        logging.info(f"Saved output to: {output_file}")
        print(f"\n✅ Output saved to: {output_file}")
    except Exception as e:
        logging.error(f"Failed to save output: {e}", exc_info=True)
        print(f"❌ Failed to save output: {e}")


# ------------------------- Main Entry Point ------------------------- #


def main() -> None:
    """
    Main function to parse arguments, prompt user if needed,
    perform extraction and save results.
    """
    parser = argparse.ArgumentParser(
        description='Extract unique values from a CSV using Polars.'
    )
    parser.add_argument('--input', required=True, help='Input CSV file path')
    parser.add_argument('--output', help='Output CSV file path')
    parser.add_argument('--unique-field', help='Field name to extract unique values from')
    parser.add_argument('--separator', default=';', help='Separator for single-row output')
    parser.add_argument('--column-name', help='Custom column name for output')
    parser.add_argument(
        '--row-format', choices=['single', 'multi'], help='Output format: single or multi'
    )
    parser.add_argument('--delimiter', default=',', help="CSV delimiter (default=',')")
    parser.add_argument('--verbose', action='store_true', help='Enable verbose logging')
    parser.add_argument('filters', nargs='*', help='Filters in format field=value1,value2,...')

    args = parser.parse_args()

    setup_logging(args.verbose)
    logging.info(f"Script started with input: {args.input}")

    if not os.path.exists(args.input):
        logging.error(f"Input file '{args.input}' does not exist.")
        print(f"❌ Input file '{args.input}' does not exist.")
        sys.exit(1)

    try:
        df_preview = pl.read_csv(args.input, separator=args.delimiter, n_rows=5)
        columns = df_preview.columns
    except Exception as e:
        logging.error(f"Failed to read input CSV: {e}", exc_info=True)
        print(f"❌ Error reading input file: {e}")
        sys.exit(1)

    filters = parse_cli_filters(args.filters) if args.filters else prompt_filters(columns)

    # Validate columns
    for col in filters.keys():
        if col not in columns:
            print(f"❌ Column '{col}' not found in input file.")
            sys.exit(1)

    unique_field = args.unique_field or prompt_unique_field(columns)
    if unique_field not in columns and unique_field != 'contact_ids':
        print(f"❌ Unique field '{unique_field}' is not in the input file.")
        sys.exit(1)

    separator = args.separator if args.unique_field else prompt_separator()
    column_name = args.column_name or prompt_column_name(f'unique_{unique_field}')
    row_format = args.row_format or prompt_row_format()

    start_time = time.time()
    try:
        result_series = filter_and_extract(args.input, filters, unique_field, args.delimiter)
    except Exception as e:
        logging.error(f"Filtering failed: {e}", exc_info=True)
        print(f"❌ Filtering failed: {e}")
        sys.exit(1)

    if result_series.is_empty():
        print('ℹ️ No matching values found.')
        return

    print('\n🔎 Unique values found:')
    for val in result_series.to_list():
        print(f' - {val}')

    if args.output:
        save_output(
            result_series,
            filters,
            unique_field,
            args.output,
            separator,
            row_format,
            column_name,
        )
    else:
        save = input('\n💾 Save results to CSV? (y/n): ').lower().strip()
        if save == 'y':
            out_path = input('Output file name: ').strip()
            save_output(
                result_series,
                filters,
                unique_field,
                out_path,
                separator,
                row_format,
                column_name,
            )

    elapsed = time.time() - start_time
    mem_used = psutil.Process().memory_info().rss / (1024 * 1024)
    print(f'\n⏱️ Time taken: {elapsed:.2f}s | 🧠 Memory used: {mem_used:.2f} MB')
    logging.info(f'Time: {elapsed:.2f}s, Memory: {mem_used:.2f} MB')


if __name__ == '__main__':
    main()
