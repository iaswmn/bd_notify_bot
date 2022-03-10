import json


class FileManager:
    def __init__(self):
        self.file_name_json = 'bd_notify.json'
        self.bd_data_column = "bd_data"

    def save_data_to_file(self, data):
        with open(self.file_name_json, 'r+') as file:
            file_data = json.load(file)
            file_data[self.bd_data_column].append(data)
            file.seek(0)
            json.dump(file_data, file, indent=4)

    def get_all_data(self):
        new_dict = []
        with open(self.file_name_json, 'r') as file:
            file_data = json.load(file)
            for row in file_data[self.bd_data_column]:
                new_dict.append(row)
        return new_dict

    def get_data_by_id(self, from_id):
        new_dict = []
        with open(self.file_name_json, 'r') as file:
            file_data = json.load(file)
            for row in file_data[self.bd_data_column]:
                if row['id'] == from_id:
                    new_dict.append(row)
        return new_dict

    def update_data_by_id_and_i(self, from_id, row_number, new_data):
        with open(self.file_name_json, 'r') as file:
            file_data = json.load(file)
            with open(self.file_name_json, 'w') as file:
                for i in range(len(file_data[self.bd_data_column])):
                    if file_data[self.bd_data_column][i]['id'] == from_id and i == row_number:
                        file_data[self.bd_data_column][i]['name'] = new_data['name']
                        file_data[self.bd_data_column][i]['date'] = new_data['date']
                        file_data[self.bd_data_column][i]['nick'] = new_data['nick']
                json.dump(file_data, file, indent=4)

    def delete_data_by_id_and_i(self, from_id, row_number):
        with open(self.file_name_json, 'r') as file:
            file_data = json.load(file)
            with open(self.file_name_json, 'w') as file:
                for i in range(len(file_data[self.bd_data_column])):
                    if file_data[self.bd_data_column][i]['id'] == from_id and i == row_number:
                        del file_data[self.bd_data_column][i]
                        break
                json.dump(file_data, file, indent=4)

    def change_notify_status(self, from_id, row_number, status):
        with open(self.file_name_json, 'r') as file:
            file_data = json.load(file)
            with open(self.file_name_json, 'w') as file:
                for i in range(len(file_data[self.bd_data_column])):
                    if file_data[self.bd_data_column][i]['id'] == from_id and i == row_number:
                        file_data[self.bd_data_column][i]['notify'] = status
                json.dump(file_data, file, indent=4)