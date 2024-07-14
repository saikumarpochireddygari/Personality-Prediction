import os
import pandas as pd
import numpy as np
from tkinter import *
from tkinter import filedialog
import tkinter.font as font
from pyresparser import ResumeParser
from sklearn import datasets, linear_model
import spacy

def ensure_spacy_model():
    try:
        nlp = spacy.load('en_core_web_sm')
    except OSError:
        print("Downloading spaCy model...")
        os.system('python -m spacy download en_core_web_sm')
        nlp = spacy.load('en_core_web_sm')
    return nlp

nlp = ensure_spacy_model()

class train_model:
    def train(self):
        data = pd.read_csv('training_dataset.csv')
        array = data.values

        for i in range(len(array)):
            if array[i][0] == "Male":
                array[i][0] = 1
            else:
                array[i][0] = 0

        df = pd.DataFrame(array)

        maindf = df[[0, 1, 2, 3, 4, 5, 6]]
        mainarray = maindf.values

        temp = df[7]
        train_y = temp.values

        self.mul_lr = linear_model.LogisticRegression(multi_class='multinomial', solver='newton-cg', max_iter=1000)
        self.mul_lr.fit(mainarray, train_y)

    def test(self, test_data):
        try:
            test_predict = [int(i) for i in test_data]
            y_pred = self.mul_lr.predict([test_predict])
            return y_pred
        except:
            print("All Factors For Finding Personality Not Entered!")
            return None

def check_type(data):
    if isinstance(data, str):
        return str(data).title()
    if isinstance(data, (list, tuple)):
        return ', '.join(map(str.title, map(str, data)))
    return str(data)

def prediction_result(top, aplcnt_name, cv_path, personality_values):
    top.withdraw()
    applicant_data = {"Candidate Name": aplcnt_name.get(), "CV Location": cv_path}
    age = personality_values[1]

    print("\n############# Candidate Entered Data #############\n")
    print(applicant_data, personality_values)

    personality = model.test(personality_values)
    print("\n############# Predicted Personality #############\n")
    print(personality)

    if not cv_path:
        print("No CV uploaded.")
        return

    try:
        data = ResumeParser(cv_path).get_extracted_data()
    except Exception as e:
        print(f"Error parsing resume: {e}")
        data = {}

    try:
        del data['name']
        if len(data.get('mobile_number', '')) < 10:
            del data['mobile_number']
    except KeyError:
        pass

    print("\n############# Resume Parsed Data #############\n")
    for key, value in data.items():
        if value:
            print(f'{key} : {value}')

    result = Tk()
    result.geometry("{0}x{1}+0+0".format(result.winfo_screenwidth(), result.winfo_screenheight()))
    result.configure(background='White')
    result.title("Predicted Personality")

    titleFont = font.Font(family='Arial', size=40, weight='bold')
    Label(result, text="Result - Personality Prediction", foreground='green', bg='white', font=titleFont, pady=10, anchor=CENTER).pack(fill=BOTH)

    Label(result, text=f"Name: {aplcnt_name.get().title()}", foreground='black', bg='white', anchor='w').pack(fill=BOTH)
    Label(result, text=f"Age: {age}", foreground='black', bg='white', anchor='w').pack(fill=BOTH)
    
    for key, value in data.items():
        if value:
            Label(result, text=f"{check_type(key.title())}: {check_type(value)}", foreground='black', bg='white', anchor='w', width=60).pack(fill=BOTH)
    
    if personality:
        Label(result, text=f"Predicted personality: {personality[0].title()}", foreground='black', bg='white', anchor='w').pack(fill=BOTH)

    Button(result, text="Exit", command=result.destroy).pack()

    terms_mean = """
    # Openness:
    People who like to learn new things and enjoy new experiences usually score high in openness. Openness includes traits like being insightful and imaginative and having a wide variety of interests.

    # Conscientiousness:
    People that have a high degree of conscientiousness are reliable and prompt. Traits include being organised, methodic, and thorough.

    # Extraversion:
    Extraversion traits include being; energetic, talkative, and assertive (sometime seen as outspoken by Introverts). Extraverts get their energy and drive from others, while introverts are self-driven get their drive from within themselves.

    # Agreeableness:
    As it perhaps sounds, these individuals are warm, friendly, compassionate and cooperative and traits include being kind, affectionate, and sympathetic. In contrast, people with lower levels of agreeableness may be more distant.

    # Neuroticism:
    Neuroticism or Emotional Stability relates to degree of negative emotions. People that score high on neuroticism often experience emotional instability and negative emotions. Characteristics typically include being moody and tense.
    """

    Label(result, text=terms_mean, foreground='green', bg='white', anchor='w', justify=LEFT).pack(fill=BOTH)

    result.mainloop()

