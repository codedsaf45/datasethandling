import os

def delete_images_without_labels(image_folder_path, label_folder_path):
    """
    라벨(.txt)이 없는 이미지를 삭제합니다.

    Parameters:
        image_folder_path (str): 이미지 파일이 저장된 폴더 경로
        label_folder_path (str): 라벨 파일이 저장된 폴더 경로
    """
    # 이미지 확장자 리스트
    image_extensions = ['.jpg', '.jpeg', '.png', '.bmp', '.tif', '.tiff']

    # 라벨 파일 목록 (확장자 제거)
    label_files = {os.path.splitext(file)[0] for file in os.listdir(label_folder_path) if file.endswith('.txt')}

    # 이미지 파일 검사
    for image_file in os.listdir(image_folder_path):
        if any(image_file.lower().endswith(ext) for ext in image_extensions):
            image_name, _ = os.path.splitext(image_file)

            # 라벨이 없는 이미지 삭제
            if image_name not in label_files:
                image_path = os.path.join(image_folder_path, image_file)
                print(f"삭제: {image_path}")
                os.remove(image_path)

# 사용 예시
image_folder_path = "/media/park/33DF49D6718AD56F/256.부산광역시 항만도로 컨테이너 차량에 의한 노면 파손 이미지 데이터/01-1.정식개방데이터/Validation/images"  # 이미지 파일이 저장된 폴더 경로
label_folder_path = "/media/park/33DF49D6718AD56F/256.부산광역시 항만도로 컨테이너 차량에 의한 노면 파손 이미지 데이터/01-1.정식개방데이터/Validation/labels"  # 라벨 파일이 저장된 폴더 경로

delete_images_without_labels(image_folder_path, label_folder_path)
