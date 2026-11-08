import argparse
import os
import sys

import numpy as np
import pandas as pd


class InvalidConfigError(Exception):
    """Некорректные параметры запуска или проблема с записью файла."""


START_DATE = "2022-01-01"
PAYMENTS = ["наличные", "карта", "онлайн"]

STORE_CITIES = ["Москва", "Москва", "Санкт-Петербург", "Казань",
                "Новосибирск", "Екатеринбург", "Самара", "Сочи"]

PRODUCTS = [
    ("Напитки", "Кофе", 40, 250, 0.45, 0.10, 0.10, 1),
    ("Напитки", "Чай", 30, 150, 0.40, -0.08, 0.15, 1),
    ("Напитки", "Лимонад", 35, 120, 0.50, 0.05, 0.50, 7),
    ("Одежда", "Футболка", 15, 900, 0.50, 0.12, 0.35, 7),
    ("Одежда", "Куртка", 6, 6500, 0.55, -0.05, 0.60, 1),
    ("Одежда", "Шапка", 10, 800, 0.45, 0.00, 0.50, 1),
    ("Электроника", "Наушники", 8, 4500, 0.65, 0.15, 0.25, 12),
    ("Электроника", "Зарядка", 12, 1200, 0.50, 0.03, 0.05, 6),
    ("Электроника", "Мышь", 9, 1500, 0.55, -0.10, 0.05, 3),
]

WEEKEND = {"Напитки": 1.25, "Одежда": 1.35, "Электроника": 0.90}


def parse_args(argv=None):
    parser = argparse.ArgumentParser(description="Генератор данных о продажах сети магазинов")
    parser.add_argument("--seed", type=int, default=42, help="seed генератора случайных чисел")
    parser.add_argument("--years", type=int, default=3, help="количество лет (1-10)")
    parser.add_argument("--stores", type=int, default=6, help="количество магазинов (5-8)")
    parser.add_argument("--out", type=str, default="data/sales.csv", help="путь к CSV-файлу")
    return parser.parse_args(argv)


def validate_config(args):
    if not 1 <= args.years <= 10:
        raise InvalidConfigError(f"должно быть от 1 до 10, получено {args.years}")
    if not 5 <= args.stores <= len(STORE_CITIES):
        raise InvalidConfigError(f"должно быть от 5 до {len(STORE_CITIES)}, получено {args.stores}")
    if not args.out.strip():
        raise InvalidConfigError("не может быть пустым")
    if os.path.isdir(args.out):
        raise InvalidConfigError(f"указывает на папку, а не на файл: {args.out}")


def build_grid(years, n_stores):
    start = pd.Timestamp(START_DATE)
    end = start + pd.DateOffset(years=years) - pd.Timedelta(days=1)
    dates = pd.date_range(start, end, freq="D")
    index = pd.MultiIndex.from_product(
        [range(n_stores), range(len(PRODUCTS)), dates], names=["store", "prod", "date"])
    return index.to_frame(index=False)


def generate_sales(seed, years, n_stores):
    rng = np.random.default_rng(seed)
    df = build_grid(years, n_stores)
    n = len(df)
    s = df["store"].to_numpy()
    p = df["prod"].to_numpy()

    base_qty = np.array([x[2] for x in PRODUCTS])
    base_price = np.array([x[3] for x in PRODUCTS])
    cost_share = np.array([x[4] for x in PRODUCTS])
    trend_year = np.array([x[5] for x in PRODUCTS])
    season_amp = np.array([x[6] for x in PRODUCTS])
    peak_day = (np.array([x[7] for x in PRODUCTS]) - 0.5) * 30.4
    weekend_k = np.array([WEEKEND[x[0]] for x in PRODUCTS])

    store_size = rng.uniform(0.7, 1.4, n_stores) 

    t = (df["date"] - pd.Timestamp(START_DATE)).dt.days.to_numpy() / 365.25 
    doy = df["date"].dt.dayofyear.to_numpy()
    is_weekend = df["date"].dt.dayofweek.to_numpy() >= 5

    trend = np.maximum(1 + trend_year[p] * t, 0.2)
    week = np.where(is_weekend, weekend_k[p], 1.0)
    year = 1 + season_amp[p] * np.cos(2 * np.pi * (doy - peak_day[p]) / 365.25)
    
    promo = (rng.random(n) < 0.12).astype(int)
    df["promo"] = promo
    prev_promo = df.groupby(["store", "prod"])["promo"].shift(1, fill_value=0).to_numpy()
    after_promo = (prev_promo == 1) & (promo == 0)

    lam = (base_qty[p] * store_size[s] * trend * week * year
           * np.where(promo == 1, 1.4, 1.0)
           * np.where(after_promo, 0.9, 1.0))
    qty = rng.poisson(lam)  

    price = base_price[p] * (1 + 0.03 * t) * np.where(promo == 1, 0.85, 1.0) * rng.normal(1, 0.02, n)
    cost = base_price[p] * cost_share[p] * (1 + 0.03 * t)

    result = pd.DataFrame({
        "date": df["date"],
        "store_id": ["S%02d" % (i + 1) for i in s],
        "city": [STORE_CITIES[i] for i in s],
        "category": [PRODUCTS[i][0] for i in p],
        "product": [PRODUCTS[i][1] for i in p],
        "qty": qty,
        "price": price.round(2),
        "cost": cost.round(2),
        "promo": promo,
        "payment_method": rng.choice(PAYMENTS, size=n, p=[0.20, 0.55, 0.25]),
    })
    return result


def add_anomalies(df, rng, share=0.016):
    n = len(df)
    idx = rng.choice(n, size=int(n * share), replace=False)
    half = len(idx) // 2
    df.loc[idx[:half], "qty"] = df.loc[idx[:half], "qty"] * 8
    df.loc[idx[half:], "price"] = (df.loc[idx[half:], "price"]
                                   * rng.choice([5, 0.1], size=len(idx) - half)).round(2)
    return df


def add_missing(df, rng, share=0.01):
    n = len(df)
    df.loc[rng.random(n) < share, "price"] = np.nan
    df.loc[rng.random(n) < share, "payment_method"] = np.nan
    return df


def save_csv(df, path):
    try:
        folder = os.path.dirname(path)
        if folder:
            os.makedirs(folder, exist_ok=True)
        df.to_csv(path, index=False, date_format="%Y-%m-%d")
    except OSError as e:
        raise InvalidConfigError(f"не удалось записать файл '{path}': {e.strerror or e}")


def main():
    args = parse_args()
    try:
        validate_config(args)
        df = generate_sales(args.seed, args.years, args.stores)
        rng = np.random.default_rng(args.seed + 1)
        df = add_anomalies(df, rng)
        df = add_missing(df, rng)
        df = df.sort_values(["date", "store_id", "product"]).reset_index(drop=True)
        save_csv(df, args.out)
    except InvalidConfigError as e:
        print(f"Ошибка: {e}", file=sys.stderr)
        return 1
    print(f"Готово: {len(df)} строк записано в {args.out}")
    return 0

if __name__ == "__main__":
    sys.exit(main())