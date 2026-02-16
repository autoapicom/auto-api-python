"""
Auto API Python Client — Complete usage example.

Replace 'your-api-key' with your actual API key from https://auto-api.com

Run: python example.py
"""

from auto_api import Client, AuthError, ApiError

client = Client('your-api-key', 'https://api1.auto-api.com')
source = 'encar'

# --- Get available filters ---

filters = client.get_filters(source)

print('Available brands:')
for brand in filters['mark']:
    print(f'  - {brand}')

print(f"\nTransmission types: {', '.join(filters['transmission_type'])}")
print(f"Body types: {', '.join(filters['body_type'])}")

# --- Search offers with filters ---

offers = client.get_offers(source, page=1, brand='Hyundai', year_from=2020, price_to=50000)

print(f"\n--- Offers (page {offers['meta']['page']}) ---")
for item in offers['result']:
    d = item['data']
    print(f"{d['mark']} {d['model']} {d['year']} — ${d['price']} ({d['km_age']} km)")

# Pagination
if offers['meta'].get('next_page'):
    next_page = client.get_offers(source, page=offers['meta']['next_page'], brand='Hyundai', year_from=2020)
    print(f"Next page has {len(next_page['result'])} offers")

# --- Get single offer ---

inner_id = offers['result'][0]['inner_id'] if offers['result'] else '40427050'
offer = client.get_offer(source, inner_id)

print('\n--- Single offer ---')
print(f"URL: {offer['data']['url']}")
print(f"Seller: {offer['data']['seller_type']}")
print(f"Images: {len(offer['data']['images'])}")

# --- Track changes ---

change_id = client.get_change_id(source, '2025-01-15')
print(f'\n--- Changes from 2025-01-15 (change_id: {change_id}) ---')

changes = client.get_changes(source, change_id)
for change in changes['result']:
    print(f"[{change['change_type']}] {change['inner_id']}")

# Fetch next batch
if changes['meta'].get('next_change_id'):
    more_changes = client.get_changes(source, changes['meta']['next_change_id'])
    print(f"Next batch: {len(more_changes['result'])} changes")

# --- Get offer by URL ---

info = client.get_offer_by_url('https://www.encar.com/dc/dc_cardetailview.do?carid=40427050')
print(f"\n--- Offer by URL ---")
print(f"{info['mark']} {info['model']} {info['year']} — ${info['price']}")

# --- Error handling ---

try:
    bad_client = Client('invalid-key', 'https://api1.auto-api.com')
    bad_client.get_offers('encar', page=1)
except AuthError as e:
    print(f'\nAuth error: {e.message} (HTTP {e.status_code})')
except ApiError as e:
    print(f'\nAPI error: {e.message} (HTTP {e.status_code})')
