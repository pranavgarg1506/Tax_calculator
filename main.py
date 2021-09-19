'''
author:- Pranav Garg
Date- 18-09-2021
'''

import pandas as pd
import numpy as np

class Person:

    def __init__(self) -> None:
        self.name = input("Please Enter your name: ")
        self.age = int(input("Please Enter your age: "))
        self.company = input("Please ENter your company: ")

    def enterInformation(self):
        self.components = ['Basic', 'HRA', 'LTA', 'City Allowance', 'Miscll', 'Non_Miscll', 'PF', 'Tax']
        self.tax_components = ['Basic', 'HRA', 'LTA', 'City Allowance', 'Miscll']


        ##  monthly salary
        self.months = {
            0 : 'April',
            1 : 'May',
            2 : 'June',
            3 : 'July',
            4 : 'August',
            5 : 'September',
            6 : 'October',
            7 : 'November',
            8 : 'December',
            9 : 'January',
            10 : 'Feburary',
            11 : 'March'
        }
        s_data = []
        for month in range(12):
            print("--------------",self.months[month],"--------------")
            temp = []
            for comp in self.components:
                q = "Please Enter the "+comp+": "
                var = int(input(q))
                temp.append(var)
            print('\n')
            s_data.append(temp)

            if month <= 10:
                ans = input('Do you have next Months Salary(Y/N)? ')
                if ans == 'N':
                    break
        rows = len(s_data)

        for i in range(rows, 12):
            s_data.append(s_data[rows-1])
                    
        self.salary = pd.DataFrame(data = s_data, columns=self.components, index=self.months.values())
        #print(self.salary)

        print("\n\nEnter Exemption Data----------------------------------------")
        self.ppf = int(input("Please Enter your contribution in PPF: "))
        self.life_insurance = int(input("Please Enter your contribution in Life Insurance: "))
        self.medical_premium = int(input("Please Enter your contribution in Medical Premium: "))
        self.lta_cliamed = int(input("Please Enter your Claimed LTA: "))
        self.hra_claimed = int(input("Please Enter your Claimed HRA: "))
        self.professional_tax = int(input("Please Enter Professional Tax Deducted: "))

    def caclulateOldRegimeTax(self):
        print("Calculating TAX via OLD TAX RATES----------------")
        figures = {}
        for col in self.salary:
            figures[col] = self.salary[col].sum()
    
        CTC = figures['Basic'] + figures['HRA'] + figures['LTA'] + figures['City Allowance'] + figures['Miscll'] + figures['Non_Miscll']

        print("TOTAL CTC", CTC)

        total = CTC - figures['Non_Miscll']

        print("\n\nDEDUCTIONS.................................\n")

        ## LTA DEDUCTIONS
        print("TOTAL LTA CLAIMED YET:-",self.lta_cliamed)

        ## HRA DEDUCTIONS
        print("TOTAL HRA USED YET:-",self.hra_claimed)

        ## 80C
        self.E_80C = self.ppf + self.life_insurance + figures['PF']
        print("TOTAL 80C USED YET:-",self.E_80C)

        ## 80D
        self.E_80D = self.medical_premium
        print("TOTAL 80D USED YET:-",self.E_80D)

        ## sec 16 Deductions
        self.E_16 = 50000 + self.professional_tax
        print("DEDUCTION UNDER SEC 16:-",self.E_16)

        ## GROSS TAXABLE SALARY
        tax_salary = total - self.lta_cliamed - self.hra_claimed - min(150000, self.E_80C) - self.E_80D - self.E_16
        print("\n\nGROSS TAXAXBLE SALARY",tax_salary)

        ## tax has to be paid
        tax = 0
        if tax_salary <= 250000:
            tax = 0
        elif 250000 < tax_salary and tax_salary <= 500000:
            temp = tax_salary - 250000
            ans = 0.05 * temp
            ax += ans
        elif 500000 < tax_salary and tax_salary <= 1000000:
            temp = tax_salary - 500000
            tax += 12500
            ans = 0.20 * temp
            tax += ans
        elif 1000000 < tax_salary:
            temp = tax_salary - 1000000
            tax += 112500
            ans = 0.30 * temp
            tax += ans

        tax = tax * 1.04
        tax = round(tax,2)
        print("TOTAL TAX TO BE PAID", tax)
        print("TOTAL TAX PAID YET", figures['Tax'])
        print("REMAINING TAX", round(tax - figures['Tax'],2))

    def printDashboard(self):
        print("Name of the Tax Payer",self.name)
        print("Age of the Tax Payer",self.age)
        print("Company of the Tax Payer",self.company)

        print("--------------SALARY BREAKDOWN ---------------")
        print(self.salary)
        print("\nTotal Components: ", self.components)
        print("\nTotal Taxable Components: ", self.tax_components)



    def main(self):
        self.enterInformation()
        self.printDashboard()
        self.caclulateOldRegimeTax()

    

p = Person()
p.main()