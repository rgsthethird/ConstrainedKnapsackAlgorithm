from openpyxl import Workbook
from openpyxl import load_workbook
from optimizer import Optimizer

def main():
    # Preps Excel file
    excelFile = input("Excel file for output: ")
    if not excelFile.endswith(".xlsx") or not excelFile.endswith(".xls"):
        excelFile += ".xlsx"
    wb = Workbook()
    ws = wb.active

    # Creates optimizer instance and solves optimal lineup
    opt = Optimizer()
    opt.optimize()
    bestScore = opt.getTopScore()
    finalMatrixSet = opt.getKnapsack()
    capStats = opt.getCapStats()
    opt.cementCaptain()
    lineup = opt.findPlayers(finalMatrixSet)

    # Prints best score, price, captain, lineup
    print("Best score: ",bestScore)
    print("Price: ","$"+str(lineup[1]*100))
    print("Captain: ",capStats[0])
    print("Lineup: ",lineup[0])

    # Preps Excel file
    matrixNum = 0
    for matrix in finalMatrixSet:
        header = [matrixNum]
        for col in range(len(matrix[0])):
            header.append(col)
        ws.append(header)
        rowNum = 0
        for row in matrix:
            playerRow = [rowNum]
            for w in row:
                wStr = "["+str(w[0])+", "+str(w[1])+"]"
                playerRow.append(wStr)
            ws.append(playerRow)
            rowNum += 1
        ws.append([])
        matrixNum += 1
    # Saves Excel file. Ends program.
    wb.save(excelFile)

if __name__ == "__main__":
    main()
