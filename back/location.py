import requests
import dotenv
import os

# Load environment variables
dotenv.load_dotenv()


def get_access_token():
    url = "https://api.orange.com/oauth/v3/token"
    payload = {
        "grant_type": "client_credentials"
    }
    headers = {
        "Authorization": os.getenv("ORANGE_AUTH_HEADER")
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    return response.json()["access_token"]


def retrieve_location(phone_number):
    '''
    Get latitude and longitude of a phone number
    '''
    url = "https://api.orange.com/camara/location-retrieval/orange-lab/v0/retrieve"
    headers = {
        "Authorization": f"Bearer {get_access_token()}",
        "Cache-Control": "no-cache",
        "accept": "application/json",
        "Content-Type": "application/json"
    }
    data = {
        "device": {
            "phoneNumber": phone_number
        },
        "maxAge": 60
    }

    response = requests.post(url, headers=headers, json=data)
    return response.json()['area']['center']


def reverse_geocoding(lat, lon):
    API_KEY = os.getenv('LOCATIONIQ_API_KEY')
    url = f"https://us1.locationiq.com/v1/reverse?key={
        API_KEY}&lat={lat}&lon={lon}&format=json&"

    response = requests.get(url)
    response = response.json()['address']
    city = response['city'] if 'city' in response else response['town']
    country = response['country']
    return {"location":
            {"city": city, "country": country}
            }

# Example usage:
# phone_number = "+33699901036"
# location_data = retrieve_location(phone_number)
# print(location_data)


def enhance_with_location_data(data):
    '''
    Takes a JSON object and adds location data to it
    '''
    data = data.copy()
    phone_number = data['phone_number']
    location_data = retrieve_location(phone_number)
    data['location'] = reverse_geocoding(lon=location_data['longitude'], lat=location_data['latitude'])
    return data


if __name__ == '__main__':
    phone_number = "+33699901032"
    location_data = retrieve_location(phone_number)
    print(location_data)
    address = reverse_geocoding(
        location_data["latitude"], location_data["longitude"])
    print(address['city'] if 'city' in address else address['town'] +
          ', ' + address['country'])
