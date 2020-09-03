import json
import os


def get_all_combinations(snapshot: json) -> list:
    result = []
    python_dict = json.loads(snapshot)
    object_list = python_dict["objects"]
    shape_list = ["cube", "circle"]
    for obj in object_list:
        if obj["shape"] in shape_list:
            temp = dict()
            temp["directions"] = python_dict["directions"]
            temp["objects"] = [obj]
            result.append(json.dumps(temp, indent=4))
    return result


def get_unique_object_name(field: dict, step_count: int) -> str:
    return field["size"] + "_" + field["color"] + "_" + field["shape"] + "_" + str(step_count)


def read_all_snapshot_jsons(path: str) -> list:
    all_snapshot_jsons = []
    for file_name in os.listdir(path):
        full_path = path + "/" + file_name
        frame = int(file_name.split(".")[0][5:])  # filename: frame375.json
        with open(full_path) as json_file:
            all_snapshot_jsons.append([frame, json.load(json_file)])
    return all_snapshot_jsons


def get_all_combinations_with_name(path: str):
    result = []
    for snapshot_json in read_all_snapshot_jsons(path):
        frame = snapshot_json[0]
        ss = snapshot_json[1]

        all_comb = get_all_combinations(json.dumps(ss,indent=4))
        for i in all_comb:
            d = json.loads(i)["objects"]
            name = get_unique_object_name(d[0],frame)
            result.append([name,i])
            print(name)
    return result

def write_to_file(input_path, output_path):
    arr = get_all_combinations_with_name(input_path)
    if not os.path.exists(output_path):
        os.makedirs(output_path)


    for snapshot in arr:
        name = snapshot[0]
        snapshot_json = snapshot[1]
        print(name)
        print(snapshot_json)
        f = open(output_path + "/" + name + ".json", "w")
        f.write(snapshot_json)
        f.close()


input_path = "/Users/cagatayyigit/Desktop/snapshots"
output_path = "/Users/cagatayyigit/Desktop/new_snapshots"
write_to_file(input_path,output_path)