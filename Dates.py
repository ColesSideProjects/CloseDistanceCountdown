import pandas as pd
from datetime import date, datetime, timedelta


class Dates:
    @staticmethod
    def get_dfs():
        days_together = {
            "California": ["03-06-2022", "01-08-2022"],
            "Spain": ["09-08-2022", "19-08-2022"],
            "Paris": ["21-01-2023", "22-02-2023"],
            "Hawaii": ["03-11-2023", "10-12-2023"],
            "Italy": ["03-03-2024", "17-03-2024"],
            "Moving": ["09-09-2024", date.today().strftime("%d-%m-%Y")]
                         }

        df = pd.DataFrame(days_together)

        df_melted = df.melt(var_name="name", value_name="date")
        df_melted["date"] = pd.to_datetime(df_melted["date"], format="%d-%m-%Y")
        df_melted = df_melted.sort_values(by="date").reset_index(drop=True)
        df_melted["ID"] = df_melted.index // 2 + 1
        df_melted["date_type"] = df_melted.groupby("ID").cumcount() + 1
        df_pivoted = df_melted.pivot(index="ID", columns="date_type", values="date").reset_index()
        df_pivoted.columns = ["ID", "date1", "date2"]
        df_final = df_pivoted.merge(df_melted[["ID", "name"]].drop_duplicates(), on="ID")
        df_final["number of days"] = (df_final["date2"] - df_final["date1"]).dt.days
        df_final["together"] = df_final["number of days"] > 0

        def fill_dates(row, next_row_date1=None):
            filled_rows = []
            if next_row_date1:
                filled_rows.append({
                    "date1": row["date2"] + timedelta(days=1),
                    "date2": next_row_date1 - timedelta(days=1),
                    "name": None,
                    "number of days": 0,
                    "together": False
                })
            return filled_rows

        filled_data = []
        for i, row in df_final.iterrows():
            next_row_date1 = df_final.loc[i + 1, "date1"] if i + 1 < len(df_final) else None
            filled_data.extend(fill_dates(row, next_row_date1))

        filled_df = pd.DataFrame(filled_data)
        combined_df = pd.concat([df_final, filled_df], ignore_index=True).sort_values(by=["date1"]).reset_index(drop=True)
        combined_df["number of days"] = (combined_df["date2"] - combined_df["date1"]).dt.days
        combined_df = combined_df.drop(columns=["ID"])


        combined_df.groupby("together")["number of days"].sum()


        stats_out = pd.DataFrame({
            "Days Together": combined_df.groupby("together")["number of days"].sum().iloc[1],
            "Days Separated": combined_df.groupby("together")["number of days"].sum().iloc[0],
            "Days Till 1": combined_df.groupby("together")["number of days"].sum().iloc[0] - combined_df.groupby("together")["number of days"].sum().iloc[1] + 1,
            "Days Till One Year": 365 - combined_df.groupby("together")["number of days"].sum().iloc[1],
        }, index=[0])

        stats_out["One Year Date"] = datetime.today() + pd.Timedelta(days=int(stats_out["Days Till One Year"].values[0]))
        stats_out["Plus One Date"] = datetime.today() + pd.Timedelta(days=int(stats_out["Days Till 1"].values[0]))


        combined_df["date1"] = pd.to_datetime(combined_df["date1"])
        combined_df["date2"] = pd.to_datetime(combined_df["date2"])
        combined_df["adjusted days"] = combined_df["number of days"] * combined_df["together"].apply(lambda x: 1 if x else -1)
        combined_df["name"] = combined_df["name"].apply(lambda x: "Long Distance" if not x else x)
        combined_df["moving average"] = combined_df["adjusted days"].cumsum()
        return combined_df, stats_out

if __name__ == "__main__":
    df, stats = Dates.get_dfs()
    print(df)
    print(stats)
