# -*- coding: utf-8 -*-
from wordcloud import WordCloud, ImageColorGenerator
import numpy as np
from PIL import Image

def word2cloud(text: str, mask_image: Image=None):
    if mask_image == None:
        wc = WordCloud(font_path='simhei.ttf', width=800, height=600, mode='RGBA',
                       background_color=None).generate(text)
    else:
        mask = np.array(mask_image)  # 使用mask,最好界限分明对比强烈的图形
        image_colors = ImageColorGenerator(mask)  # 提取蒙版颜色
        wc = WordCloud(mask=mask, color_func=image_colors,
                       width=800, height=600,
                       font_path='simhei.ttf', mode='RGBA',
                       background_color=None).generate(text)
    img_res = wc.to_image()
    return img_res


# 这个大小只是大概,若要精细化,可用结巴统计词频
# freq=jieba.analyse.extract_tags(text, topK=200, withWeight=True)
# freq={w[0]:w[1] for w in freq}
# WordCloud(...).generate_from_frequencies(freq)

# plt.imshow(wc,interpolation='bilinear')  # 插值颜色均匀
# plt.axis('off')
# plt.show()

#wc.to_file('wordcloud.png')  # 保存