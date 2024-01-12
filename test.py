import requests
import sys

# SmartThings API Endpoint 및 장치 목록을 가져올 URL
api_url = "https://api.smartthings.com/v1"
devices_url = f"{api_url}/devices"
device_profile_url = f"{api_url}/deviceprofiles"
locations_url = f"{api_url}/locations"
modes_url = ""
rooms_url = ""
rules_url = f"{api_url}/rules"
scenes_url = f"{api_url}/scenes"
capabilities_url = f"{api_url}/capabilities"

# Output file name
output_file_name = "output.txt"


def apiResponse(url, indent, output_file):
    # SmartThings Personal Access Token (하드 코딩)
    access_token = "6ea2b5b4-e1fa-48a1-a8c4-7b3f0f67e553"

    # 장치 목록 가져오기
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }

    response = requests.get(url, headers=headers)
    ret = []
    print("Response from ", url, file=output_file)  # Write to file instead of standard output
    if response.status_code == 200:
        devices = response.json()
        for key, value in devices.items():
            print("\t" * indent, key, "(", type(value), ") : ", file=output_file)
            if type(value) == list and len(value) != 0:
                for idx in range(len(value)):
                    print("\t" * (indent + 1), f"({idx})", file=output_file)
                    for key_, value_ in value[idx].items():
                        print(
                            "\t" * (indent + 2), key_, "(", type(value_), ") : ", value_, file=output_file
                        )
                        if url == locations_url and key_ == "locationId":
                            ret.append(f"{locations_url}/{value_}")
                        if url == devices_url and key_ == "deviceId":
                            ret.append(f"{devices_url}/{value_}/status")
                        if url == capabilities_url and key_ == "id":
                            ret.append(f"{capabilities_url}/{value_}/1")
                    print("\n", file=output_file)
            else:
                print("\t" * (indent + 1), value, file=output_file)
    else:
        print(f"에러 발생: {response.status_code}, {response}", file=output_file)

    print("\n", file=output_file)
    if ret:
        return ret


if __name__ == "__main__":
    with open(output_file_name, 'w') as output_file:
        # Location
        locationId_urls = apiResponse(locations_url, 0, output_file)  # GET Locations List
        for locationId_url in locationId_urls:
            apiResponse(locationId_url, 1, output_file)  # GET Each Location Information
            rooms_url = locationId_url + "/rooms"
            modes_url = locationId_url + "/modes"
            apiResponse(rooms_url, 1, output_file)  # GET Rooms List
            apiResponse(modes_url, 1, output_file)  # GET Modes List

        # Device
        device_status_urls = apiResponse(devices_url, 0, output_file)  # GET Devices List
        for device_status_url in device_status_urls:
            apiResponse(device_status_url, 1, output_file)  # GET Each Device's Status
        apiResponse(device_profile_url, 0, output_file)  # GET Device Profile

        # Automation
        apiResponse(rules_url, 0, output_file)  # GET Rules List
        apiResponse(scenes_url, 0, output_file)  # GET Scenes List

        # Capability
        capabilities_id_ver_urls = apiResponse(capabilities_url, 0, output_file)
        for capabilities_id_ver_url in capabilities_id_ver_urls:
            apiResponse(capabilities_id_ver_url, 1, output_file)
