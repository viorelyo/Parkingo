import cv2
from tinydb import TinyDB, Query
from config import *



def draw_boxes_for_image(img_path):
    """
    Draw a box around each parking spot from a full image: green for free, red for occupied
    """
    global test_dataset
    full_path = test_dataset + img_path
    img = image = cv2.imread(full_path)

    global db_path
    db = TinyDB(db_path)
    q = Query()
    spots = db.search(q.url == img_path)[0]['spots']
    for spot in spots:
        if spot["occupied"]:
            # create red box
            cv2.rectangle(img, (spot['crop'][0], spot['crop'][1]),
                          (spot['crop'][0] + spot['crop'][2], spot['crop'][1] + spot['crop'][3]), (0, 0, 255), 2)
        else:
            # create green box
            cv2.rectangle(img, (spot['crop'][0], spot['crop'][1]),
                          (spot['crop'][0] + spot['crop'][2], spot['crop'][1] + spot['crop'][3]), (0, 255, 0), 2)

    global test_output
    output_path = test_output + img_path
    cv2.imwrite(output_path, img)


if __name__ == "__main__":
    get_test_results()

            





