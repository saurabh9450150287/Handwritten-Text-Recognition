# Handwritten-Text-Recognition
## Working Procedure
- **Paragraph Segmentation** :
Detect that area of the image which contains handwritten text

![Paragraph detector](https://user-images.githubusercontent.com/43703209/79051799-d968b500-7c4f-11ea-9457-c6c025c1eba2.PNG)



- **Word Detection** :
Detect the words in the area which we got after paragaraph segmentation.

- **Line Identification** :
Identify the lines and the words present in that line by checking the vertical overlap between the words

![Line Detector](https://user-images.githubusercontent.com/43703209/79051872-38c6c500-7c50-11ea-988b-c7ea655f96ad.PNG)


- **Handwriting Recognition**
Now for each of the lines we apply a pretrained model to detect the text present.

![Text Recognizer](https://user-images.githubusercontent.com/43703209/79051806-e84f6780-7c4f-11ea-9d21-fc657dcabbf9.PNG)


- **Error Correction(Denoising)**
After detecting the text we do denoising.For this we use a pre-trained model which tends to check that vocabulary,grammar of the text.
If the text identified is not there in english vocabulary then it predicts the closest matching words for that text and we then replace the previous one with later one.
## Pretrained Models
To get the pretrained models run this command on anaconda prompt:
```python
python get_models.py
```
## Output :
To see output along with the code please open :
https://github.com/saurabh9450150287/Handwritten-Text-Recognition/blob/master/0_handwriting_ocr.ipynb 
