import csv


with open("testo.txt", 'w') as file:

    writer = csv.writer(file)
    writer.writerow(["Prova", "altra prova"])
    #file.write("Questa è una prova")