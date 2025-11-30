import json
from pathlib import Path
from datacommons_client import DataCommonsClient

def get_ca_county_income():
    client = DataCommonsClient(api_key="AIzaSyCTI4Xz-UW_G2Q2RfknhcfdAnTHq5X5XuI") # Trial API key

    df = client.observations_dataframe(
        variable_dcids=["Median_Income_Household"],
        parent_entity="geoId/06", # California
        entity_type="County",
        date="latest"
    )

    print(f"Found {len(df)} entries.")

    results = []
    seen_counties = set()
    
    for _, row in df.iterrows():
        if row.get('entity_name') not in seen_counties:
            results.append({
                "County": row.get('entity_name').replace(' County', ''),
                "Median Household Income": row.get('value'),
            })
        seen_counties.add(row.get('entity_name'))

    output_file = Path(__file__).parent.parent / 'data' / 'ca_county_median_income.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=4)

if __name__ == "__main__":
    get_ca_county_income()