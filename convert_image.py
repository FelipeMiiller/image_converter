import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image
import os  # Para manipulação de nomes e caminhos de arquivos

root = None

# Função para verificar o formato das imagens e listar os formatos de conversão disponíveis
def check_image_format(file_paths):
    formats = set()
    for file_path in file_paths:
        try:
            with Image.open(file_path) as img:
                formats.add(img.format)
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao abrir {file_path}: {e}")
            return None
    return formats

# Função de conversão genérica com barra de progresso
def convert_images():
    file_paths = filedialog.askopenfilenames(
        title="Selecione as imagens",
        filetypes=[("Imagens", "*.png *.jpg *.jpeg *.bmp *.webp *.gif"), ("Todos os arquivos", "*.*")]
    )

    if file_paths:
        image_formats = check_image_format(file_paths)
        if not image_formats:
            return

        output_formats = [("JPEG", "*.jpg"), ("PNG", "*.png"), ("BMP", "*.bmp"), ("WEBP", "*.webp")]
        output_format_choice = tk.StringVar()
        
        # Janela para escolha de formato de saída
        format_window = tk.Toplevel(root)
        format_window.title("Escolha o Formato de Saída")
        
        tk.Label(format_window, text="Escolha o formato de saída:").pack(pady=10)

        for fmt, ext in output_formats:
            tk.Radiobutton(format_window, text=fmt, variable=output_format_choice, value=fmt).pack(anchor=tk.W)
        
        def start_conversion():
            if output_format_choice.get():
                format_window.destroy()
                save_images(file_paths, output_format_choice.get())
            else:
                messagebox.showwarning("Aviso", "Por favor, selecione um formato de saída.")
        
        tk.Button(format_window, text="Iniciar Conversão", command=start_conversion).pack(pady=10)

# Função que salva as imagens convertidas com o mesmo nome, mas com nova extensão
def save_images(file_paths, output_format):
    progress_window = tk.Toplevel(root)
    progress_window.title("Convertendo Imagens")
    
    progress_bar = ttk.Progressbar(progress_window, orient="horizontal", length=300, mode="determinate")
    progress_bar.pack(pady=20)
    
    num_files = len(file_paths)
    progress_bar["maximum"] = num_files

    for i, file_path in enumerate(file_paths):
        try:
            with Image.open(file_path) as img:
                # Definir a extensão do arquivo de saída com base no formato escolhido
                ext = output_format.lower()
                
                # Extrair o caminho e nome do arquivo sem extensão
                base_name = os.path.splitext(file_path)[0]
                
                # Criar o caminho de saída com o mesmo nome, mas com nova extensão
                output_file = f"{base_name}.{ext}"
                
                # Salvar a imagem convertida
                img.convert("RGB").save(output_file, output_format)

        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao converter {file_path}: {e}")
            progress_window.destroy()
            return
        
        # Atualizar a barra de progresso
        progress_bar["value"] = i + 1
        root.update_idletasks()

    messagebox.showinfo("Sucesso", "Imagens convertidas com sucesso!")
    progress_window.destroy()

# Configuração da interface gráfica com Tkinter
def create_gui():
    global root
    root = tk.Tk()
    root.title("Conversor de Imagens Genérico")
    
    # Tamanho mínimo da janela
    root.geometry("400x200")

    # Botão para realizar a conversão
    convert_button = tk.Button(root, text="Selecionar e Converter Imagens", command=convert_images)
    convert_button.pack(pady=50)
    
    # Executa a aplicação
    root.mainloop()

# Executa a aplicação gráfica
create_gui()
