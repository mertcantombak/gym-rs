# Çalışmada API servisi için kullanılan yapılar dahil ediliyor.
from flask import Flask,request, jsonify

# Çalışmada kullanılacak fonksiyonel kütüphaneler dahil ediliyor.
import numpy as np
import pandas as pd

# Çalışmada kullanılacak makine öğrenmesi kütüphaneleri dahil ediliyor.
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

app = Flask(__name__)

# GYM Programs veri kümesi pandas aracılığı ile okunuyor.
program_dataset = pd.read_csv('datasets/gym-programs.csv')
program_data = program_dataset.iloc[:,2:]
program_target = program_dataset['class']

# Data ve target içeriklerinin belirlenen oran ve random_state doğrultusunda train-test olarak ayrılması.
x_train, x_test, y_train, y_test = train_test_split(program_data, program_target, test_size=0.20, random_state=90)

# Random Forest Classifier ile modelin oluşturulması ve verinin modele fit edilmesi.
model = RandomForestClassifier()
model.fit(x_train, y_train)

prediction_classes = {1: "Strength",
                      2: "Strength",
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

# Tahmin edilen sınıf doğrultusunda filtreleme işlemi ile elde edilecek egzersizlerin yer aldığı veri kümesi tanımlanıyor.
gym_dataset = pd.read_csv('datasets/megaGymDataset.csv')
gym_dataset.columns = gym_dataset.columns.str.replace('Unnamed: 0', 'index')

# POST metodu
@app.route('/PostData', methods=['POST'])
def post_data():
    data = request.get_json()  # Gelen JSON verisini al
    user_feature = np.array(data['array'] )     # İstenilen dizi verisini al
    user_feature = user_feature.reshape(1,-1)

    user_predict = model.predict(user_feature)

    # Antrenman zorluğunun belirlenmesi
    if user_predict[0] == 1:
        PARAM_LEVEL = ['Beginner', 'Intermediate']
    elif user_predict[0] == 3:
        PARAM_LEVEL = ['Intermediate', 'Expert']
    else:
        PARAM_LEVEL = ['Beginner', 'Intermediate', 'Expert']

    # Antrenman ekipmanlarının belirlenmesi
    if user_feature[0][1] == 1:
        PARAM_EQUIPMENT = ['Cable', 'Body Only', 'None', 'Foam Roll', 'Dumbbell']
    else:
        PARAM_EQUIPMENT = ['Bands', 'Barbell', 'Kettlebells', 'Dumbbell', 'Other', 'Cable', 'Machine', 'Body Only',
                           'Medicine Ball', 'None', 'Exercise Ball', 'Foam Roll', 'E-Z Curl Bar']

    # Antrenman hareket sayısının belirlenmesi
    if user_feature[0][5] == 1:
        PARAM_EXERCISES = 5
    elif user_feature[0][5] == 2:
        PARAM_EXERCISES = 7
    else:
        PARAM_EXERCISES = 10

    # Antrenman tipinin belirlenmesi
    PARAM_TYPE = [prediction_classes[user_predict[0]]]

    print(f'PARAM_LEVEL (exercise-level)= {PARAM_LEVEL}')
    print(f'PARAM_EXERCISES (exercise-number)= {PARAM_EXERCISES}')
    print(f'PARAM_EQUIPMENT (exercise-eq-type)= {PARAM_EQUIPMENT}')
    print(f'PARAM_TYPE (exercise-goal)= {PARAM_TYPE}')

    # Yeni antrenman programı için uygun hareketler getiriliyor
    new_program_data = gym_dataset.loc[ \
        (gym_dataset['Level'].isin(PARAM_LEVEL)) & \
        (gym_dataset['Equipment'].isin(PARAM_EQUIPMENT)) & \
        (gym_dataset['Type'].isin(PARAM_TYPE)) \
        ].sort_values(by=['Type', 'BodyPart']) \
        .copy(deep=True) \
        .reset_index()

    new_program_data.drop(columns=['index'], inplace=True)

    # Yeni antrenmana ait kolon değerleri kontrol ediliyor
    print(f'Level: {new_program_data.Level.unique()} \n')
    print(f'Equipment: {new_program_data.Equipment.unique()} \n')
    print(f'Type: {new_program_data.Type.unique()} \n')
    print(f'Total Number of Workouts: {new_program_data.count()}')

    # Kaç farklı uygun hareket olduğu görüntüleniyor
    new_program_data.groupby('Type').size()
    print("PROGRAM DATA SIZE = ", len(new_program_data.Type))

    # Orantılı dağılım için her zorluk seviyesinden kaç örnek alınacağı belirleniyor
    sampling_num = int(round((PARAM_EXERCISES / len(new_program_data.Level.unique()))))
    print(sampling_num)

    # Eksik kalacak hareket sayısı belirleniyor
    remainder = PARAM_EXERCISES % sampling_num
    print(remainder)

    # Yeni program oluşturuluyor
    new_program = new_program_data.groupby("Level").sample(n=sampling_num, random_state=42).sort_values("Rating")

    # Eksik hareketler programa ekleniyor
    new_program._append(new_program_data.sample(n=remainder, random_state=42))

    while new_program.duplicated().sum() != 0:
        dup_count = new_program.duplicated().sum()
        new_program.drop_duplicates()
        new_program._append(new_program_data.sample(n=dup_count, random_state=42))

    program_json = new_program.to_json(orient="records")

    return program_json

if __name__ == '__main__':
    app.run()