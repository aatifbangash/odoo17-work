from pprint import pprint

import requests
import re


class KovaAPI:
    def __init__(self, env):
        self.env = env
        self.api_url = "https://c03-usa-east.integrate-test.boomi.com/ws/simple"
        self.token = self.env['ir.config_parameter'].sudo().get_param('module_sb.kova_api_token')

    def create_franchisee_kova(self, company):
        endpoint = self.api_url + "/createBUnit"
        headers = {
            'Authorization': f'Basic {self.token}',
            'Content-Type': 'application/json'
        }

        franchisor = self.env['res.company']._get_main_company()

        payload = {
            "ParentRID": franchisor.kova_bunit_rid if franchisor.kova_bunit_rid else 342,
            "BUnitLevelRID": 3,  # will be setting
            "BUnitID": self.generate_bunit_id(company.name),
            "Name": company.name if company.name else '',
            "Description": company.description if company.description else '',
            "LegalName": company.legal_name if company.legal_name else '',
            "SelectionListName": company.name if company.name else '',
            "EnableInWeb": True
        }

        try:
            response = requests.post(endpoint, json=payload, headers=headers)
            if response.status_code == 200:
                response_data = response.json()
                if response_data['BUnitRID']:
                    return response_data['BUnitRID']

            return 0
        except requests.exceptions.RequestException as e:
            return 0

    def generate_bunit_id(self, name):
        name = re.sub(r'\s+', ' ', name).strip()
        name = name.replace(" ", "_")
        name = name.upper()
        name = re.sub(r'[^A-Z0-9_]', '', name)
        return name[:10]
