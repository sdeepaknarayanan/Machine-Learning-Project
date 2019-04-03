#reference: https://github.com/davrempe/domain-transfer-net/blob/master/datasets/ms-celeb-1m/data/decode_images.py 

import multiprocessing
import base64
import io
from PIL import Image
import os
import hashlib


def decode_image( x ):
    [url, face_data] = [x[0],x[1]]
    results_path = './MSceleb_data/data/'
    sha_res = hashlib.sha1(url).hexdigest() + '.jpg'
    fname = os.path.join(results_path, sha_res)
    decoded = base64.b64decode(face_data)
    img = Image.open(io.BytesIO(decoded))
    img.save(fname)

    info_path = './MSceleb_data/info/'
    with open(os.path.join(info_path,'test_data_info.txt'), 'a') as fd:
                fd.write('%s\n' % (sha_res))
        
if __name__=='__main__':
    data_file = '/home/deepak_narayanan/TrainData_Base.tsv'
    num_to_decode = 10**5
    
    print('Reading in file...')
    tasks = []
    with open(data_file, 'r', encoding='utf-8') as f:
        for i in range(0, num_to_decode):
            line = f.readline()
            tokens = line.split('\t')
            #print(tokens[1])
            tasks.append((bytes(tokens[4], 'utf-8'), bytes(tokens[1], 'utf-8')))
            
    print('Done.')
    print('Decoding...')
    
    pool_size = multiprocessing.cpu_count()
    pool = multiprocessing.Pool(processes=pool_size, maxtasksperchild=2)
    pool.map(decode_image, tasks)
    pool.close()
    pool.join()       
