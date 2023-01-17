# Importando as bibliotecas necessárias
import tkinter as tk
from tkinter import filedialog
import pandas as pd
import numpy as np 
import statsmodels.api as sm
import math

# Criando a classe FileSelector
class FileSelector:
    def __init__(self): # Método construtor
        self.root = tk.Tk()
        self.root.title("Modelo de Previsão de Peso	- Pokémon")
        self.root.geometry("400x300")
        self.root.resizable(False, False)

        self.browse_button = tk.Button(self.root, text="Procurar arquivo", command=self.browse)
        self.browse_button.pack()

        self.analyze_button = tk.Button(self.root, text="Realizar análise", command=self.analyze, state="disable")
        self.analyze_button.pack()

        self.weight_kg_entry = tk.Entry(self.root)
        self.weight_kg_entry.pack()
        self.weight_kg_label = tk.Label(self.root, text="Insira o peso do Pokémon em kg: ")
        self.weight_kg_label.pack()

        self.result_label = tk.Label(self.root, text="")
        self.result_label.pack()

    def browse(self): # Método para procurar o arquivo
        self.filename = filedialog.askopenfilename(initialdir = "/", title = "Select a File", filetypes = (("csv files", "*.csv"), ("all files", "*.*")))
        if self.filename.endswith(".csv"):
            self.df = pd.read_csv(self.filename)
            self.analyze_button.config(state="normal")
        else:
            self.result_label.config(text="Por favor, selecione um arquivo CSV.")
            self.analyze_button.config(state="disable")

    def analyze(self): # Método para realizar a análise
        self.result_label.config(text="Realizando análise...")
        name_type_height_weight_df = self.df[['english_name', 'primary_type', 'height_m', 'weight_kg']]
        grass_pokemon_filtering = np.where((name_type_height_weight_df['primary_type']=='grass'))
        grass_pokemon_df = name_type_height_weight_df.loc[grass_pokemon_filtering]
        weight_kg_grass = grass_pokemon_df['weight_kg'].apply(math.log)
        height_m_grass = grass_pokemon_df['height_m']

        model = sm.OLS(height_m_grass, weight_kg_grass).fit()

        weight_kg = float(self.weight_kg_entry.get())
        predicted_height = model.predict(np.log(weight_kg))
        self.result_label.config(text=f'A previsão de altura para um Pokémon com peso {weight_kg} kg é {predicted_height} m')
