import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter.messagebox import showinfo
import requests
import shutil

class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("API Client")
        self.geometry("800x600")

        # Adicione a imagem da logo da empresa
        self.logo_image = tk.PhotoImage(file="views/logo.png")
        self.logo_label = tk.Label(self, image=self.logo_image)
        self.logo_label.pack(pady=10)

        # Crie um notebook para alternar entre as abas
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(pady=10)

        # Crie as abas
        self.create_highest_incidence_tab()
        self.create_update_tables_tab()
        self.create_export_results_tab()
        self.create_add_files_tab()

    def create_highest_incidence_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Highest Incidence")

        # Crie uma variável para armazenar a opção selecionada
        self.selected_item = tk.StringVar()
        self.selected_item.set("Buraco")

        # Crie uma lista de opções
        options = ["Buraco", "Remendo", "Trinca", "Placa", "Drenagem"]

        # Crie um Combobox para selecionar a opção
        combo_box = ttk.Combobox(tab, textvariable=self.selected_item, values=options)
        combo_box.pack(pady=10)

        # Crie um botão para chamar a API
        button = ttk.Button(tab, text="Buscar", command=self.get_highest_incidence_km)
        button.pack()

    def create_update_tables_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Update Tables")

        # Crie um botão para chamar a API
        button = ttk.Button(tab, text="Atualizar Tabelas", command=self.update_tables)
        button.pack()

    def create_export_results_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Export Results")

        # Crie uma entrada para inserir o número da highway
        self.highway_entry = ttk.Entry(tab)
        self.highway_entry.pack(pady=10)

        # Crie um botão para chamar a API
        button = ttk.Button(tab, text="Exportar Resultados", command=self.export_results)
        button.pack()

    def create_add_files_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Add Files")

        # Crie um botão para adicionar arquivos
        button = ttk.Button(tab, text="Adicionar Arquivos", command=self.add_files)
        button.pack()

    def get_highest_incidence_km(self):
        item = self.selected_item.get()
        url = f"http://localhost:8888/highest_incidence_km/{item}"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            highest_km = data["highest_km"]
            showinfo("Resultado", f"A maior incidência de {item} ocorre na Km {highest_km}.")
        else:
            showinfo("Erro", f"Não foi possível obter a maior incidência de {item}.")

    def update_tables(self):
        url = "http://localhost:8888/update_tables"
        response = requests.post(url)
        if response.status_code == 200:
            showinfo("Sucesso", "As tabelas foram atualizadas com sucesso.")
        else:
            showinfo("Erro", "Falha ao atualizar as tabelas.")

    def export_results(self):
        highway = self.highway_entry.get()
        url = f"http://localhost:8888/export_results?highway={highway}"
        response = requests.get(url)
        if response.status_code == 200:
            showinfo("Sucesso", f"Resultados da rodovia {highway} exportados para CSV com sucesso.")
        else:
            showinfo("Erro", f"Falha ao exportar resultados da rodovia {highway} para CSV.")

    def add_files(self):
        # Abrir a caixa de diálogo de seleção de arquivo
        filetypes = (("Arquivos CSV", "*.csv"),)
        files = filedialog.askopenfilenames(filetypes=filetypes)

        # Copiar os arquivos selecionados para a pasta "dados"
        for file_path in files:
            file_name = file_path.split("/")[-1]  # Extrai apenas o nome do arquivo
            destination = "dados/" + file_name
            shutil.copy(file_path, destination)

        # Exibir uma mensagem para o usuário
        showinfo("Arquivos Adicionados", "Os arquivos foram adicionados com sucesso.")


if __name__ == "__main__":
    app = Application()
    app.mainloop()