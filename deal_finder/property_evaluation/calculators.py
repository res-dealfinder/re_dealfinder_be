from math import log10

# Define constants for dictionary keys
ID = 'id'
STREET = 'street'
CITY = 'city'
ZIP_CODE = 'zip_code'
ONLINE_LINK = 'online_link'
YEAR_BUILT = 'year_built'
ASKING_PRICE = 'asking_price'
OFFER_PRICE = 'offer_price'
INFO = 'info'
DOWN_PAYMENT_PERCENTAGE = 'down_payment_percentage'
RENOVATIONS = 'renovations'
CLOSING_COST = 'closing_cost'
INTEREST_RATE = 'interest_rate'
YEARS = 'years'
PROPERTY_TAX_RATE = 'property_tax_rate'
PROPERTY_SQFT = 'property_sqft'
LOT_SQFT = 'lot_sqft'
SECTION_8 = 'section8'
LEASE = 'lease'
DISCLOSURE_OR_INSPECTIONS = 'disclosure_or_inspections'

DOWN_PAYMENT ='down_payment'
TOTAL_COST = 'total_cost'
LOAN_AMOUNT = 'loan_amount'
MONTHLY_MORTGAGE = 'monthly_mortgage'
MONTHLY_PROPERTY_TAX = 'monthly_property_taxes'
MONTHLY_INSURANCE = 'monthly_insurance'
MONTHLY_UTILITIES = 'monthly_utilities'
MONTHLY_FEES = 'monthly_fees'
TOTAL_MONTHLY_COST = 'total_monthly_cost'
ACTUAL_MONTHLY_RENTAL_INCOME = 'actual_monthly_rental_income'
ACTUAL_NET = 'actual_net'
ACTUAL_ANNUAL_NET = 'actual_annual_net'
ACTUAL_ROI = 'actual_roi'
ACTUAL_DCSR = 'actual_dcsr'
ACTUAL_INCOME_OVER_DEBT = 'actual_income_over_debt'
ACTUAL_CAP_RATE = 'actual_cap_rate'
PROJECTED_MONTHLY_RENTAL_INCOME = 'projected_monthly_rental_income'
PROJECT_NET = 'project_net'
PROJECTED_ANNUAL_NET = 'projected_annual_net'
PROJECTED_ROI = 'projected_roi'
PROJECTED_DCSR = 'projected_dcsr'
PROJECTED_INCOME_OVER_DEBT = 'projected_income_over_debt'
PROJECTED_CAP_RATE = 'projected_cap_rate'
YEARS_UNTIL_MAXED_RENTS = 'years_until_maxed_rents'

RENT_CONTROL_INCREASE_PER_YEAR = 0.08

