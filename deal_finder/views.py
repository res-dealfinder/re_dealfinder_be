from django.http import HttpResponse
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from bson.json_util import dumps #convert cursor to json
from bson.objectid import ObjectId
from .models import property_collection


from .property_evaluation.calculators import *

@api_view()
def property_list(request):
    properties = property_collection.find().limit(10)
    properties_list = []
    for property in properties:
        property_base = property.get("data").get("base")
        property_data = {
            ID: (str(property.get("_id"))),
            STREET: property_base.get('location').get('address').get('line'),
            CITY: property_base.get('location').get('address').get('city'),
            ZIP_CODE: property_base.get('location').get('address').get('postal_code'),
            ONLINE_LINK: property_base.get('href'),
            YEAR_BUILT: property_base.get('description').get('year_built'),
            ASKING_PRICE: property_base.get('list_price'),
            OFFER_PRICE: property_base.get('list_price'),
            INFO: property_base.get('description').get('text'),
            DOWN_PAYMENT_PERCENTAGE: 30,
            RENOVATIONS: 0,
            CLOSING_COST: 0,
            INTEREST_RATE: property_base.get('mortgage').get('estimate').get("average_rate").get("rate"),
            YEARS: property_base.get('mortgage').get('estimate').get("average_rate").get("loan_type").get("term"),
            PROPERTY_TAX_RATE: property_base.get('mortgage').get('property_tax_rate'),
            PROPERTY_SQFT: property_base.get('description').get('sqft'), 
            LOT_SQFT: property_base.get('description').get('lot_sqft'),
            SECTION_8: False,
            LEASE: False,
            DISCLOSURE_OR_INSPECTIONS: False,
        }
        property_data = PropertyEvaluation(property_data)
        property_data.cal_down_payment()
        property_data.cal_loan_amount()
        property_data.cal_down_payment()
        property_data.cal_total_cost()
        property_data.cal_loan_amount()
        property_data.cal_monthly_mortgage()
        property_data.cal_monthly_property_tax()
        property_data.add_monthly_insurance(600)
        property_data.add_monthly_utilities(300)
        property_data.add_monthly_fees(0)
        property_data.cal_total_monthly_cost()
        property_data.add_actual_monthly_rental_income(3600)
        property_data.cal_actual_net()
        property_data.cal_actual_annual_net()
        property_data.cal_actual_ROI()
        property_data.cal_actual_DCSR()
        property_data.cal_actual_income_over_debt()
        property_data.cal_actual_cap_rate()
        property_data.add_projected_monthly_rental_income(6280)
        property_data.cal_project_net()
        property_data.cal_projected_annual_net()
        property_data.cal_projected_ROI()
        property_data.cal_projected_DCSR()
        property_data.cal_projected_income_over_debt()
        property_data.cal_projected_cap_rate()
        property_data.cal_years_until_maxed_rents()

        properties_list.append(property_data.property)

    return Response(properties_list)

@api_view()
def property_detail(request, id):
    property = property_collection.find({"_id": ObjectId(id)})
    property_base = property[0].get("data").get("base")

    property_data = {
        STREET: property_base.get('location').get('address').get('line'),
        CITY: property_base.get('location').get('address').get('city'),
        ZIP_CODE: property_base.get('location').get('address').get('postal_code'),
        ONLINE_LINK: property_base.get('href'),
        YEAR_BUILT: property_base.get('description').get('year_built'),
        ASKING_PRICE: property_base.get('list_price'),
        OFFER_PRICE: property_base.get('list_price'),
        INFO: property_base.get('description').get('text'),
        DOWN_PAYMENT_PERCENTAGE: 30,
        RENOVATIONS: 0,
        CLOSING_COST: 0,
        INTEREST_RATE: property_base.get('mortgage').get('estimate').get("average_rate").get("rate"),
        YEARS: property_base.get('mortgage').get('estimate').get("average_rate").get("loan_type").get("term"),
        PROPERTY_TAX_RATE: property_base.get('mortgage').get('property_tax_rate'),
        PROPERTY_SQFT: property_base.get('description').get('sqft'), 
        LOT_SQFT: property_base.get('description').get('lot_sqft'),
        SECTION_8: False,
        LEASE: False,
        DISCLOSURE_OR_INSPECTIONS: False,
    }

    property_data = PropertyEvaluation(property_data)
    property_data.cal_down_payment()
    property_data.cal_loan_amount()
    property_data.cal_down_payment()
    property_data.cal_total_cost()
    property_data.cal_loan_amount()
    property_data.cal_monthly_mortgage()
    property_data.cal_monthly_property_tax()
    property_data.add_monthly_insurance(600)
    property_data.add_monthly_utilities(300)
    property_data.add_monthly_fees(0)
    property_data.cal_total_monthly_cost()
    property_data.add_actual_monthly_rental_income(3600)
    property_data.cal_actual_net()
    property_data.cal_actual_annual_net()
    property_data.cal_actual_ROI()
    property_data.cal_actual_DCSR()
    property_data.cal_actual_income_over_debt()
    property_data.cal_actual_cap_rate()
    property_data.add_projected_monthly_rental_income(6280)
    property_data.cal_project_net()
    property_data.cal_projected_annual_net()
    property_data.cal_projected_ROI()
    property_data.cal_projected_DCSR()
    property_data.cal_projected_income_over_debt()
    property_data.cal_projected_cap_rate()
    property_data.cal_years_until_maxed_rents()
    
    # print("Property_data: ",property_data)
    # hashMap = {
    #     "name": "Luan",
    #     "add": "2000 Fords"
    # }
    return Response(property_data.property)