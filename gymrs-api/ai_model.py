# Çalışmada kullanılacak fonksiyonel kütüphaneler dahil ediliyor.
import numpy as np
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
from plotly.subplots import make_subplots
import plotly.graph_objects as go

# Çalışmada kullanılacak makine öğrenmesi kütüphaneleri dahil ediliyor.
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix, accuracy_score, f1_score
from sklearn.model_selection import cross_val_score

# Feature name içeriklerinin belirli noktalarda yoksayılması ile ilgili uyarıların kaldırılması için kullanılmıştır.
import warnings
warnings.filterwarnings('ignore')

# GYM Programs veri kümesi pandas aracılığı ile okunuyor.
program_dataset = pd.read_csv('datasets/gym-programs.csv')
program_data = program_dataset.iloc[:,2:]
program_target = program_dataset['class']

program_counts = program_dataset.groupby(['class']).count()

goals_counts= program_dataset.groupby(['class'])['class'].count()
classes = ["Strength-1", "Strength-2", "Strength-3", "Plyometrics", "Cardio", "Stretching", "Powerlifting"]

# Data ve target içeriklerinin belirlenen oran ve random_state doğrultusunda train-test olarak ayrılması.
x_train, x_test, y_train, y_test = train_test_split(program_data, program_target, test_size=0.20, random_state=90)

# Random Forest Classifier ile modelin oluşturulması ve verinin modele fit edilmesi.
model = RandomForestClassifier()
model.fit(x_train, y_train)

# Cross-validation işlemi uygulanarak (7 fold) modelin test edilmesi.
# Not: Bu aşamada veri train/test olarak ayrılmadan verilmiştir, cv=7 ile veri 7 parçaya bölünerek cv işlemi gerçekleştirilmektedir.
scores = cross_val_score(model, program_data, program_target, cv=7)
print("Scores for cross-validation: ", scores)

# Skorlara ait ortalama hesaplanıyor.
print("Mean: ", scores.mean())

# Skorlara ait standart sapma hesaplanıyor.
print("Std: ", scores.std())

# CV işlemine ek olarak başlangıçta oluşturulan train-test verileri ile model test ediliyor.
# Test sonuçları ve gerçek sonuçlar ile oluşturulan confusion_matrix ve hesaplanan accuracy ve f1 score değerleri görüntüleniyor.
predicted = model.predict(x_test)
acc = accuracy_score(y_test, predicted)
print("Accuracy: " + str(acc))
f1 = f1_score(y_test, predicted, average="weighted")
print("F1 Score: " + str(f1))
cm = confusion_matrix(y_test, predicted)
print("Confusion Matrix: \n", cm)

prediction_classes = {1: "Strenght",
                      2: "Strenght",
                      3: "Strength",
                      4: "Plyometrics",
                      5: "Cardio",
                      6: "Stretching",
                      7: "Powerlifting"}

# Test edilen örneklerde oluşturulan dizi yapısı, modelin eğitilmiş olduğu veri kümesindeki kolon sıraları ile eşdeğer biçimde tanımlanmıştır.
# Bu doğrultuda 6 boyutlu bir dizi için değerler sırasıyla şu özellikleri temsil etmektedir:
#   level: Antrenmanın zorluk derecesi veya kullanıcının spor tecrübesi olarak belirtilir. [1: Beginner, 2: Intermediate, 3: Expert]
#   eq: Antrenmanın gerçekleştirileceği ekipman veya ortamı belirtir. [1: No-eqs, 2: Basic eqs, 3: Advanced eqs. ]
#   gender: Kullanıcının cinsiyetini belirtir. [1: Male, 2: Female]
#   goal: Kullanıcının spor hedefini belirtir. [1: Strength, 2: Plyometrics, 3: Cardio, 4: Stretching, 5: Powerlifting]
#   bmi: Kullanıcıya ait vücut kitle indeksini belirtir. [1: <19, 2: <25, 3: <30, 4: >30]
#   time: Kullanıcının gün içerisinde spora ayırmak istediği süre miktarını dakika cinsinden belirtir. [1: <45min, 2: <90, 3: >90]

feature_test1 = np.array([2,3,1,1,3,3])
feature_test1 = feature_test1.reshape(1,-1)

# Tanımlanan bu örnek için
#   orta seviyeli, gelişmiş ekipmanlar kullanarak, güç kazanımına yönelik, yaklaşık 175 boylarında ve 80 kilogram bir erkeğin günde 90 dakikadan fazla
#   ayıracağı bir senaryo için antrenman programının sınıfı belirlenmektedir.

prediction_test1 = model.predict(feature_test1)
print("Bu senaryo için tahmin edilen sınıf:", prediction_test1[0])

# Tahmin edilen sınıf doğrultusunda filtreleme işlemi ile elde edilecek egzersizlerin yer aldığı veri kümesi tanımlanıyor.
gym_dataset = pd.read_csv('datasets/megaGymDataset.csv')
gym_dataset.columns = gym_dataset.columns.str.replace('Unnamed: 0', 'index')

# Kaggle üzerinden alınan veri kümesindeki eksik değerlerin yer aldığı satırlar tespit ediliyor.
missing_values_count = gym_dataset.isnull().sum()

print("Row count:\t" + str(gym_dataset.shape[0]))
print("Col count:\t" + str(gym_dataset.shape[1]))

# Kaslara ve bölgelere göre verinin gruplandırılması ve incelenmesi
count_exercises = gym_dataset.groupby(['BodyPart']).count()

