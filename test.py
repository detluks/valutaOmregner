import csv
dicdic = {}
codes = []
data = ["code","desc","rate"]
for i in range(3):
            filePath = f"saves/{"2026-01-05"}/{data[i]}"
            with open(filePath, newline="", encoding="utf-8") as f:
                reader = csv.reader(f)
                if i == 0:
                    for row in reader:
                        dicdic[",".join(row)] = {'desc':'','rate':''}
                        codes.append(",".join(row))
                    print(dicdic)
                else:
                    k = 0
                    if data[i]=="rate":
                        for row in reader:
                            dicdic[codes[k]][data[i]] = float(",".join(row))
                            k+=1
                    else:
                        for row in reader:
                            dicdic[codes[k]][data[i]] = ",".join(row)
                            k+=1
dicdic["DKK"]={'desc':"Danske kroner", 'rate': 100}
print (dicdic)