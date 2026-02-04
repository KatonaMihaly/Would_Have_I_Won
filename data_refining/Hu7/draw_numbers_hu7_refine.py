import pandas as pd
import re

def fix_date_format(date_str):
    if pd.isnull(date_str):
        return None
    date_str = str(date_str).strip('. ')
    date_str = re.sub(r'[.]', '-', date_str)
    # Convert to standard YYYY-MM-DD
    parts = date_str.split('-')
    if len(parts) == 3:
        return f"{parts[0]}-{int(parts[1]):02d}-{int(parts[2]):02d}"
    return None

def complete_draws(csv_file):
    df = pd.read_csv(csv_file, dtype=str)
    # Standardize and fix date values
    df['draw_date'] = df['date'].apply(fix_date_format)
    # Forward-fill missing dates using previous value + 7 days
    for i in range(1, len(df)):
        if pd.isnull(df.loc[i, 'draw_date']):
            prev_date = pd.to_datetime(df.loc[i-1, 'draw_date'])
            new_date = prev_date - pd.Timedelta(days=7)
            df.loc[i, 'draw_date'] = new_date.strftime('%Y-%m-%d')
    return df

def to_sql(df):
    lines = []
    lines.append("INSERT INTO draw (draw_date, lottery_id, numbers) VALUES")
    for _, row in df.iterrows():
        date = row['draw_date']
        lottery = row['lottery_id']
        numbers = [row['n1'], row['n2'], row['n3'], row['n4'], row['n5'], row['n6'], row['n7']]
        sql = f"('{date}', '{lottery}', ARRAY[{','.join(map(str, numbers))}]),"
        lines.append(sql)

    with open('../SQL_commands/draw_numbers_hu7a_SQL.sql', 'w') as f:
        f.write('\n'.join(lines))

if __name__ == '__main__':
    fixed_df = complete_draws('draw_numbers_hu7a.csv')
    del fixed_df['date']
    to_sql(fixed_df)
