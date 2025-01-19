import os
import json

def convert_to_yolo_from_xyxy(bbox, image_width, image_height):
    """
    [x_min, y_min, x_max, y_max] 형식의 bbox를 YOLO 형식으로 변환.

    Args:
        bbox (list): [x_min, y_min, x_max, y_max]
        image_width (int): 이미지 폭
        image_height (int): 이미지 높이

    Returns:
        list: YOLO 형식 [x_center, y_center, width, height]
    """
    x_min, y_min, x_max, y_max = bbox

    # 너비와 높이 계산
    w = x_max - x_min
    h = y_max - y_min

    # 중심 좌표 계산
    x_center = x_min + w / 2
    y_center = y_min + h / 2

    # 상대 좌표로 변환
    x_center_rel = x_center / image_width
    y_center_rel = y_center / image_height
    w_rel = w / image_width
    h_rel = h / image_height

    return [x_center_rel, y_center_rel, w_rel, h_rel]

def convert_json_with_xyxy_to_yolo(json_file, output_dir, image_width, image_height):
    """
    JSON 파일에서 [x_min, y_min, x_max, y_max] bbox를 YOLO 형식으로 변환하여 텍스트 파일로 저장.

    Args:
        json_file (str): JSON 파일 경로
        output_dir (str): YOLO 텍스트 파일 출력 디렉토리
        image_width (int): 이미지 폭
        image_height (int): 이미지 높이
    """
    with open(json_file, "r") as f:
        coco_data = json.load(f)

    os.makedirs(output_dir, exist_ok=True)

    # 이미지 파일 이름 매핑 (ID → 파일명)
    image_info = {img["id"]: img["file_name"] for img in coco_data["images"]}

    for annotation in coco_data["annotations"]:
        image_id = annotation.get("image_id")
        category_id = annotation.get("category_id", -1) - 1  # YOLO 클래스 ID는 0부터 시작
        bbox = annotation.get("bbox", [])  # 기본값으로 빈 리스트를 설정

        # 유효성 검사
        if not bbox or len(bbox) != 4:
            print(f"ID {annotation.get('id', 'unknown')}의 bbox가 비어 있거나 잘못되었습니다. 건너뜁니다.")
            continue

        if image_id not in image_info:
            print(f"이미지 ID {image_id}가 JSON 파일에 없습니다. 건너뜁니다.")
            continue

        file_name = image_info[image_id]
        yolo_bbox = convert_to_yolo_from_xyxy(bbox, image_width, image_height)

        # YOLO 텍스트 파일 저장
        txt_file = os.path.join(output_dir, os.path.splitext(file_name)[0] + ".txt")
        with open(txt_file, "a") as f:
            f.write(f"{category_id} " + " ".join(f"{coord:.6f}" for coord in yolo_bbox) + "\n")

    print(f"변환 완료: {json_file} → {output_dir}")


def process_multiple_json_with_xyxy(input_dir, output_dir, image_width, image_height):
    """
    여러 JSON 파일을 YOLO 형식으로 변환.

    Args:
        input_dir (str): JSON 파일 디렉토리
        output_dir (str): YOLO 텍스트 파일 출력 디렉토리
        image_width (int): 이미지 폭
        image_height (int): 이미지 높이
    """
    json_files = [f for f in os.listdir(input_dir) if f.endswith(".json")]

    for json_file in json_files:
        json_path = os.path.join(input_dir, json_file)
        convert_json_with_xyxy_to_yolo(json_path, output_dir, image_width, image_height)


# 실행 예시
input_dir = "/media/park/33DF49D6718AD56F/dataset/data/Training/02.라벨링데이터"  # JSON 파일 폴더 경로
output_dir = "/media/park/33DF49D6718AD56F/dataset/data/Training/originals"  # YOLO TXT 파일 출력 폴더 경로
image_width = 3840  # 고정된 이미지 폭
image_height = 2160  # 고정된 이미지 높이

process_multiple_json_with_xyxy(input_dir, output_dir, image_width, image_height)