def predict_person():
    root.withdraw()
    top = Toplevel()
    top.geometry('700x500')
    top.configure(background='black')
    top.title("Apply For A Job")

    titleFont = font.Font(family='Helvetica', size=20, weight='bold')
    Label(top, text="Personality Prediction", foreground='red', bg='black', font=titleFont, pady=10).pack()

    job_list = ('Select Job', '101-Developer at TTC', '102-Chef at Taj', '103-Professor at MIT')
    job = StringVar(top)
    job.set(job_list[0])

    labels = [
        ("Applicant Name", 130), ("Age", 160), ("Gender", 190), ("Upload Resume", 220),
        ("Enjoy New Experience or thing(Openness)", 250),
        ("How Often You Feel Negativity(Neuroticism)", 280),
        ("Wishing to do one's work well and thoroughly(Conscientiousness)", 310),
        ("How much would you like to work with your peers(Agreeableness)", 340),
        ("How outgoing and social interaction you like(Extraversion)", 370)
    ]

    for text, y in labels:
        Label(top, text=text, foreground='white', bg='black').place(x=70, y=y)

    sName = Entry(top)
    sName.place(x=450, y=130, width=160)
    age = Entry(top)
    age.place(x=450, y=160, width=160)
    gender = IntVar()
    Radiobutton(top, text="Male", variable=gender, value=1, padx=7).place(x=450, y=190)
    Radiobutton(top, text="Female", variable=gender, value=0, padx=3).place(x=540, y=190)
    cv_path = StringVar()
    cv_button = Button(top, text="Select File", command=lambda: OpenFile(cv_path, cv_button))
    cv_button.place(x=450, y=220, width=160)

    entries = []
    for y in range(250, 371, 30):
        entry = Entry(top)
        entry.insert(0, '1-10')
        entry.place(x=450, y=y, width=160)
        entries.append(entry)

    submitBtn = Button(top, padx=2, pady=0, text="Submit", bd=0, foreground='white', bg='red', font=(12))
    submitBtn.config(command=lambda: prediction_result(top, sName, cv_path.get(), 
                                                       (gender.get(), age.get()) + tuple(e.get() for e in entries)))
    submitBtn.place(x=350, y=400, width=200)

    top.mainloop()

def OpenFile(cv_path_var, cv_button):
    file_path = filedialog.askopenfilename(
        initialdir="/Users/saikumarreddypochireddygari/Documents/vaishnavinikkiproject/Personality-Prediction-Through-CV/Test_Cases",
        filetypes=(("Document", "*.docx*"), ("PDF", "*.pdf*"), ('All files', '*')),
        title="Choose a file."
    )
    if file_path:
        cv_path_var.set(file_path)
        cv_button.config(text=os.path.basename(file_path))

if __name__ == "__main__":
    model = train_model()
    model.train()

    root = Tk()
    root.geometry('700x500')
    root.configure(background='white')
    root.title("Personality Prediction System")
    titleFont = font.Font(family='Helvetica', size=25, weight='bold')
    homeBtnFont = font.Font(size=12, weight='bold')
    Label(root, text="Personality Prediction System", bg='white', font=titleFont, pady=30).pack()
    Button(root, padx=4, pady=4, width=30, text="Predict Personality", bg='black', foreground='white', bd=1, 
           font=homeBtnFont, command=predict_person).place(relx=0.5, rely=0.5, anchor=CENTER)
    root.mainloop()