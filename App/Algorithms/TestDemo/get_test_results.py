from tinydb import TinyDB
from config import *
from save_predicted import draw_boxes_for_image

global db_path
db = TinyDB(db_path)


def read_test_labels():
    print("reading labels")
    global test_dataset, test_labels
    labels_path = test_dataset + test_labels
    labels_dict = {}
    with open(labels_path, 'r') as lbl_file:
        line = lbl_file.readline()
        while(line):
            line = line.strip().split(" ")
            labels_dict[line[0][25:-4]] = int(line[1])
            line = lbl_file.readline()
    return labels_dict


def test_on_full_images():
    test_labels = read_test_labels()
    parkings = db.all()
    accuracies = {}

    for parking in parkings:
        weather = parking['weather']
        img_url = parking['url']
        all_spots = parking['spots']

        img_guessed = 0
        for spot in all_spots:
            label_key = weather + '_' + img_url[:13] + '.' + img_url[13:15] + '_C08_' +  spot['slot_id']

            expected_label = test_labels[label_key]
            actual_label = spot['occupied']
            if bool(expected_label) == actual_label:
                img_guessed += 1
        
        accuracies[img_url] = img_guessed/len(all_spots)
        draw_boxes_for_image(img_url)

    average_accuracy = sum(list(accuracies.values())) / len(list(accuracies.values()))
    print("The average accuracy is " + str(round(average_accuracy, 4)))


if __name__ == "__main__":
    test_on_full_images()

            





