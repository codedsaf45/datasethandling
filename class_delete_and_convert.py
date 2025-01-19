import os

def remove_class_from_labels(label_folder, target_class_id="9"):
    """
    YOLO 라벨 파일에서 특정 클래스 ID를 제거합니다.

    Parameters:
        label_folder (str): 라벨 파일이 저장된 폴더 경로
        target_class_id (str): 제거할 클래스 ID (예: "9")
    """
    label_files = [f for f in os.listdir(label_folder) if f.endswith('.txt')]

    for label_file in label_files:
        label_path = os.path.join(label_folder, label_file)
        with open(label_path, 'r') as f:
            lines = f.readlines()

        # 특정 클래스 ID를 제외한 라벨만 유지
        filtered_lines = [line for line in lines if not line.startswith(target_class_id)]

        # 기존 파일 덮어쓰기
        with open(label_path, 'w') as f:
            f.writelines(filtered_lines)

    print(f"클래스 ID '{target_class_id}' 제거가 완료되었습니다: {label_folder}")

def update_labels_to_zero(label_dir):
    """
    모든 라벨 파일의 클래스 ID를 0으로 변경하는 함수.
    
    Parameters:
        label_dir (str): 라벨 파일이 저장된 디렉토리 경로
    """
    for filename in os.listdir(label_dir):
        if filename.endswith(".txt"):  # 라벨 파일만 처리
            filepath = os.path.join(label_dir, filename)
            with open(filepath, "r") as file:
                lines = file.readlines()
            
            updated_lines = []
            for line in lines:
                parts = line.strip().split()
                if len(parts) > 0:
                    parts[0] = "0"  # 클래스 ID를 0으로 변경
                    updated_lines.append(" ".join(parts))
            
            with open(filepath, "w") as file:
                file.write("\n".join(updated_lines) + "\n")
    print(f"모든 라벨 ID가 0으로 변경되었습니다: {label_dir}")

# 실행 예시
label_folder = "/media/park/33DF49D6718AD56F/dataset/data/Training/originals"

# 9번 클래스 제거
remove_class_from_labels(label_folder, target_class_id="9")

# 모든 라벨을 0으로 변경
update_labels_to_zero(label_folder)
