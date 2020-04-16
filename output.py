import csv

def writeCSV(list):
    RowList = ["Number of Observation", "Time of Year", "Density of Observations",
                "Standard Deviation of Denstiy of Observations",
                "Average Canopy Height", "Standard Deviation of Canopy Height", "Data Quality", "Classify Forest Types",
                "Raw Data"]

    try:
        with open("result.csv", 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(RowList)
            writer.writerow(list)
    except IOError:
        print("I/O error")