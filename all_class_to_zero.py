import os

def update_labels_to_zero(label_dir):
    """
    모든 라벨 파일의 클래스 ID를 0으로 변경하는 함수.
    
    :param label_dir: 라벨 파일이 저장된 디렉토리 경로
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
                file.write("\n".join(updated_lines))
    print(f"모든 라벨 ID가 0으로 변경되었습니다: {label_dir}")

# 라벨 파일이 저장된 디렉토리 경로 입력
label_directory = "/media/park/33DF49D6718AD56F/dataset/data/Training/originals"  # 라벨 파일 폴더 경로
update_labels_to_zero(label_directory)
