import argparse
import sqlite3
from pathlib import Path

import pandas as pd

COLS_TO_IGNORE = ["Duplicate?", "Duplicate", "To check?", "To fill?"]
COL_MAP = {
    "english": "eng",
    "croatian": "hrk",
}


def delete_empty_cols(df):
    return df.drop(columns=[c for c in df.columns if df[c].isnull().sum() == len(df)])


def make_cols_lower(df):
    return df.rename(columns={c: c.lower() for c in df.columns})


def parse_normal_sheets(f, normal_sheets, cols_to_ignore=None, cols_map=None):
    if cols_to_ignore is None:
        cols_to_ignore = []

    if cols_map is None:
        cols_map = {}

    df_dict = {}
    for sheet in normal_sheets:
        df = f.parse(sheet_name=sheet).pipe(
            pipe_normal_sheet, cols_to_ignore=cols_to_ignore, cols_map=cols_map
        )
        df_dict[sheet.lower()] = df

    return df_dict


def process_anki(df):
    return df.pipe(
        lambda df: df.assign(anki=df["Anki?"].fillna(False))
        if "Anki?" in df.columns
        else df.assign(anki=False)
    ).pipe(lambda df: df.drop(columns={"Anki?"}.intersection(df.columns)))


def remove_cols(df, cols):
    return df.pipe(lambda df: df.drop(columns=[c for c in cols if c in df.columns]))


def remove_unnamed_cols(df):
    return df.drop(columns=[c for c in df.columns if "Unnamed" in c])


def pipe_normal_sheet(df, cols_to_ignore, cols_map):
    return (
        df.pipe(remove_unnamed_cols)
        .pipe(remove_cols, cols=cols_to_ignore)
        .pipe(delete_empty_cols)
        .pipe(process_anki)
        .pipe(make_cols_lower)
        .rename(columns=cols_map)
        .dropna(axis=0, how="all")
    )


def parse_verb_sheet(f, sheet_name, cols_to_ignore=None, cols_map=None):
    if cols_to_ignore is None:
        cols_to_ignore = []

    if cols_map is None:
        cols_map = {}

    return (
        f.parse(sheet_name)
        .pipe(remove_cols, cols_to_ignore)
        .pipe(remove_unnamed_cols)
        .pipe(make_cols_lower)
        .rename(columns=cols_map)
        .dropna(axis=0, how="all")
        .assign(anki=False)
    )


def write_to_db(data_dict, db_path) -> None:
    with sqlite3.connect(db_path) as con:
        for k, df in data_dict.items():
            df.to_sql(k, con, if_exists="append")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("-db", action="store")
    parser.add_argument("-i", action="store_true")
    args = parser.parse_args()

    db_path = args.db
    init_db_flag = args.i

    if init_db_flag:
        p = Path(db_path)
        if p.exists():
            p.unlink()

    path = "./data/Vocab.xlsx"
    f = pd.ExcelFile(path)

    all_sheets = set(f.sheet_names)
    normal_sheets = {"Nouns", "Adjectives", "Adverbs", "ToSort"}.intersection(
        all_sheets
    )

    dict_sheets = parse_normal_sheets(
        f, normal_sheets=normal_sheets, cols_to_ignore=COLS_TO_IGNORE, cols_map=COL_MAP
    )

    df_verbs = parse_verb_sheet(
        f, sheet_name="Verbs", cols_to_ignore=COLS_TO_IGNORE, cols_map=COL_MAP
    )

    df_mess = parse_verb_sheet(
        f, sheet_name="mess", cols_to_ignore=COLS_TO_IGNORE, cols_map=COL_MAP
    )

    dict_sheets["verbs"] = pd.concat([df_verbs, df_mess], axis=0, ignore_index=True)

    write_to_db(dict_sheets, db_path=db_path)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
