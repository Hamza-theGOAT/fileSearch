import os


def wordLookup(folder, word, matchFiles: list = []):
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


if __name__ == '__main__':
    word = input("Word(s) inside the filename: ")
    folder = "D:\\The Volt"
    check = os.path.exists(folder)
    print(f"Folder Check: {check}\n")
    matchFiles = wordLookup(folder, word)
