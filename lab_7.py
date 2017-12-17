import os.path
import re


cfg = {'encoding': 'utf-8',
       'path': '10.txt',
       'errors': 'ignore',
       'file_1_path': '1.txt',
       'file_2_path': '2.txt',
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
                    res = re.search('(\w[\?\.!] ?\- \w|\w[\?\.!]{1} |\w\[[0-9]\]. )', k)
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


i_file = FileControl(path=cfg['path'], mode='r')
o1_file = FileControl(path=cfg['file_1_path'], mode='w')
text_processor = TextProcessing(i_file.get_text())
needed_sentences = text_processor.get_sentence_with_odd_or_even_length(needed='odd')
for i in needed_sentences:
    print(i.strip())


"""
if o2_file.opened_for_writing_flag:
    for j in i_file.get_text().split():
        if len(re.findall('[аoуiиеяюєїАОУІИЕЯЮЄЇ]', j)) >= 3:
            o2_file.write_to_file_w_newline(re.search('[І-є]+', j))


c = LabWork7(cfg['path'], cfg['file_1_path'], cfg['file_2_path'])
c.task1()
c.task2()
"""
