# Handwritten-Text-Recognition
## Working Procedure
- **Paragraph Segmentation** :
Detect that area of the image which contains handwritten text
- **Word Detection** :
Detect the words in the area which we got after paragaraph segmentation.
- **Line Identification** :
Identify the lines and the words present in that line by checking the vertical overlap between the words
- **Handwriting Recognition**
Now for each of the lines we apply a pretrained model to detect the text present.
- **Error Correction(Denoising)**
After detecting the text we do denoising.For this we use a pre-trained model which tends to check that vocabulary,grammar of the text.
If the text identified is not there in english vocabulary then it predicts the closest matching words for that text and we then replace the previous one with later one.
## Pretrained Models
To get the pretrained models run this command on anaconda prompt:
```python
python get_models.py
```
## Output :
To see output please open :
https://github.com/saurabh9450150287/Handwritten-Text-Recognition/blob/master/0_handwriting_ocr.ipynb
