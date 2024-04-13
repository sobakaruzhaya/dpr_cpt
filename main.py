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

def get_analog_price(d):
    file = pd.read_excel("price.xlsx", nrows=37)
    for rows,columns in file.iterrows():
        if columns.values[1] == d:
            return columns.values[3]

def check_price(price):
	return bool(price)

price_corr = False

def main(filename):
	print(1)
	dataset_path = os.path.join('static','img','uploads',f"{filename}.jpg")
	results = model.predict(dataset_path, save=True, save_crop=True, project="images", name=filename)
	labels = ['name','rub','kop']
	a = []
	price = 0
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

	print(a)
	d = a[0].lower()
	print(type(d))
	if "картоф" in d:
		d = "Картофель"
	elif "капус" in d:
		d = "Капуста белокочанная свежая"
	elif "лук" in d:
		d = "Лук репчатый"
	elif "свёк" in d:
		d = "Свёкла столовая"
	elif "морк" in d:
		d = "Морковь"
	elif "огур" in d:
		d = "Огурцы свежие"
	elif "тома" in d:
		d = "Томаты свежие"
	elif "бана" in d:
		d = "Бананы"
	elif "яблок" in d:
		d = "Яблоки"
	elif "яйц" in d:
		d = "Яйца куриные категории С1"
	elif "кур" in d:
		d = "Тушка куриная"
	elif "колб" in d:
		d = "Колбасы полукопченая, варено-копченая"
	elif "сахар" in d:
		d = "Сахар-песок"
	elif "хле" in d:
		d = "Хлеб из ржаной муки и из смеси ржаной и пшеничной муки"
	elif "пшено" in d:
		d = "Пшено"
	elif "слив" in d:
		d = "Масло сливочное"
	elif "марг" in d:
		d = "Маргарин"
	elif "пастер" in d:
		d = "Молоко пастеризованное 2,5%-3,2% жирн."
	elif "стер" in d:
		d = "Молоко стерилизованное 2.5%-3.2% жирн."
	elif "твор" in d:
		d = "Творог 5%-10% жирности"
	elif "мясн" in d:
		d = "Консервы мясные"
	elif "овощ" in d:
		d = "Консервы овощные"
	elif "фрук" in d:
		d = "Консервы фруктово-ягодные"
	elif "корм" in d:
		d = "Сухие корма для домашних животных (кошек и собак)"
	elif "подг" in d:
		d = "Подгузники детские бумажные (3-18 кг)"
	elif "мыло туалет" in d:
		d = "Мыло туалетное"
	elif "хозяй" in d:
		d = "Мыло хозяйственное"
	elif "стир" in d:
		d = "Порошок стиральный"
	elif "бума" in d:
		d = "Бумага туалетная"
	else:
		d = "Прочее"

	if d == "Прочее" or "социальная" not in a[0].lower():
		price = 2
	elif float(a[1]) <= get_analog_price(d):
		price = 0
	else:
		price = 1

	
	
		

	
	data = {'Наименование файла':[f"{filename}.jpg"], 'Категория продукта':[d],'Цена': [price]}
	df = pd.DataFrame(data)
	df.to_csv('output.csv', encoding='utf-8',index=False,sep=";")

	cursor.execute("INSERT INTO data VALUES(?,?,?,?,?)",(f"{filename}.jpg",a[0],a[1],0,price))
	connection.commit()
	




if __name__ == "__main__":
	for root, dirs, files in os.walk("dataset/"):  
		for filename in files:
			file = (filename.replace(".jpg",""))
			main(file)
	