import csv
import os
terminal_start_command  = "start python" if os.name == 'nt' else "gnome-terminal -x"
with open('GAP_trained_verified_variants.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            print(row[0])
            if (row[0]=="Failed"):
                print("skipping failed variant")
            else:    
                os.system(terminal_start_command+" python skill_model_generate_with_csv.py "+" ".join(row[0][1:-1].split(", "))+" "+row[1])