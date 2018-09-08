import urllib.request
import cv2
import numpy as np
import os

pic_num = 1

def store_raw_images(neg_images_link) :
  while True :
    if urllib.request.urlopen(neg_images_link).getcode() != 200 :
      continue
    elif urllib.request.urlopen(neg_images_link).getcode() == 200 :
      neg_image_urls = urllib.request.urlopen(neg_images_link).read().decode()
      break

  # if the folder 'negatives' does not exist, make it:
  if not os.path.exists('negatives') :
    os.makedirs('negatives')
  
  global pic_num
  for url in neg_image_urls.split('\n') :
    try :
      print(url)
      urllib.request.urlretrieve(url, 'negatives/neg_' + str(pic_num) + '.jpg')
      img = cv2.imread('negatives/neg_' + str(pic_num) + '.jpg', cv2.IMREAD_GRAYSCALE)
      resized = cv2.resize(img, (100, 100))
      cv2.imwrite('negatives/neg_' + str(pic_num) + '.jpg', resized)
      pic_num += 1

    except Exception as e :
      print(str(e))

# store_raw_images('http://image-net.org/api/text/imagenet.synset.geturls?wnid=n00523513')
# store_raw_images('http://image-net.org/api/text/imagenet.synset.geturls?wnid=n07942152')

def find_uglies() :
  counter = 1
  for file_type_dir in ['negatives'] : # negatives, positives, etc; folder under which images exist
    for image in os.listdir(file_type_dir) : # get image inside above folder
      for ugly in os.listdir('uglies') : # types of uglies in 'uglies' folder; various sizes, image types, etc
        try :
          current_image_path = str(file_type_dir) + '/' + str(image) # example: negatives/neg_58.jpg
          ugly = cv2.imread('uglies/' + str(ugly)) # image to be tested for ugliness
          question = cv2.imread(current_image_path) # image to be considered as a sample of ugliness

          if ugly.shape == question.shape and not(np.bitwise_xor(ugly, question).any()) :
            # if dimensions match, and there is a pixel by pixel match
            output = 'Ugly located! (' + str(counter) + ')'
            counter += 1
            print(output)
            print(current_image_path)
            os.remove(current_image_path)

        except Exception as e :
          print(str(e))

# find_uglies()

def create_positive_negative() :
  for file_type in ['negatives'] :
    for img in os.listdir(file_type) :
      if file_type == 'negatives' :
        line = file_type + '/' + img + '\n'
        with open('background.txt', 'a') as f :
          f.write(line)
      elif file_type == 'positives' :
        line = file_type + '/' + img + ' 1 0 0 50 50\n'
        with open('background.txt', 'a') as f :
          f.write(line)

create_positive_negative()