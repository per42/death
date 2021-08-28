import pandas as pd
from pyjstat import pyjstat


def to_date(month_code, monthly):
    v = [int(p) for p in month_code.split("M")]

    y = v[0]

    if monthly:
        m = v[1]
    else:
        m = 12

    m += 1

    if m >= 13:
        y += 1
        m = 1

    return f"{y:04d}{m:02d}"


def load(json_stat_path, monthly):
    with open(json_stat_path) as f:
        ds = pyjstat.Dataset.read(f.read())

    frame = ds.write("dataframe")

    if monthly:
        del frame["tabellinnehåll"]

        frame = frame.set_index(["månad", "förändringar"])

    else:
        frame = frame.set_index(["år", "tabellinnehåll"])

    series = frame.value

    frame = series.unstack()
    frame.index = pd.to_datetime(
        [to_date(c, monthly) for c in frame.index], format="%Y%m"
    )

    if monthly:
        return (frame["döda"] / frame["folkmängd"]).rolling(12).sum()
    else:
        return frame["Döda"] / frame["Folkmängd"]


def load_monthly():
    return load("data/ManadBefStatRegion.json", True)


def load_yearly():
    return load("data/BefUtvKon1749.json", False)


if __name__ == "__main__":
    series = load_monthly()
    print(series)
    series.plot()
    from matplotlib import pyplot as plt

    plt.savefig("scb.png")
