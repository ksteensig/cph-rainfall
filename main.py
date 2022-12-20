import argparse
import matplotlib.pyplot as plt
import pandas as pd
import requests

DAYS_OF_WEEK = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

def get_location_data(api_key, station_id="06180", parameter_id="precip_past1h", limit=8760):
    DMI_URL = 'https://dmigw.govcloud.dk/v2/metObs/collections/observation/items'
    r = requests.get(DMI_URL, params={'api-key': api_key, "stationId": station_id, "parameterId": parameter_id, "limit": limit})
    json = r.json()
    df = pd.json_normalize(json['features'])
    
    df['time'] = pd.to_datetime(df['properties.observed'])

    return df


if __name__ ==  "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--api-key", help="DMI API key", type=str, required=True)
    args = parser.parse_args()

    api_key = args.api_key

    df = get_location_data(api_key)
    df = df.sort_values(by='time', ascending=False)
    df = df[["time", "properties.value"]].resample('D', on = 'time').sum()
    df = df.sort_values(by='time', ascending=False)
    df["weekday"] = df.index.day_name()

    result = pd.DataFrame(columns=["weekday", "mean", "std"])

    result = result.set_index('weekday')

    for wd in DAYS_OF_WEEK:        
        m = df[df["weekday"] == wd].mean()
        s = df[df["weekday"] == wd].std()

        result.loc[wd] = [float(m), float(s)]

    plt.errorbar(result.index, result["mean"], yerr=result["std"], fmt='-o', ecolor="red")

    plt.xlabel("weekday")

    plt.ylabel("avg rain in mm")

    plt.show()

