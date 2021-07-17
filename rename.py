import os
path = r'D:\PythonPC\AI Master Class\Day12\Dataset\test'
# os.chdir('D:\\MasterClass\\Artificial_Intelligence\\Day12\\Code\\simple_images\\thanosMarvel\\')
os.chdir(path)
i=1
dataset_number = 0  # Set Dataset number
for file in os.listdir():
    src = file
    dst = str(dataset_number) +"_"+ str(i) +".jpg"
    os.rename(src,dst)
    i+=1

