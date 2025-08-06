import cv2 
import numpy as np
import mnist
import time
# from ptpython.repl import embed

# 기울어진 숫자를 바로 세우기 위한 함수
affine_flags = cv2.WARP_INVERSE_MAP|cv2.INTER_LINEAR
def deskew(img):
    m = cv2.moments(img)
    if abs(m['mu02']) < 1e-2:
        return img.copy()
    skew = m['mu11']/m['mu02']
    M = np.float32([[1, skew, -0.5*20*skew], [0, 1, 0]])
    img = cv2.warpAffine(img,M,(20, 20),flags=affine_flags)
    return img

# --- [추가된 부분] 데이터 증강 함수 ---
def augment_data(img):
    rows, cols = img.shape
    
    # 랜덤 회전 (최대 ±15도)
    angle = np.random.randint(-15, 15)
    M_rot = cv2.getRotationMatrix2D((cols/2, rows/2), angle, 1)
    img_rotated = cv2.warpAffine(img, M_rot, (cols, rows))
    
    # 랜덤 이동 (최대 ±2픽셀)
    tx = np.random.randint(-2, 2)
    ty = np.random.randint(-2, 2)
    M_trans = np.float32([[1, 0, tx], [0, 1, ty]])
    img_translated = cv2.warpAffine(img_rotated, M_trans, (cols, rows))

    return img_translated

# HOGDescriptor를 위한 파라미터 설정 및 생성
winSize = (20,20)
blockSize = (10,10)
blockStride = (5,5)
cellSize = (5,5)
nbins = 9
hogDesc = cv2.HOGDescriptor(winSize,blockSize,blockStride,cellSize,nbins)

if __name__ =='__main__':
    # MNIST 이미지에서 학습용 이미지와 테스트용 이미지 가져오기
    train_data_raw, train_label_raw  = mnist.getTrain(reshape=False)
    test_data, test_label = mnist.getTest(reshape=False)

    # --- [수정된 부분] 데이터 증강 및 학습 ---
    # 원본 데이터와 레이블을 담을 리스트
    augmented_data = []
    augmented_labels = []

    print("Data augmentation started...")
    train_images = train_data_raw.reshape(-1, 20, 20)
    train_labels = train_label_raw.flatten()
    test_images = test_data.reshape(-1, 20, 20)
    test_labels = test_label.flatten()

    augmented_data = []
    augmented_labels = []

    startT = time.time()
    
    # 이제 단일 루프를 사용하여 모든 이미지와 레이블을 처리
    for i in range(len(train_images)):
        img = train_images[i]
        label = train_labels[i]

        # 3채널 이미지를 흑백으로 변환 (만약 3채널인 경우)
        if len(img.shape) == 3:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        deskewed_img = deskew(img)
        
        # 원본 이미지 추가
        augmented_data.append(deskewed_img)
        augmented_labels.append(label)
        
        # 증강된 이미지 추가 (회전, 이동)
        # for _ in range(1):
        aug_img = augment_data(deskewed_img)
        augmented_data.append(aug_img)
        augmented_labels.append(label)

    # 리스트를 numpy 배열로 변환
    augmented_data = np.array(augmented_data)
    augmented_labels = np.array(augmented_labels)
    endT = time.time() - startT
    print('Data augmentation complete. %.2f seconds' % endT)
    print('Original data size:', len(train_data_raw))
    print('Augmented data size:', len(augmented_data))

    # 학습 이미지 HOG 계산
    hogdata = [hogDesc.compute(img) for img in augmented_data]
    train_data = np.float32(hogdata)
    print('SVM training started...train data:', train_data.shape)
    
    # 학습용 HOG 데이타 재배열
    train_data = train_data.reshape(-1, train_data.shape[1])
    
    # SVM 알고리즘 객체 생성 및 훈련
    svm = cv2.ml.SVM_create()
    startT = time.time()
    # svm.trainAuto(train_data, cv2.ml.ROW_SAMPLE, augmented_labels)

    svm.setKernel(cv2.ml.SVM_RBF)
    svm.setC(12.5) # 적절한 값으로 설정
    svm.setGamma(0.50625) # 적절한 값으로 설정
    svm.train(train_data, cv2.ml.ROW_SAMPLE, augmented_labels)

    endT = time.time() - startT
    print('SVM training complete. %.2f Min' % (endT / 60))  
    
    # 훈련된 결과 모델 저장
    svm.save('svm_mnist.xml')

    # 테스트 이미지 글씨 바로 세우기 및 HOG 계산
    deskewed = [list(map(deskew,row)) for row in test_data]
    hogdata = [list(map(hogDesc.compute,row)) for row in deskewed]
    test_data = np.float32(hogdata)
    
    # 테스트용 HOG 데이타 재배열
    test_data = test_data.reshape(-1,test_data.shape[2])
    
    # 테스트 데이타 결과 예측
    ret, result = svm.predict(test_data)
    
    # 예측 결과와 테스트 레이블이 맞은 갯수 합산 및 정확도 출력
    correct = (result==test_label).sum()
    print('Accuracy: %.2f%%'%(correct*100.0/result.size))