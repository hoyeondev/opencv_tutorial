import cv2, numpy as np

img1 = None # roi로 선택할 이미지
win_name = 'Camera Matching' # 윈도우 이름
MIN_MATCH = 10 # 최소 매칭점 개수

'''
카메라로 특징점 매칭 예제
1. 사용자가 스페이스바를 누름
2. ROI로 등록된 이미지(img1) 설정
3. 카메라로 실시간 영상(img2) 캡쳐
4. ORB 특징점 검출 및 디스크립터 추출
5. Flann 매칭으로 img1과 img2의 특징점 매칭
6. 좋은 매칭점이 MIN_MATCH 이상인 경우, 원근 변환 행렬
7. 원근 변환 행렬을 이용해 img2에 img1의 영역 표시
'''

# ORB 검출기 생성
# ORB란 이미지에서 특징점을 찾는 알고리즘
detector = cv2.ORB_create(1000) # 이미지에서 1000개의 특징점을 찾는다.

# Flann 추출기 생성
FLANN_INDEX_LSH = 6
index_params = dict(algorithm=FLANN_INDEX_LSH,
                   table_number=6,
                   key_size=12,
                   multi_probe_level=1)
search_params = dict(checks=32)
matcher = cv2.FlannBasedMatcher(index_params, search_params)

# 카메라 캡쳐 연결 및 프레임 크기 축소
cap = cv2.VideoCapture(0)              
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

while cap.isOpened():       
    ret, frame = cap.read() 
    if not ret:
        break
    
    frame = cv2.flip(frame, 1)

    if img1 is None:  # 등록된 이미지 없음, 카메라 바이패스
        res = frame
    else:             # 등록된 이미지 있는 경우, 매칭 시작
        img2 = frame
        # [step 1]
        gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY) # 참조이미지
        gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY) # 현재 카메라 프레임
        
        # [step 2]
        # 키포인트와 디스크립터 추출
        # kp : keypoint 특징점의 위치정보
        # desc : 특징점의 특성을 숫자로 표현
        kp1, desc1 = detector.detectAndCompute(gray1, None) # 참조 이미지의 특징점
        kp2, desc2 = detector.detectAndCompute(img2, None) # 카메라의 이미지 특징점
        
        # 디스크립터가 없으면 건너뛰기
        if desc1 is None or desc2 is None or len(desc1) < 2 or len(desc2) < 2:
            res = frame
        else:
            # [step 3]
            # 매칭점 찾기
            # k=2로 knnMatch : 각 특징점마다 가장 유사한 2개의 후보를 찾는다.
            matches = matcher.knnMatch(desc1, desc2, 2)
            
            # [step 4]
            # 이웃 거리의 75%로 좋은 매칭점 추출
            ratio = 0.75
            good_matches = []
            for match_pair in matches:
                if len(match_pair) == 2:
                    m, n = match_pair # 1등, 2등
                    if m.distance < n.distance * ratio: # 1등이 2등보다 25%이상 좋으면
                        good_matches.append(m)
            
            print('good matches:%d/%d' % (len(good_matches), len(matches)))
            
            # matchesMask 초기화를 None으로 설정
            matchesMask = None
            label = "DIFFERENT PRODUCT"
            
            # 좋은 매칭점 최소 갯수 이상인 경우
            if len(good_matches) > MIN_MATCH:
                
                # 좋은 매칭점으로 원본과 대상 영상의 좌표 구하기
                src_pts = np.float32([kp1[m.queryIdx].pt for m in good_matches]).reshape(-1, 1, 2)
                dst_pts = np.float32([kp2[m.trainIdx].pt for m in good_matches]).reshape(-1, 1, 2)
                
                # 원근 변환 행렬 구하기
                mtrx, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)
                
                if mtrx is not None:
                    accuracy = float(mask.sum()) / mask.size
                    print("accuracy: %d/%d(%.2f%%)" % (mask.sum(), mask.size, accuracy * 100))
                    
                    if mask.sum() > MIN_MATCH and accuracy > 0.3:  # 정상치 매칭점 최소 갯수 이상인 경우
                        label = "SAME PRODUCT"
                        # 마스크를 리스트로 변환 (정수형으로)
                        matchesMask = [int(x) for x in mask.ravel()]
                        
                        # 원본 영상 좌표로 원근 변환 후 영역 표시
                        h, w = img1.shape[:2]
                        pts = np.float32([[[0, 0]], [[0, h-1]], [[w-1, h-1]], [[w-1, 0]]])
                        dst = cv2.perspectiveTransform(pts, mtrx)
                        img2 = cv2.polylines(img2, [np.int32(dst)], True, (0, 255, 0), 3, cv2.LINE_AA)
            
            # 매칭점 그리기
            res = cv2.drawMatches(img1, kp1, img2, kp2, good_matches, None, 
                                matchColor=(0, 255, 0),
                                singlePointColor=None,
                                matchesMask=matchesMask,
                                flags=cv2.DRAW_MATCHES_FLAGS_NOT_DRAW_SINGLE_POINTS)
            

            cv2.putText(res, label, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.5,
                        (0, 0, 255) if label == "DIFFERENT PRODUCT" else (0, 255, 0), 3)
    
    # 결과 출력
    cv2.imshow(win_name, res)
    key = cv2.waitKey(1) & 0xFF
    
    if key == 27:    # Esc, 종료
        break          
    elif key == ord(' '):  # 스페이스바를 누르면 ROI로 img1 설정
        x, y, w, h = cv2.selectROI(win_name, frame, False)
        if w and h:
            img1 = frame[y:y+h, x:x+w]
            print("ROI 선택됨: (%d, %d, %d, %d)" % (x, y, w, h))

cap.release()                          
cv2.destroyAllWindows()