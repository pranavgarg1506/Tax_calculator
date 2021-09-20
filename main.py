'''
author:- Pranav Garg
Date- 18-09-2021
'''

import pandas as pd
from pandas.core.reshape import reshape
import numpy as np

class Person:

    def __init__(self) -> None:
        self.name = input("Please Enter your name: ")
        self.age = int(input("Please Enter your age: "))
        self.company = input("Please ENter your company: ")
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

    def enterInformation(self):
        
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
        self.life_insurance = int(input("Please Enter your contribution in Life Insurance(80C): "))
        self.medical_premium = int(input("Please Enter your contribution in Medical Premium(80D): "))
        self.lta_cliamed = int(input("Please Enter your Claimed LTA: "))
        self.hra_claimed = int(input("Please Enter your Claimed HRA: "))
        self.professional_tax = int(input("Please Enter Professional Tax Deducted: "))

    def downloadExcelSheet(self):
        components = ['Basic', 'HRA', 'LTA', 'City Allowance', 'Miscll', 'Non_Miscll', 'PF', 'Tax']
        df = pd.DataFrame(columns=components)
        df.to_csv('Salary_breakdown.csv', index=False)

    def processcsvSheet(self):
        print("Processing the Salary BreakDown Sheet into the System....")
        df = pd.read_csv('Salary_breakdown.csv')
        #print(df)

        s_data = df.values.tolist()
        rows = len(s_data)

        for i in range(rows, 12):
            s_data.append(s_data[rows-1])
                    
        self.salary = pd.DataFrame(data = s_data, columns=self.components, index=self.months.values())
        #print(self.salary)

        print("\n\nEnter Exemption Data----------------------------------------")
        self.ppf = int(input("Please Enter your contribution in PPF: "))
        self.life_insurance = int(input("Please Enter your contribution in Life Insurance(80C): "))
        self.medical_premium = int(input("Please Enter your contribution in Medical Premium(80D): "))
        self.lta_cliamed = int(input("Please Enter your Claimed LTA: "))
        self.hra_claimed = int(input("Please Enter your Claimed HRA: "))
        self.professional_tax = int(input("Please Enter Professional Tax Deducted: "))

    def caclulateOldRegimeTax(self):
        print("Calculating TAX via OLD TAX RATES----------------")
        figures = {}
        for col in self.salary:
            figures[col] = self.salary[col].sum()

        tax_dict = {}
        CTC = figures['Basic'] + figures['HRA'] + figures['LTA'] + figures['City Allowance'] + figures['Miscll'] + figures['Non_Miscll']

        print("TOTAL CTC", CTC)
        tax_dict['Total CTC'] = CTC

        total = CTC - figures['Non_Miscll']
        tax_dict['Taxable_Salary'] = total

        print("\n\nDEDUCTIONS.................................\n")

        ## LTA DEDUCTIONS
        print("TOTAL LTA CLAIMED YET:-",self.lta_cliamed)
        tax_dict['LTA CLAIMED'] = self.lta_cliamed

        ## HRA DEDUCTIONS
        print("TOTAL HRA USED YET:-",self.hra_claimed)
        tax_dict['HRA CLAIMED'] = self.hra_claimed

        ## 80C
        self.E_80C = self.ppf + self.life_insurance + figures['PF']
        print("TOTAL 80C USED YET:-",self.E_80C)
        tax_dict['80C Deduction'] = self.E_80C

        ## 80D
        self.E_80D = self.medical_premium
        print("TOTAL 80D USED YET:-",self.E_80D)
        tax_dict['80D Deduction'] = self.E_80D

        ## sec 16 Deductions
        self.E_16 = 50000 + self.professional_tax
        print("DEDUCTION UNDER SEC 16:-",self.E_16)
        tax_dict['Section 16 Deduction'] = self.E_16

        ## GROSS TAXABLE SALARY
        tax_salary = total - self.lta_cliamed - self.hra_claimed - min(150000, self.E_80C) - self.E_80D - self.E_16
        print("\n\nGROSS TAXAXBLE SALARY",tax_salary)
        tax_dict['GROSS TAXAXBLE SALARY'] = tax_salary

        ## tax has to be paid
        tax = 0
        if tax_salary <= 250000:
            tax = 0
        elif 250000 < tax_salary and tax_salary <= 500000:
            temp = tax_salary - 250000
            ans = 0.05 * temp
            tax += ans
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
        tax_dict['TOTAL TAX TO BE PAID'] = tax
        tax_dict['TOTAL TAX PAID YET'] = figures['Tax']
        tax_dict['REMAINING TAX'] = round(tax - figures['Tax'],2)

        ## Downloading the EXCEL SHeet with the TAX INFORMATION
        file_name = 'Salary_Breakdown_'+self.name+'.csv'
        self.salary.to_csv(file_name)
        print("Salary BreakDown file for "+self.name+" is downoaded SUCCESSFULLY")

        file_name = 'TAX_INFORMATION_'+self.name+'.csv'
        df11 = pd.DataFrame(list(tax_dict.items()))
        df11.to_csv(file_name,index=False,header=False)
        print("TAX INFORMATION file for "+self.name+" is downoaded SUCCESSFULLY")





    def printDashboard(self):
        print("Name of the Tax Payer",self.name)
        print("Age of the Tax Payer",self.age)
        print("Company of the Tax Payer",self.company)

        print("--------------SALARY BREAKDOWN ---------------")
        print(self.salary)
        print("\nTotal Components: ", self.components)
        print("\nTotal Taxable Components: ", self.tax_components)

    def main(self):
        print("What do you want to do?")
        print("1. Enter the informtation via program")
        print("2. Enter data in the excel sheet and then process the data")
        response = int(input("Enter your response  "))
        if response == 1:
            self.enterInformation()
        elif response == 2:
            res1 = input("Do you want to download the empty excel sheet(y/n)  ")
            if res1.lower() == 'y':
                print("\nDownloading Empty Salary BreakDown Sheet......")
                self.downloadExcelSheet()
                print("File is Downloaded Successfully...")
                return
            self.processcsvSheet()
            
        self.printDashboard()
        self.caclulateOldRegimeTax()

    
p = Person()
p.main()