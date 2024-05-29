import csv
from collections import defaultdict
from statistics import mean
from datetime import datetime

def calculate_mean_fee(input_filename, output_filename):
    # Dictionary to store data grouped by date
    data_by_date = defaultdict(list)

    # Read the input CSV file
    with open(input_filename, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            # Extract date from timestamp
            date = datetime.strptime(row['date'], '%Y-%m-%d %H:%M:%S').date()
            # Append data to the corresponding date
            data_by_date[date].append({
                'medianFee': float(row['medianFee']),
                'avgFeeRate': float(row['avgFeeRate'])
            })

    # Calculate mean values for each date
    mean_values_by_date = {}
    for date, data in data_by_date.items():
        mean_median_fee = mean(entry['medianFee'] for entry in data)
        mean_avg_fee_rate = mean(entry['avgFeeRate'] for entry in data)
        mean_values_by_date[date] = {
            'meanMedianFee': mean_median_fee,
            'meanAvgFeeRate': mean_avg_fee_rate
        }

    # Write mean values to output CSV file
    with open(output_filename, 'w', newline='') as csvfile:
        fieldnames = ['date', 'meanMedianFee', 'meanAvgFeeRate']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for date, mean_values in mean_values_by_date.items():
            writer.writerow({
                'date': date.strftime('%Y-%m-%d'),
                'meanMedianFee': round(mean_values['meanMedianFee'], 3),
                'meanAvgFeeRate': round(mean_values['meanAvgFeeRate'], 3)
            })

# Run the function
calculate_mean_fee('block_data.csv', 'mean_historic_fee.csv')
