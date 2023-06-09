#import sys
import json
import requests
from requests import HTTPError, TooManyRedirects


URL_GITHUB_API = "https://api.github.com/"
#JSON_PATH = ".//tokens//token.json"


# 暂时没卵用，因为好像不用token也能访问部分数据，私密数据访问token有权限访问的部分，其余看不到
#def read_json_authorization(json_path=JSON_PATH):
#    """
#    Read json file to get token.
#    """
#    try:
#        with open(json_path, "rt", encoding="utf-8") as f:
#            json_token = f.read()
#    except OSError as err:
#        print("OS error:", err)
#    finally:
#        f.close()
#
#    client_json_token = json.loads(json_token)
#    client_id, client_token = client_json_token["id"], client_json_token#["token"]
#
#    return (client_id, client_token)
#
## asignment id and token
#your_id, your_token = *read_json_authorization(),


def user_public_events(username="cireu"):
    """
    Get people in Github public events then output it in standard output.
    """
    if username is None:
        raise ValueError("username must be not none.")
    elif username is False:
        raise ValueError("username must be not False.")
    else:
        url_concate = URL_GITHUB_API + f'users/{username}/events/public'

    headers={
        "Accept": "application/vnd.github+json",   # `vnd.github`到底什么意思，不过可以换成 `application/json` 
        #"Authorization": f"token {your_token}", 
        'X-GitHub-Api-Version': '2022-11-28'
        }

    # with 语句可以省略 r.close()
    with requests.request(method='get', url=url_concate, headers=headers) as r:
        if r.status_code == requests.codes.ok:
            return json.dumps(r.json(), indent=4)  # maybe change.
        elif r.status_code in [403, 404]:
            return f"""{r.status_code}, {r.json()['message']}, \nmaybe you try to use a REST API endpoint without a token, \nor with a token that has insufficient permissions."""
        else:
            return f"{r.status_code}, {r.json()['message']}"

def main():
    input_name = input("Input Github username: ") or 'cireu'
    try:
        r = requests.get(URL_GITHUB_API + f'users/{input_name}')
        # r.raise_for_status()
    except ConnectionError as CE:
        raise CE
    except TooManyRedirects as TMR:
        raise TMR
    except HTTPError as HE:
        raise HE
    else:
        print(user_public_events(input_name))
    finally:
        print("\r\nFinished.")
    return 0

# Execute when the module is not initialized from an import statement.
# if __name__ == '__main__':
#     sys.exit(main())
