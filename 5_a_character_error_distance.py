#!/usr/bin/env python
# coding: utf-8

# # Model Distance between characters

# In[4]:


import numpy as np
import mxnet as mx
import difflib

from ocr.handwriting_line_recognition import Network as BiLSTMNetwork, decode as topK_decode
from ocr.utils.noisy_forms_dataset import Noisy_forms_dataset
from ocr.utils.ngram_dataset import Ngram_dataset
from ocr.utils.iam_dataset import resize_image


# ## Decode noisy forms

# We want to find what characters are more likely to be confused with each others to build a distance model between them

# For that we do a diff of the predictions vs the form

# In[6]:


line_image_size = (60, 800)
def handwriting_recognition_transform(image):
    image, _ = resize_image(image, line_image_size)
    image = mx.nd.array(image)/255.
    image = (image - 0.942532484060557) / 0.15926149044640417
    image = image.as_in_context(ctx)
    image = image.expand_dims(0).expand_dims(0)
    return image

def get_ns(is_train):
    network = BiLSTMNetwork(rnn_hidden_states=512, rnn_layers=2, max_seq_len=160, ctx=ctx)
    network.load_parameters("models/handwriting_line_sl_160_a_512_o_2.params", ctx=ctx)

    def noise_source_transform(image, text):
        image = handwriting_recognition_transform(image)
        output = network(image)
        predict_probs = output.softmax().asnumpy()
        return predict_probs
    ns = Noisy_forms_dataset(noise_source_transform, train=is_train, name="OCR_noise2", topK_decode=topK_decode)
    return ns


# In[9]:


ctx = mx.gpu(0) if mx.context.num_gpus() > 0 else mx.cpu()


# In[8]:


train_ns = get_ns(is_train=True)
ng_train_ds = Ngram_dataset(train_ns, "word_5train", output_type="word", n=5)


# #### Using ndiff to diff the expected result and the predicted results

# In[13]:


insertions = []
deletions = []
substitutions = []

for i in range(len(ng_train_ds)):
    _, _, noisy, actual = ng_train_ds[i]
    diffs = []
    for diff in difflib.ndiff(noisy, actual):
        if diff[0] == "+" or diff[0] == "-":
            diffs.append(diff)
    if len(diffs) == 1:
        if diffs[0][0] == "+":
            insertions.append(diffs[0][-1])
        if diffs[0][0] == "-":
            deletions.append(diffs[0][-1])
    if len(diffs) == 2:
        if diffs[0][0] == "+" and diffs[1][0] == "-" or diffs[0][0] == "-" and diffs[1][0] == "+":
            changes1 = (diffs[0][-1], diffs[1][-1])
            changes2 = (diffs[1][-1], diffs[0][-1])
            substitutions.append(changes1)
            substitutions.append(changes2)


# #### Using SequenceMatcher to diff the expected result and the predicted results

# In[14]:


insertions = []
deletions = []
substitutions = []
output = []
for i in range(len(ng_train_ds)):
    _, _, noisy, actual = ng_train_ds[i]
    seqm = difflib.SequenceMatcher(None, noisy, actual)
    for opcode, a0, a1, b0, b1 in seqm.get_opcodes():
        if opcode == 'equal':
            output.append(seqm.a[a0:a1])
        elif opcode == 'insert':
            for char in seqm.b[b0:b1]:
                insertions.append(char)
        elif opcode == 'delete':
            for char in seqm.a[a0:a1]:
                deletions.append(char)
        elif opcode == 'replace':
            # seqm.a[a0:a1] -> seqm.b[b0:b1]
            if len(seqm.a[a0:a1]) == len(seqm.b[b0:b1]):
                for charA, charB in zip(seqm.a[a0:a1], seqm.b[b0:b1]):
                    substitutions.append((charA, charB))
        else:
            pass


# In[20]:


insertion_dict = {}
for insertion in insertions:
    if insertion not in insertion_dict:
        insertion_dict[insertion] = 0
    insertion_dict[insertion] += 1
insertion_costs = np.ones(128, dtype=np.float64)
for key in insertion_dict:
    insertion_costs[ord(key)] = 0.9 if insertion_dict[key] <= 4 else 0.8
print(insertion_costs)
np.savetxt("models/insertion_costs.txt", insertion_costs, fmt='%4.6f')


# In[21]:


deletion_dict = {}
for deletion in deletions:
    if deletion not in deletion_dict:
        deletion_dict[deletion] = 0
    deletion_dict[deletion] += 1
print(deletion_dict)
deletion_costs = np.ones(128, dtype=np.float64)
for key in deletion_dict:
    deletion_costs[ord(key)] = 0.9 if deletion_dict[key] <= 4 else 0.8
print(deletion_costs)
np.savetxt("models/deletion_costs.txt", deletion_costs, fmt='%4.6f')


# In[22]:


substitution_dict = {}
for subs in substitutions:
    if subs not in substitution_dict:
        substitution_dict[subs] = 0
    substitution_dict[subs] += 1
print(substitution_dict)
substitute_costs = np.ones((128, 128), dtype=np.float64)
for key in substitution_dict:
    key1, key2 = key
    substitute_costs[ord(key1), ord(key2)] = 0.9 if substitution_dict[key] <= 4 else 0.8
print(substitute_costs)
np.savetxt("models/substitute_costs.txt", substitute_costs, fmt='%4.6f')


# In[ ]:




