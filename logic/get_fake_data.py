import requests

def get_fake_users(quantity=1):
    url = f"https://fakerapi.it/api/v1/persons?_quantity={quantity}"
    response = requests.get(url)

    if response.status_code != 200:
        return []

    data = response.json().get("data", [])
    persons = [
        {
            "lastname": user["lastname"],
            "firstname": user["firstname"]
        }
        for user in data
    ]
    return persons

# users = get_fake_users(3)
# print(users)
# print(users[0]['lastname'])