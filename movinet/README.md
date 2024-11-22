
### Chosen MoViNet Models:
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


## Table of Contents:
- About MoViNet
- Prepare Dataset
- Train MoViNet Model
- Inference MoViNet Model

## 📖 About MoViNet
The **MoViNet** model family has been published in March 2021 by Google research. It tries to solve the recurring problem with video classification models, which is how resource hungry the models are. Figure below shows how **MoViNet** compares in resource usage to other **SOTA** video classification models such as **X3D**.

![ezgif-2-166afa34a2](https://user-images.githubusercontent.com/88816150/227913487-4ed5b612-304b-4dd1-acf7-cddfb4f195ca.jpg)



**Example**
```
python3 inference.py --tflite my_model.tflite --source 'videos/sample.mp4' --num_frames 32 \
                     --data data/test --save
```
