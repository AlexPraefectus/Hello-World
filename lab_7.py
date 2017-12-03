import os.path
import re


cfg = {'encoding': 'windows-1251',
       'path': '10.txt',
       'errors': 'ignore',
       'file_1_path': '1.txt',
       'file_2_path': '2.txt',
       }


class FileControl:
    def __init__(self, path):
        try:
            self.path = os.path.abspath(path)
            self.file = open(r"{}".format(path), "r", encoding=cfg['encoding'], errors=cfg['errors'])
            self.opening_flag = True
            self.text = self.file.read()
        except OSError:
            print(r"Path {} is incorrect".format(path))
            self.opening_flag = False

    def __del__(self):
        if self.opening_flag:
            self.file.close()

    def get_text(self):
        if self.opening_flag:
            return self.text
        else:
            return False


class TextProcessing:
    def __init__(self, text):
        self.processing_text = text
        self.raw_sentences_lst1 = []
        self.raw_sentences_lst2 = []
        self.final_sentences_lst = []

    def deleting_control_symbols(self):
        self.processing_text = self.processing_text.replace('\n', ' ')
        self.processing_text = self.processing_text.replace('\r', ' ')
        self.processing_text = self.processing_text.replace('\t', ' ')
        self.processing_text = self.processing_text.replace('\a', '')
        self.processing_text = self.processing_text.replace('\b', '')
        self.processing_text = self.processing_text.replace('\f', '')
        re.sub(r'\s+', ' ', self.processing_text)

    def split1_by_3dots(self):
        try:
            while self.processing_text:
                res = re.search('\.\.\.( +[Ї-Я]| +\- [Ї-Я]|\")', self.processing_text)
                if not res:
                    self.raw_sentences_lst1.append(self.processing_text)
                    break
                else:
                    self.raw_sentences_lst1.append(self.processing_text[:self.processing_text.index(res.group(0))+4])
                    self.processing_text = self.processing_text[self.processing_text.index(res.group(0))+4:]
        except ValueError:
            pass

    def split2_by_quest_exclam_marks(self):
        for j in self.raw_sentences_lst1:
            try:
                while j:
                    res = re.search('\?!', j)
                    if not res:
                        self.raw_sentences_lst2.append(j)
                        break
                    else:
                        self.raw_sentences_lst2.append(j[:j.index(res.group(0)) + 2])
                        j = j[j.index(res.group(0)) + 2:]
            except ValueError:
                pass

    def split_by_single_marks(self):
        for k in self.raw_sentences_lst2:
            try:
                while k:
                    res = re.search('(\w[\?\.!] \- \w|\w[\?\.!]{1} |\w\[[0-9]\]. )', k)
                    if not res:
                        self.final_sentences_lst.append(k)
                        break
                    else:
                        self.final_sentences_lst.append(k[:k.index(res.group(0)) + len(res.group(0))])
                        k = k[k.index(res.group(0)) + len(res.group(0)):]
            except ValueError:
                pass

    def get_processed_text(self):
        self.deleting_control_symbols()
        self.split1_by_3dots()
        self.split2_by_quest_exclam_marks()
        self.split_by_single_marks()
        return self.final_sentences_lst


class LabWork7:
    def __init__(self, encoding, path, errors, file_1_path, file_2_path):
        i_file = FileControl(path=path)
        o1_file = FileControl(path=file_1_path)


a = TextProcessing(FileControl(cfg['path']).get_text()).get_processed_text()
for i in a:
    print(i.strip())
