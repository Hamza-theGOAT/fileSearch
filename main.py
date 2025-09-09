import customtkinter as ctk
from tkinter import filedialog
import threading
from PIL import Image
import os


def wordLookup(folder: os.path, word: str, matchFiles: list = []):
    folderElms = []
    fileElms = []
    for subElm in os.listdir(folder):
        subElmPath = os.path.join(folder, subElm)
        if os.path.isfile(subElmPath):
            # print(f"Files in {folder}:{subElmPath}")
            fileElms.append(subElmPath)
        elif os.path.isdir(subElmPath):
            folderElms.append(subElmPath)
            # print(f"Folders in {folder}:{subElmPath}")
        else:
            print(f"Invalid entries in {folder}:\n{subElmPath}")
            continue

    for fileElm in fileElms:
        if word in os.path.basename(fileElm) and fileElm not in matchFiles:
            matchFiles.append(fileElm)
            print(f"Found <{word}> at [{fileElm}]")
        continue

    for folderElm in folderElms:
        matchFiles = wordLookup(folderElm, word)

    return matchFiles


ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")


class fileLookup:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("File Search")
        self.root.geometry("1000x700")

        # Main frame creation
        self.mainSection()

    def mainSection(self):
        self.mainFrame = ctk.CTkFrame(
            self.root,
            fg_color="#1a1d23",
            border_width=3,
            border_color="#3a3f4b"
        )
        self.mainFrame.pack(fill="both", expand=True, padx=10, pady=10)
        self.mainFrame.grid_rowconfigure(0, weight=1)
        self.mainFrame.grid_rowconfigure(1, weight=9)
        self.mainFrame.grid_columnconfigure(0, weight=1)

        self.topSection()
        self.resultDisplaySection()

    def topSection(self):
        self.topFrame = ctk.CTkFrame(
            self.mainFrame,
            fg_color="#23272f",
            border_width=2,
            border_color="#444b57"
        )
        self.topFrame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        self.topFrame.grid_rowconfigure(0, weight=1)
        self.topFrame.grid_columnconfigure(0, weight=0)
        self.topFrame.grid_columnconfigure(1, weight=1)

        self.browseBtn = ctk.CTkButton(
            self.topFrame,
            text="📁 Browse Folder",
            command=self.browseFolder,
            height=40,
            width=150
        )
        self.browseBtn.grid(
            row=0, column=0, padx=10, pady=10
        )

    def browseFolder(self):
        """Open folder dialog to select folder to search files in"""
        folderPath = filedialog.askdirectory(title="Select Folder")

        if folderPath:
            self.currentFolder = folderPath
            self.matchedFiles = wordLookup(
                self.currentFolder,
                'inv_rec'
            )

    def resultDisplaySection(self):
        """Main body to display results from search"""
        self.resultDisplayFrame = ctk.CTkFrame(
            self.mainFrame,
            fg_color="#1a1d23",
            border_width=2,
            border_color="#3a3f4b"
        )
        self.resultDisplayFrame.grid(
            row=1, column=0, sticky="nsew", padx=10, pady=10)

    def run(self):
        """Start the GUI application"""
        self.root.mainloop()


def main():
    word = input("Word(s) inside the filename: ")
    folder = "D:\\The Volt"
    check = os.path.exists(folder)
    print(f"Folder Check: {check}\n")
    matchFiles = wordLookup(folder, word)


if __name__ == '__main__':
    app = fileLookup()
    app.run()
