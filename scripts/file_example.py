import json


def write_json_file():

    # Example of configuration file for MMSLA :
    MMSLA_config = {
        "layer_height": 0.05,  # mm
        "ctb_file" : "_D50_S.ctb",
        "resine_changes": [
            {
                "layer": 0,  # no cut off
                "resine": "build",  # display purposes only
                "exposure_time": 8000  # ms
            },
            {
                "layer": 10,  # cut out layer
                "resine": "tenuous",  # display purposes only
                "exposure_time": 8000  # ms
            },
            {
                "layer": 20,  # cut out layer
                "resine": "build",  # display purposes only
                "exposure_time": 8000  # ms
            }
        ]
    }

    # Write the data to a JSON file
    with open("config/print_settings.json", "w+") as f:
        json.dump(MMSLA_config, f)


def read_json_file():
    # Read the data from the JSON file
    with open("config/print_settings.json", "r") as f:
        changes = json.load(f)

    # Print the data to verify it was read correctly
    for switch in changes["resine_changes"]:
        print(switch)


def main():
    # Write data to JSON file
    write_json_file()

    # Read data from JSON file
    read_json_file()


if __name__ == "__main__":
    main()
# change exposure time f"M6001 S{expo_time}"
