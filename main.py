import pandas as pd
import easyocr
from ultralytics import YOLO
import os
import sqlite3
connection = sqlite3.connect('database.db',check_same_thread=False)

cursor = connection.cursor()
cursor.execute("""CREATE TABLE IF NOT EXISTS data(
			   img TEXT,
			   name TEXT,
			   rub TEXT,
			   kop TEXT,
			   soc_prise INT
)""")
connection.commit()
# Загрузка модели YOLO
model = YOLO('model/best.pt')


def text_from_foto(imgg):
	reader = easyocr.Reader(['ru'])
	output = reader.readtext(imgg)
	a = ""
	for i in range(len(output)):
		a = a +  (output[i][-2]) + " "
	return a

def clear_text(s):
	t = "йцукенгшщзхъфывапролджэячсмитьбю,. 1234567890"
	a = ""

	for j in s:
		if j.lower() in t:
			a += j
	return(a)


def main(filename):
	print(1)
	dataset_path = os.path.join('static','img','uploads',f"{filename}.jpg")
	results = model.predict(dataset_path, save=True, save_crop=True, project="images", name=filename)
	labels = ['name','rub','kop']
	a = []
	for i in range(3):
		text = clear_text(text_from_foto(f"images/{filename}/crops/{labels[i]}/{filename}.jpg"))
		if labels[i] == 'kop':
			
			if "00" in text:
				text = "0"
				print("YES")
				a.append(text)
		elif labels[i] == "rub":
			g = []
			for t in text:
				if t in "0987654321":
					g.append(t)
				
			text = "".join(g)
			a.append(text)
		else:
			a.append(text)
	data = {'Наименование файла':[f"{filename}.jpg"], 'Категория продукта':[a[0]],'Цена':[1]}
	df = pd.DataFrame(data)
	df.to_csv('output.csv', encoding='utf-8',index=False,sep=";")

	cursor.execute("INSERT INTO data VALUES(?,?,?,?,?)",(f"{filename}.jpg",a[0],a[1],a[2],0))
	connection.commit()


if __name__ == "__main__":
	for root, dirs, files in os.walk("dataset/"):  
		for filename in files:
			file = (filename.replace(".jpg",""))
			main(file)