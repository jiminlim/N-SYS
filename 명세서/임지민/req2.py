import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from PIL import Image
import pandas as pd 
import numpy as np

# img, caption = preprocess.sampling_data(1,'./datasets/train_data.csv')
data =pd.read_csv('./datasets/train_data.csv' ,sep='|', encoding='UTF8', names=['image_name','comment_number','comment'], header=None)
imgs = data['image_name']
captions = data['comment']


# req1-1 . text size 변경 
# for img_name in imgs:
    # image = Image.open('./datasets/images/'+img_name)
    # width, height = image.size
    # if width != 500 or height != 375:
    #     resize_image = image.resize((500,375))
    #     resize_image.save('./datasets/resize_images/'+img_name)
       

# req1-2. 이미지 정규화
for img_name in imgs.head(1):
    img = mpimg.imread('./datasets/resize_images/'+img_name)
    img = img/255

# plt.imshow(img)
# plt.show()







        
    
    

        



