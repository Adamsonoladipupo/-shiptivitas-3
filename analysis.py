import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

connection = sqlite3.connect("shiptivity.db")

# GRAPH 1: Daily Active Users

daily_users_query = """
SELECT
    date(login_timestamp, 'unixepoch') AS login_date,
    COUNT(DISTINCT user_id) AS daily_active_users
FROM login_history
GROUP BY date(login_timestamp, 'unixepoch')
ORDER BY login_date;
"""

daily_users = pd.read_sql_query(
    daily_users_query,
    connection
)

daily_users["login_date"] = pd.to_datetime(
    daily_users["login_date"]
)

feature_date = pd.Timestamp("2018-06-02")

daily_users["period"] = daily_users["login_date"].apply(
    lambda date: "Before" if date < feature_date else "After"
)

before_average = daily_users.loc[
    daily_users["period"] == "Before",
    "daily_active_users"
].mean()

after_average = daily_users.loc[
    daily_users["period"] == "After",
    "daily_active_users"
].mean()

# Create Graph 1
plt.figure(figsize=(14, 6))

plt.plot(
    daily_users["login_date"],
    daily_users["daily_active_users"],
    linewidth=1
)

plt.axvline(
    feature_date,
    linestyle="--",
    linewidth=2,
    label="Kanban Board released — 2018-06-02"
)

plt.axhline(
    before_average,
    linestyle=":",
    linewidth=1.5,
    label=f"Before average: {before_average:.2f}"
)

plt.axhline(
    after_average,
    linestyle=":",
    linewidth=1.5,
    label=f"After average: {after_average:.2f}"
)

plt.title(
    "Daily Active Users Before and After Kanban Board Release"
)

plt.xlabel("Date")
plt.ylabel("Daily Active Users")

plt.legend()

plt.tight_layout()

plt.savefig(
    "graph_1_daily_active_users.png",
    dpi=200
)

plt.close()

# GRAPH 2: Status Changes by Card

status_query = """
SELECT
    status_changes,
    COUNT(*) AS number_of_cards
FROM (
    SELECT
        cardID,
        COUNT(*) AS status_changes
    FROM card_change_history
    WHERE oldStatus IS NOT newStatus
    GROUP BY cardID
)
GROUP BY status_changes
ORDER BY status_changes;
"""

status_distribution = pd.read_sql_query(
    status_query,
    connection
)

# Create Graph 2
plt.figure(figsize=(9, 6))

plt.bar(
    status_distribution["status_changes"].astype(str),
    status_distribution["number_of_cards"]
)

for x, y in zip(
    status_distribution["status_changes"].astype(str),
    status_distribution["number_of_cards"]
):
    plt.text(
        x,
        y + 1,
        str(y),
        ha="center"
    )

plt.title(
    "Number of Cards by Number of Status Changes"
)

plt.xlabel("Number of Status Changes")
plt.ylabel("Number of Cards")

plt.tight_layout()

plt.savefig(
    "graph_2_status_changes_by_card.png",
    dpi=200
)

plt.close()

connection.close()

print("Analysis complete.")
