import pandas as pd

MONTHS = """
    januari
    februari
    mars
    april
    maj
    juni
    juli
    augusti
    september
    oktober
    november
    december
""".split()
MONTHS_I = {m: i + 1 for i, m in enumerate(MONTHS)}


def to_date(year, month):
    y = int(year)

    m = MONTHS_I[month] + 1

    if m >= 13:
        y += 1
        m = 1

    return f"{y:04d}{m:02d}"


def load():
    frame = pd.read_excel(
        "data/prel.xlsx",
        sheet_name="Tabell 11",
        header=9,
        index_col=0,
        usecols="B:I",
        nrows=12,
        na_values=0.0,
    )

    frame.columns.name = "År"
    frame = frame.T

    series = frame.stack()
    series.index = pd.to_datetime(
        [to_date(y, m) for y, m in series.index], format="%Y%m"
    )

    return (series / 100000.0).rolling(12).sum()


if __name__ == "__main__":
    print(load())
