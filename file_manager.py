import json


class FileManager:
    def __init__(self):
        self.file_name_json = 'bd_notify.json'
        self.bd_data_column = "bd_data"

    def save_data_to_file(self, data):
        with open(self.file_name_json, 'r+') as file:
            file_data = json.load(file)
            if str(data['id']) in file_data[self.bd_data_column][0]:
                file_data[self.bd_data_column][0][str(data['id'])].append(data)
            else:
                file_data[self.bd_data_column][0][str(data['id'])] = [data]
            file.seek(0)
            json.dump(file_data, file, indent=4)

    #def get_all_data(self):
    #    new_dict = []
    #    with open(self.file_name_json, 'r') as file:
    #        file_data = json.load(file)
    #        for row in file_data[self.bd_data_column][0]:
    #            for k in file_data[self.bd_data_column][0][row]:
    #                new_dict.append(k)
    #    return new_dict

    def get_all_data(self):
        new_dict = []
        with open(self.file_name_json, 'r') as file:
            file_data = json.load(file)
            for row in file_data[self.bd_data_column][0]:
                new_dict.append({row: [file_data[self.bd_data_column][0][row]]})
        return new_dict

    def get_data_by_id(self, from_id):
        new_dict = []
        with open(self.file_name_json, 'r') as file:
            file_data = json.load(file)
            for row in file_data[self.bd_data_column][0][str(from_id)]:
                new_dict.append(row)
        return new_dict

    def update_data_by_id_and_i(self, from_id, row_number, new_data):
        with open(self.file_name_json, 'r') as file:
            file_data = json.load(file)
            with open(self.file_name_json, 'w') as file:
                column = file_data[self.bd_data_column][0][str(from_id)]
                for i in range(len(column)):
                    if i == row_number:
                        column[i]['name'] = new_data['name']
                        column[i]['date'] = new_data['date']
                        column[i]['nick'] = new_data['nick']
                json.dump(file_data, file, indent=4)

    def delete_data_by_id_and_i(self, from_id, row_number):
        with open(self.file_name_json, 'r') as file:
            file_data = json.load(file)
            with open(self.file_name_json, 'w') as file:
                column = file_data[self.bd_data_column][0][str(from_id)]
                for i in range(len(column)):
                    if i == row_number:
                        del column[i]
                        break
                json.dump(file_data, file, indent=4)

    def change_notify_status(self, from_id, row_number, status):
        with open(self.file_name_json, 'r') as file:
            file_data = json.load(file)
            with open(self.file_name_json, 'w') as file:
                column = file_data[self.bd_data_column][0][str(from_id)]
                for i in range(len(column)):
                    if i == row_number:
                        column[i]['notify'] = status
                json.dump(file_data, file, indent=4)
