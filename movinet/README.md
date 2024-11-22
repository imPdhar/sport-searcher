## Table of Contents:
- About MoViNet
- Setup for training and inference


## 📖 About MoViNet
The **MoViNet** model family has been published in March 2021 by Google research. It tries to solve the recurring problem with video classification models, which is how resource hungry the models are. Figure below shows how **MoViNet** compares in resource usage to other **SOTA** video classification models such as **X3D**.

![ezgif-2-166afa34a2](https://user-images.githubusercontent.com/88816150/227913487-4ed5b612-304b-4dd1-acf7-cddfb4f195ca.jpg)

### Chosen MoViNet Model/s:
- [ ] MoViNet Base A0
- [ ] MoViNet Base A1
- [ ] MoViNet Base A2
- [ ] MoViNet Base A3
- [ ] MoViNet Base A4
- [ ] MoViNet Base A5
- [ ] MoViNet Base A6
- [ ] MoViNet Stream A0
- [x] MoViNet Stream A1
- [x] MoViNet Stream A2
- [ ] MoViNet Stream A3
- [ ] MoViNet Stream A4
- [ ] MoViNet Stream A5

### Chose A2_Stream as it has the best trade-off between performance and accuracy.



## Setup
**Note:** I used Colab as the laptop I used for this assignment does not have very good computation capabilities so this setup will hold good for colab runners. The whole environment is dependent on Tensorflow so there are some things broken here and there but I have managed to fix them all.

**Colab link:** https://colab.research.google.com/drive/12M7w_RPhWvr_ua16AlaF8UnbDJqdC5az?usp=sharing

- Run ```pip install -r requirements.txt``` (If facing issues install packages individually)
- Download pre-trained checkpoint from model zoo of Tensorflow using ```!wget https://storage.googleapis.com/tf_model_garden/vision/movinet/movinet_a2_stream.tar.gz``` and place it in the directory of movinet
- Then ```pip install keras==2.15.0 ```
- Replace given builder.py within the path of protobuf (for colab it was ```'/usr/local/lib/python3.10/dist-packages/google/protobuf/internal'```
- Replace load_context.py within the path of Keras (for colab it was ```/usr/local/lib/python3.10/dist-packages/keras/src/saving/legacy/saved_model```)
- Make Dataset is in the format of Kinetics dataset (i.e train/classname/video1.avi, video2.avi...; test/classname/video1.avi, video2.avi etc)
- Then run train.py based on the model used. I used a2 so I made some changes in the training code for a2's architecture and the commandline to run it was ```!python3 train.py --data '/content/Dataset' --batch_size 32 --num_frames 32 --resolution 224 --num_epochs 14 --pre_ckpt movinet_a2_stream/ --save_ckpt '/content/drive/MyDrive/vid-class-ckpts/run04/' --export '/content/drive/MyDrive/vid-class-ckpts/run04/' --model_id a2 --save '/content/drive/MyDrive/vid-class-ckpts/run03/sport_model.tflite'```
- Since the dataset was balanced, I used generic accuracy as an evaluation metric.
- .tflite file will be saved in your specified dir. Use that path to pass into inference.py
- The inference commandline I used was ```!python3 inference.py --tflite '/content/drive/MyDrive/vid-class-ckpts/run04/sport_model.tflite' --source '/content/My 2 year old son playing cricket.mp4' --num_frames 32 --data '/content/Dataset/test' --save```
- The inference video will be saved as output.mp4 with the classification written in the video.