class PropertyEvaluation:
    def __init__(self, property_data: dict):
        self.property = property_data
    def cal_down_payment(self):
        try:
            if not isinstance(self.property[OFFER_PRICE], (int, float)) or not isinstance(self.property[DOWN_PAYMENT_PERCENTAGE], (int, float)):
                raise TypeError("Both offer_price and down_payment_percentage must be numbers.")
            
            if self.property[OFFER_PRICE] < 0 or self.property[DOWN_PAYMENT_PERCENTAGE] < 0:
                raise ValueError("Both offer_price and down_payment_percentage must be non-negative.")

            down_payment = self.property[OFFER_PRICE] * (self.property[DOWN_PAYMENT_PERCENTAGE] / 100)
            self.property[DOWN_PAYMENT] = down_payment
            return down_payment

        except TypeError as e:
            print(f"Type Error: {e}")
        except ValueError as e:
            print(f"Value Error: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

    def cal_total_cost(self):
        total_cost = self.property[RENOVATIONS] + self.property[CLOSING_COST] + self.property[DOWN_PAYMENT]
        self.property[TOTAL_COST] = total_cost
        return total_cost

    def cal_loan_amount(self):
        loan_amount = self.property[OFFER_PRICE] - self.property[DOWN_PAYMENT]
        self.property[LOAN_AMOUNT] = loan_amount
        return loan_amount
    
    def cal_monthly_mortgage(self):
        monthly_mortgage = ((self.property[INTEREST_RATE]/1200) + (self.property[INTEREST_RATE]/1200) / ((1+(self.property[INTEREST_RATE]/1200))**(self.property[YEARS]*12)-1))*self.property[LOAN_AMOUNT]
        monthly_mortgage = round(monthly_mortgage, 2)
        self.property[MONTHLY_MORTGAGE] = monthly_mortgage
        return monthly_mortgage

    def cal_monthly_property_tax(self):
        monthly_property_tax = round(self.property[OFFER_PRICE]*self.property[PROPERTY_TAX_RATE]/12,2)
        self.property[MONTHLY_PROPERTY_TAX] = monthly_property_tax
        return monthly_property_tax
    
    def add_monthly_insurance(self, monthly_insurance):
        self.property[MONTHLY_INSURANCE] = monthly_insurance
        return monthly_insurance
    
    def add_monthly_utilities(self, monthly_utilities):
        self.property[MONTHLY_UTILITIES] = monthly_utilities
        return monthly_utilities
    
    def add_monthly_fees(self, monthly_fees):
        self.property[MONTHLY_FEES] = monthly_fees
        return monthly_fees
    
    def cal_total_monthly_cost(self):
        total_monthly_cost =round(self.property[MONTHLY_MORTGAGE] + self.property[MONTHLY_PROPERTY_TAX] + self.property[MONTHLY_INSURANCE] + self.property[MONTHLY_UTILITIES] + self.property[MONTHLY_FEES],2)
        self.property[TOTAL_MONTHLY_COST] = total_monthly_cost
        return total_monthly_cost
    
    def add_actual_monthly_rental_income(self, actual_monthly_rental_income):
        self.property[ACTUAL_MONTHLY_RENTAL_INCOME] = actual_monthly_rental_income
        return actual_monthly_rental_income
    
    def cal_actual_net(self):
        actual_net = round(self.property[ACTUAL_MONTHLY_RENTAL_INCOME] - self.property[TOTAL_MONTHLY_COST], 2)
        self.property[ACTUAL_NET] = actual_net
        return actual_net
    
    def cal_actual_annual_net(self):
        actual_annual_net = round(self.property[ACTUAL_NET] * 12, 2)
        self.property[ACTUAL_ANNUAL_NET] = actual_annual_net
        return actual_annual_net
    
    def cal_actual_ROI(self):
        actual_ROI = round(self.property[ACTUAL_NET]/self.property[TOTAL_COST]*1000,2)
        self.property[ACTUAL_ROI] = actual_ROI
        return actual_ROI
    
    def cal_actual_DCSR(self):
        actual_DCSR = round((self.property[ACTUAL_MONTHLY_RENTAL_INCOME] - (self.property[MONTHLY_PROPERTY_TAX] + self.property[MONTHLY_INSURANCE] + self.property[MONTHLY_FEES]+self.property[MONTHLY_UTILITIES])) / self.property[MONTHLY_MORTGAGE],2)
        self.property[ACTUAL_DCSR] = actual_DCSR
        return actual_DCSR
    
    def cal_actual_income_over_debt(self):
        actual_income_over_debt = round(self.property[ACTUAL_MONTHLY_RENTAL_INCOME] / self.property[TOTAL_MONTHLY_COST], 2)
        self.property[ACTUAL_INCOME_OVER_DEBT] = actual_income_over_debt
        return actual_income_over_debt
    
    def cal_actual_cap_rate(self):
        cal_actual_cap_rate = round(self.property[ACTUAL_ANNUAL_NET] / self.property[ASKING_PRICE] * 100, 2)
        self.property[ACTUAL_CAP_RATE] = cal_actual_cap_rate
        return cal_actual_cap_rate
    
    def add_projected_monthly_rental_income(self, projected_monthly_rental_income):
        self.property[PROJECTED_MONTHLY_RENTAL_INCOME] = projected_monthly_rental_income
        return projected_monthly_rental_income
    
    def cal_project_net(self):
        project_net = self.property[PROJECTED_MONTHLY_RENTAL_INCOME] - self.property[TOTAL_MONTHLY_COST]
        self.property[PROJECT_NET] = project_net
        return project_net
    
    def cal_projected_annual_net(self):
        cal_projected_annual_net = round(self.property[PROJECT_NET] * 12, 2)
        self.property[PROJECTED_ANNUAL_NET] = cal_projected_annual_net
        return cal_projected_annual_net
    
    def cal_projected_ROI(self):
        projected_ROI = round(self.property[PROJECT_NET] / self.property[TOTAL_COST] * 1000, 2)
        self.property[PROJECTED_ROI] = projected_ROI
        return projected_ROI
    
    def cal_projected_DCSR(self):
        projected_DCSR = round((self.property[PROJECTED_MONTHLY_RENTAL_INCOME] - (self.property[MONTHLY_PROPERTY_TAX] + self.property[MONTHLY_INSURANCE] + self.property[MONTHLY_UTILITIES] + self.property[MONTHLY_FEES])) / self.property[MONTHLY_MORTGAGE],2)
        self.property[PROJECTED_DCSR] = projected_DCSR
        return projected_DCSR
    
    def cal_projected_income_over_debt(self):
        projected_income_over_debt = round(self.property[PROJECTED_MONTHLY_RENTAL_INCOME] / self.property[TOTAL_MONTHLY_COST] ,2)
        self.property[PROJECTED_INCOME_OVER_DEBT] = projected_income_over_debt
        return projected_income_over_debt
    
    def cal_projected_cap_rate(self):
        projected_cap_rate = round(self.property[PROJECTED_ANNUAL_NET] / self.property[ASKING_PRICE] * 100 ,2)
        self.property[PROJECTED_CAP_RATE] = projected_cap_rate
        return projected_cap_rate
    
    def cal_years_until_maxed_rents(self):
        years_until_maxed_rents = round(log10(self.property[PROJECTED_MONTHLY_RENTAL_INCOME]/self.property[ACTUAL_MONTHLY_RENTAL_INCOME])/log10(1+ RENT_CONTROL_INCREASE_PER_YEAR),2)
        self.property[YEARS_UNTIL_MAXED_RENTS] = years_until_maxed_rents
        return years_until_maxed_rents
    
    # round( ,2)
# self.property[]
# Create a dictionary with the defined constants
property_data = {
    STREET: '7562 24th st',
    CITY: 'Sacramento',
    ZIP_CODE: '95822',
    ONLINE_LINK: 'https://www.realtor.com/realestateandhomes-detail/7562-24th-St_Sacramento_CA_95822_M24603-85219',
    YEAR_BUILT: 1965,
    ASKING_PRICE: 560000,
    OFFER_PRICE: 560000,
    INFO: 'Beautifully renovated home near the city center.',
    DOWN_PAYMENT_PERCENTAGE: 30,
    RENOVATIONS: 10000,
    CLOSING_COST: 5000,
    INTEREST_RATE: 4.5,
    YEARS: 30,
    PROPERTY_TAX_RATE: 0.0126,
    PROPERTY_SQFT: 1500, 
    LOT_SQFT: 7500,
    SECTION_8: False,
    LEASE: False,
    DISCLOSURE_OR_INSPECTIONS: False,
}

#testing example using row 4 on Property Evaluations sheet
# test = PropertyEvaluation(property_data)
# print("down_payment: ", test.cal_down_payment())
# print("total_cost: ", test.cal_total_cost())
# print("loan_amount: ", test.cal_loan_amount())
# print("monthly_mortgage: ", test.cal_monthly_mortgage())
# print("monthly_property_tax: ", test.cal_monthly_property_tax())
# print("monthly_insurance: ", test.add_monthly_insurance(600))
# print("monthly_utilities: ", test.add_monthly_utilities(300))
# print("monthly_fees: ", test.add_monthly_fees(0))
# print("total_monthly_cost: ", test.cal_total_monthly_cost())
# print("actual_monthly_rental_income: ", test.add_actual_monthly_rental_income(3600))
# print("actual_net: ", test.cal_actual_net())
# print("actual_annual_net: ", test.cal_actual_annual_net())
# print("actual_ROI: ", test.cal_actual_ROI())
# print("actual_DCSR: ", test.cal_actual_DCSR())
# print("cal_actual_income_over_debt: ", test.cal_actual_income_over_debt())
# print("cal_actual_cap_rate: ", test.cal_actual_cap_rate())
# print("add_projected_monthly_rental_income: ", test.add_projected_monthly_rental_income(6280))
# print("cal_project_net: ", test.cal_project_net())
# print("cal_projected_annual_net: ", test.cal_projected_annual_net())
# print("cal_projected_ROI: ", test.cal_projected_ROI())
# print("cal_projected_DCSR: ", test.cal_projected_DCSR())
# print("cal_projected_income_over_debt: ", test.cal_projected_income_over_debt())
# print("cal_projected_cap_rate: ", test.cal_projected_cap_rate())
# print("cal_years_until_maxed_rents: ", test.cal_years_until_maxed_rents())

# for key, value in test.property.items():
#     print(f"{key} : {value}")