# Bu aşamadan sonra diğer veri kümesini anlamak ve incelemek amacı ile çalışmalar gerçekleştirilmektedir.
# 'Intermediate' zorluk düzeyinde olan egzersizlerin listelenmesi.
intermediate_exercises = gym_dataset[gym_dataset.Level == 'Intermediate']

# İlgili zorluk seviyesindeki egzersizlerden ekipman gerektirmeyenlerin listelenmesi.
body_only_intermediate_exercises = intermediate_exercises[intermediate_exercises.Equipment == 'Body Only']

# İlgili egzersizlerin çalıştırmış olduğu kas grubu veya vücut bölümlerine göre dağılımlarının incelenmesi ve görselleştirilmesi.
body_only_exercises_groupby_bodypart = body_only_intermediate_exercises.groupby(['BodyPart']).count()
body_only_exercises_groupby_bodypart = body_only_exercises_groupby_bodypart.sort_values(by='index')

# Egzersizlerin vücut bölgesi ve amaçları doğrultusunda gruplandırılması.
bodyPart_dist = gym_dataset.groupby(['Type','BodyPart']).count()

# İlgili içeriklerin 0 ve 1 seviyelerine göre gruplandırılarak toplam egzersiz sayısının elde edilmesi
bodyPart_dist=bodyPart_dist.groupby(level=[0,1]).sum()

# Kaç farklı eşsiz egzersiz tipi olduğu bilgisi elde ediliyor.
allTypes =(gym_dataset["Type"].unique())

# Her egzersiz tipi için elde edilen egzersiz sayıları tanımlanıyor.
typeDfs = []
for i in range(7):
    typeDfs.append(bodyPart_dist.iloc[bodyPart_dist.index.get_level_values('Type') == allTypes[i]])

# Veri kümesi eşsiz kolon değerlerinin incelenmesi
print(f'Body Part: {gym_dataset.BodyPart.unique()} \n')
print(f'Equipment: {gym_dataset.Equipment.unique()} \n')
print(f'Type: {gym_dataset.Type.unique()} \n')

# Feature test verisinin - boyut analizi
print(feature_test1)
print(feature_test1[0])
print(len(feature_test1[0]))

# Kullaniciya onerilecek spor programı için parametrelerin belirlenmesi;

# Antrenman zorluğunun belirlenmesi
if prediction_test1[0] == 1:
  PARAM_LEVEL = ['Beginner' ,'Intermediate']
elif prediction_test1[0] == 3:
  PARAM_LEVEL = ['Intermediate', 'Expert']
else:
  PARAM_LEVEL = ['Beginner', 'Intermediate', 'Expert']

# Antrenman ekipmanlarının belirlenmesi
if feature_test1[0][1] == 1:
  PARAM_EQUIPMENT = ['Cable', 'Body Only', 'None', 'Foam Roll']
else:
  PARAM_EQUIPMENT = ['Bands', 'Barbell', 'Kettlebells', 'Dumbbell', 'Other', 'Cable', 'Machine', 'Body Only', 'Medicine Ball', 'None', 'Exercise Ball', 'Foam Roll', 'E-Z Curl Bar']

# Antrenman hareket sayısının belirlenmesi
if feature_test1[0][5] == 1:
  PARAM_EXERCISES = 5
elif feature_test1[0][5] == 2:
  PARAM_EXERCISES = 7
else:
  PARAM_EXERCISES = 10

# Antrenman tipinin belirlenmesi
PARAM_TYPE = [prediction_classes[prediction_test1[0]]]

print(f'PARAM_LEVEL (exercise-level)= {PARAM_LEVEL}')
print(f'PARAM_EXERCISES (exercise-number)= {PARAM_EXERCISES}')
print(f'PARAM_EQUIPMENT (exercise-eq-type)= {PARAM_EQUIPMENT}')
print(f'PARAM_TYPE (exercise-goal)= {PARAM_TYPE}')

# Yeni antrenman programı için uygun hareketler getiriliyor
new_program_data = gym_dataset.loc[ \
                    (gym_dataset['Level'].isin(PARAM_LEVEL)) & \
                    (gym_dataset['Equipment'].isin(PARAM_EQUIPMENT)) & \
                    (gym_dataset['Type'].isin(PARAM_TYPE)) \
                    ].sort_values(by=['Type','BodyPart']) \
                    .copy(deep=True) \
                    .reset_index()

new_program_data.drop(columns=['index'],inplace=True)

# Yeni antrenmana ait kolon değerleri kontrol ediliyor
print(f'Level: {new_program_data.Level.unique()} \n')
print(f'Equipment: {new_program_data.Equipment.unique()} \n')
print(f'Type: {new_program_data.Type.unique()} \n')
print(f'Total Number of Workouts: {new_program_data.count()}')

# Kaç farklı uygun hareket olduğu görüntüleniyor
new_program_data.groupby('Type').size()

# Orantılı dağılım için her zorluk seviyesinden kaç örnek alınacağı belirleniyor
sampling_num = int(round((PARAM_EXERCISES/len(new_program_data.Level.unique()))))
print(sampling_num)

# Eksik kalacak hareket sayısı belirleniyor
remainder = PARAM_EXERCISES % sampling_num
print(remainder)

# Yeni program oluşturuluyor
new_program = new_program_data.groupby("Level").sample(n=sampling_num,random_state=42).sort_values("Rating")

# Eksik hareketler programa ekleniyor
new_program._append(new_program_data.sample(n=remainder, random_state=42))

while new_program.duplicated().sum() != 0:
  dup_count = new_program.duplicated().sum()
  new_program.drop_duplicates()
  new_program._append(new_program_data.sample(n=dup_count, random_state=42))

program_json = new_program.to_json(orient="records")

print(program_json)





