import customtkinter as ctk
from tkinter import filedialog
import threading
from PIL import Image
import os
import subprocess
import logging


def safeRun(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logging.error(
                f"Error in {func.__name__}: [{type(e).__name__}] ...")
            logging.error(f"{e}")
    return wrapper


@safeRun
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
            fileElm = fileElm.replace('/', '\\')
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

    @safeRun
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
        self.topFrame.grid_columnconfigure(2, weight=0)

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

        self.searchBox = ctk.CTkEntry(
            self.topFrame,
            placeholder_text="Search Term ...",
            textvariable=None,
            height=40
        )
        self.searchBox.grid(
            row=0, column=1, padx=10, pady=10, sticky="ew"
        )

        self.searchBtn = ctk.CTkButton(
            self.topFrame,
            text="🔍 Search",
            command=self.performSearch,
            height=40,
            width=100
        )
        self.searchBtn.grid(
            row=0, column=2, padx=10, pady=10
        )

        self.searchBox.bind("<Return>", lambda event: self.performSearch())

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

        # A scrollable frame inside
        self.resultsFrame = ctk.CTkScrollableFrame(
            self.resultDisplayFrame,
            fg_color="#1a1d23",
            border_width=0
        )
        self.resultsFrame.pack(fill="both", expand=True, padx=5, pady=5)

    @safeRun
    def browseFolder(self):
        """Open folder dialog to select folder to search files in"""
        folderPath = filedialog.askdirectory(title="Select Folder")

        if folderPath:
            self.currentFolder = folderPath

    @safeRun
    def performSearch(self):
        """Perform search using the current folder and search box text"""
        # Get search term from the search box
        searchTerm = self.searchBox.get().strip()

        # Validate inputs
        if not searchTerm:
            return

        if not self.currentFolder:
            return

        # Perform the search
        matchedFiles = wordLookup(self.currentFolder, searchTerm)

        if matchedFiles:
            self.showResults(matchedFiles)

    @safeRun
    def showResults(self, filePaths):
        # Clear old results first
        for widget in self.resultsFrame.winfo_children():
            widget.destroy()

        # Configure the resultsFrame to expand the itemFrames
        self.resultsFrame.grid_columnconfigure(0, weight=1)

        # Display each file as a rectangular item
        for idx, path in enumerate(filePaths):
            folder = os.path.dirname(path)
            file = os.path.basename(path)

            # Create a new frame for each item (use local variable, not self.itemFrame)
            itemFrame = ctk.CTkFrame(
                self.resultsFrame,
                fg_color="#23272f",
                border_width=1,
                border_color="#23272f",
                corner_radius=6
            )

            # Grid the itemFrame for this iteration
            itemFrame.grid(row=idx, column=0, sticky="ew", padx=4, pady=4)

            # Configure column weights for THIS itemFrame
            itemFrame.grid_columnconfigure(0, weight=0, minsize=200)
            itemFrame.grid_columnconfigure(1, weight=1, minsize=300)
            itemFrame.grid_columnconfigure(2, weight=0, minsize=100)

            # Create filename label for THIS itemFrame
            filenameLabel = ctk.CTkLabel(
                itemFrame,
                text=file,
                anchor="w",
                text_color="white",
                justify="left"
            )
            filenameLabel.grid(row=0, column=0, padx=8, pady=8, sticky="w")

            # Create path label for THIS itemFrame
            pathLabel = ctk.CTkLabel(
                itemFrame,
                text=path,
                anchor="w",
                text_color="white",
                justify="left"
            )
            pathLabel.grid(row=0, column=1, padx=8, pady=8, sticky="ew")

            # Create open button for THIS itemFrame
            openBtn = ctk.CTkButton(
                itemFrame,
                text="Open",
                width=60,
                command=lambda p=folder: self.openInExplorer(p)
            )
            openBtn.grid(row=0, column=2, padx=6, pady=6)

    @safeRun
    def openInExplorer(self, path):
        if os.path.isfile(path):
            print(f"Opening File: {path}")
            subprocess.run(["explorer", "/select", path])
        elif os.path.isdir(path):
            print(f"Opening Folder: {path}")
            subprocess.run(["explorer", path])

    def run(self):
        """Start the GUI application"""
        self.root.mainloop()


@safeRun
def main():
    word = input("Word(s) inside the filename: ")
    folder = "D:\\The Volt"
    check = os.path.exists(folder)
    print(f"Folder Check: {check}\n")
    matchFiles = wordLookup(folder, word)


if __name__ == '__main__':
    app = fileLookup()
    app.run()
