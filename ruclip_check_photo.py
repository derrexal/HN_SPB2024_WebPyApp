# import ruclip
# import requests
# import numpy as np
# import torch
# from io import BytesIO
# from PIL import Image
#
#
# def normalize_vector(vec):
#     norm = np.linalg.norm(vec)
#     return vec / norm if norm > 0 else vec
#
#
# def cosine_similarity(vec_a, vec_b):
#     return np.dot(vec_a, vec_b)
#
#
# def similarity(url: str, name: str) -> float:
#     response = requests.get(url)
#     img = Image.open(BytesIO(response.content))
#     templates = ['{}', 'это {}', 'на фото {}']
#
#     device = 'cpu'
#     clip, processor = ruclip.load('ruclip-vit-base-patch32-384', device=device)
#     predictor = ruclip.Predictor(clip, processor, device, bs=8, templates=templates)
#
#     with torch.no_grad():
#         text_latents = normalize_vector(predictor.get_text_latents([name])).T
#         image_latents = normalize_vector(predictor.get_image_latents([img]))
#
#         cos_sim = cosine_similarity(image_latents, text_latents)[0][0]
#
#     return cos_sim
#
#
# def check_photo_function(photos):
#     """ Проверка фото """
#     result_check = [{'similar': str, 'name': str}]
#
#     for photo in photos:
#         similar = similarity(photo['photo_url'], photo['name'])
#         result_check.append({'similar': similar, 'name': photo['name']})
#
#     return result_check
