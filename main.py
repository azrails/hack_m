import parser
import os, os.path
import tkinter as tk

class MainApp(tk.Tk):
    def __init__(self) ->None:
        super().__init__()
        self.geometry('{}x{}+{}+{}'.format(round(self.winfo_screenwidth() / 1.5), round(self.winfo_screenheight() / 1.5), (self.winfo_screenwidth()-self.winfo_screenwidth()//2)// 2, (self.winfo_screenheight()-self.winfo_screenheight() // 2)// 2))
        self.title('Рассчет службы дорожного покрытия')
        self.frame = tk.Frame()
        self.btn_chose_directory = tk.Button(text='Chose directory', width=30, height=15, master=self.frame).grid(row=0, column=0, padx=10, pady=10)
        self.frame.pack()
        

def main():
    app = MainApp()
    app.mainloop()
                

if __name__=='__main__':
    main()