import argparse

import cv2

import cvlib as cv
from cvlib.object_detection import draw_bbox

# list of supported objects
# https://github.com/arunponnusamy/object-detection-opencv/blob/master/yolov3.txt


def detect(input):
    input_img = cv2.imread(input)
    bbox, label, conf = cv.detect_common_objects(input_img)
    return input_img, bbox, label, conf


def filter(bbox, label, conf, object):
    filtered_bbox = []
    filtered_label = []
    filtered_conf = []

    for i in range(0, len(label)):
        if label[i] != object:
            continue
        filtered_bbox.append(bbox[i])
        filtered_label.append(label[i])
        filtered_conf.append(conf[i])

    return filtered_bbox, filtered_label, filtered_conf


def generate_output_image(output, input_img, bbox, label, conf, object=None):
    if object:
        bbox, label, conf = filter(bbox, label, conf, object)

    output_img = draw_bbox(input_img, bbox, label, conf)
    cv2.imwrite(output, output_img)


def count(output, label, object=None):
    with open(output, "w") as output_text:
        if object:
            output_text.write(str(label.count(object)))
        else:
            output_text.write(str(len(label)))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input", help="input filename")
    parser.add_argument("output_without_ext", help="output filename without extension")
    parser.add_argument(
        "--generate_image", help="enable generate image", action="store_true"
    )
    parser.add_argument("--count", help="enable count", action="store_true")
    parser.add_argument("--object", help="car, person, ...")
    args = parser.parse_args()

    input_img, bbox, label, conf = detect(args.input)
    print("bbox", bbox)
    print("label", label)
    print("conf", conf)

    if args.generate_image:
        generate_output_image(
            args.output_without_ext + ".png",
            input_img,
            bbox,
            label,
            conf,
            object=args.object,
        )

    if args.count:
        count(args.output_without_ext + ".txt", label, object=args.object)


if __name__ == "__main__":
    main()

