import cv2

img = cv2.imread('mumu.png')  # 先手动保存一张全屏
roi = cv2.selectROI('Select Template', img, False)
if roi != (0, 0, 0, 0):
    x, y, w, h = roi
    template = img[y:y+h, x:x+w]
    # cv2.imwrite('../../resource/robot/activity/receive.png', template)
    cv2.imwrite('../../resource/common/receive.png', template)
    print('✅ 已保存 template.png，尺寸:', w, 'x', h)
cv2.waitKey(0)          # 按任意键继续
cv2.destroyAllWindows()