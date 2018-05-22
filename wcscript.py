from wordcloud import WordCloud as wc
import matplotlib.pyplot as plt

#text = open("beep boop").read()
text = "Beep boop bip bap bup"

# Generate a word cloud image
wordcloud = wc().generate(text)

#plt.imshow(wordcloud, interpolation='bilinear')
#plt.axis("off")
#plt.show()

image = wordcloud.to_image()
image.show()
