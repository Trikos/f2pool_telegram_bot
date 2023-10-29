import variables
import requests
import datetime


def get_all_mining_user_name():
    api_url = f"{variables.f2pool_endpoint}/mining_user/list"
    headers = {"F2P-API-SECRET": variables.f2pool_api_key}
    try:
        response = requests.post(api_url, headers=headers)
        response.raise_for_status()
        data = response.json()  # Ottieni il payload come un dizionario Python
        user_list = data.get("mining_user_list", [])
        usernames = [user.get("mining_user_name") for user in user_list]
        return usernames

    except requests.exceptions.HTTPError as e:
        error_message = f"Errore nella richiesta HTTP: {e} # {e.response}"
        with open("error_log.txt", "a") as log_file:
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            log_file.write(f"{timestamp} - {error_message}\n")
        return e.response


def post_pause_unpause(action: str, data):
    try:
        api_url = f"{variables.f2pool_endpoint}/mining_user/payment/{action}"
        headers = {"F2P-API-SECRET": variables.f2pool_api_key}
        payload = {
            "mining_user_names": data,
            "currency": "bitcoin"
        }
        response = requests.post(api_url, headers=headers, json=payload)
        response.raise_for_status()
        return response

    except requests.exceptions.HTTPError as e:
        error_message = f"Errore nella richiesta HTTP: {e} # {e.response}"
        with open("error_log.txt", "a") as log_file:
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            log_file.write(f"{timestamp} - {error_message}\n")
        return e.response
