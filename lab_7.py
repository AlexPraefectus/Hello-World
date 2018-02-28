import os.path
import re
import os
import pickle
import shutil
import shelve
import time


countries_dict = {
                'Spain': (505990, 46528966),  # 91
                'Monaco': (2.02, 37550),  # 18589.90
                'Ukraine': (576500, 42456012),  # 73
                'Netherlands': (41526, 17165895),  # 413
}
dictionary = {
              'France': (543965, 67135000),  # 123
              'Belgium': (30528, 11370968),  # 372
              'Italy': (301308, 60525277)  # 201
}


cfg = {'encoding': 'utf-8',
       'path': 'D:\\10.txt',
       'errors': 'ignore',
       'file_1_path': 'D:\\lab7\\1.txt',
       'file_2_path': 'D:\\lab7\\2.txt',
       }


class FileControl:
    def __init__(self, path, mode="r"):
        if mode == "r":
            try:
                self.path = os.path.abspath(path)
                self.file = open(r"{}".format(path), "r", encoding=cfg['encoding'], errors=cfg['errors'])
                self.opened_for_reading_flag = True
                self.text = self.file.read()
            except OSError:
                print(r"Path {} is incorrect".format(path))
                self.opened_for_reading_flag = False
        elif mode == "w":
            try:
                self.path = os.path.abspath(path)
                self.file = open(r"{}".format(path), "w", encoding=cfg['encoding'], errors=cfg['errors'])
                self.opened_for_writing_flag = True
            except OSError:
                print(r"Path {} is incorrect".format(path))
                self.opened_for_writing_flag = False

    def __del__(self):
        self.file.close()

    def write_to_file_w_newline(self, text_to_print):
        if self.opened_for_writing_flag:
            self.file.write(text_to_print)
            self.file.write('\n')

    def get_text(self):
        if self.opened_for_reading_flag:
            return self.text
        else:
            return False


class TextProcessing:
    def __init__(self, text):
        self.processing_text = text
        self.raw_sentences_lst1 = []
        self.raw_sentences_lst2 = []
        self.raw_sentences_lst3 = []

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
                res = re.search('\.\.\.( +[Ї-Я]| +\- [І-Я]|\")', self.processing_text)
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
                    res = re.search('(\w[\?\.!]{1} |\w\[[0-9]\]\.)', k)
                    if not res:
                        self.raw_sentences_lst3.append(k)
                        break
                    else:
                        self.raw_sentences_lst3.append(k[:k.index(res.group(0)) + len(res.group(0))])
                        k = k[k.index(res.group(0)) + len(res.group(0)):]
            except ValueError:
                pass

    def get_processed_text(self):
        self.deleting_control_symbols()
        self.split1_by_3dots()
        self.split2_by_quest_exclam_marks()
        self.split_by_single_marks()
        return self.raw_sentences_lst3

    def get_sentence_with_odd_or_even_length(self, needed='odd'):
        lst = []
        for z in self.get_processed_text():
            if needed == 'odd':
                if sum([len(a) for a in re.findall('[І-є]+',z)])%2 == 1:
                    lst.append(z)
            elif needed == 'even':
                if sum([len(a) for a in re.findall('[І-є]+',z)])%2 == 0:
                    lst.append(z)
            else:
                return 1
        return lst


try:
    os.mkdir('D:\\lab7\\')
    os.mkdir('D:\\lab7\\Korienev\\')
    os.mkdir('D:\\lab5\\')
    os.chdir('D:\\lab7\\')
    with open('data.pickle', 'wb') as f:
        pickle.dump(countries_dict, f)
    shutil.move('data.pickle', 'D:\\lab5\\')
    os.chdir('D:\\lab5\\')
    with open('data.pickle', 'rb') as f:
        data_new = pickle.load(f)
        data_new.update(dictionary)
    with open('new_data_pickle', 'wb') as f:
        pickle.dump(data_new, f)
    os.mkdir('D:\\lab6\\')
    a = shelve.open('D:\\myShelve')
    for i in countries_dict.keys():
        a[i] = countries_dict[i]
    a.close()
    shutil.move('D:\\myShelve.dir', 'D:\\lab6\\')
    shutil.move('D:\\myShelve.dat', 'D:\\lab6\\')
    shutil.move('D:\\myShelve.bak', 'D:\\lab6\\')
    os.rename('D:\\lab6\\myShelve.bak', 'D:\\lab6\\newfile.ext')
    os.utime('D:\\lab6\\newfile.ext', (time.time(), time.time() - 20000))
    os.chmod('D:\\lab6\\newfile.ext', mode=7)
except ValueError:
    print("OSError")


i_file = FileControl(path=cfg['path'], mode='r')
o1_file = FileControl(path=cfg['file_1_path'], mode='w')
o2_file = FileControl(path=cfg['file_2_path'], mode='w')
text_processor = TextProcessing(i_file.get_text())
needed_sentences = text_processor.get_sentence_with_odd_or_even_length(needed='odd')
for i in needed_sentences:
    o1_file.write_to_file_w_newline(i.strip())
for j in i_file.get_text().split():
    if len(re.findall('[аoуiиеяюєїАОУІИЕЯЮЄЇ]', j)) >= 3:
        o2_file.write_to_file_w_newline(j)
