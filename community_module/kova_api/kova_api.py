from pprint import pprint

import requests


class KovaAPI:
    def __init__(self, env):
        self.env = env
        self.api_url = "https://c03-usa-east.integrate-test.boomi.com/ws/simple/createCommunities"
        self.token = self.env['ir.config_parameter'].sudo().get_param('module_sb.kova_api_token')

    def create_community_kova(self, community):
        return 0 # will be removed later
        headers = {
            'Authorization': f'Basic {self.token}',
            'Content-Type': 'application/json'
        }

        community_franchisee = community.create_uid.company_id.read(['name', 'kova_bunit_rid', 'description'])[0]
        payload = {
            "FranchiseeBUnitRID": 401,
            "BUnitID": str(community_franchisee['kova_bunit_rid']) if community_franchisee['kova_bunit_rid'] else "0",
            "BUnit_Name": community_franchisee['name'] if community_franchisee['name'] else "",
            "BUnit_Description": community_franchisee['description'] if community_franchisee['description'] else "",
            "CommunityID": str(community.id),
            "Community_Name": community.legal_name if community.legal_name else "",
            "Community_Description": community.description if community.description else "",
            "MarketingName": community.display_name if community.display_name else "",
            "EnabledAPILevels": "1,2,3,4",
            "EnabledCache": True
        }

        try:
            response = requests.post(self.api_url, json=payload, headers=headers)
            if response.status_code == 200:
                response_data = response.json()
                if response_data['CommunityRID']:
                    return response_data['CommunityRID']

            return 0
        except requests.exceptions.RequestException as e:
            return 0
