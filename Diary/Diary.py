import datetime
import os

from loopyCryptor import RSA_encrypt, RSA_decrypt


class Diary:
    def __init__(self, content: str = None, key_path: str = None):
        self.__raw_content = content
        self.__date = str(datetime.date.today()) if content is not None else None

        key = ["diary_key.pri", "diary_key.pub"]
        for i in range(2):
            if key_path is not None and os.path.isfile(os.path.join(key_path, key[i])):
                with open(os.path.join(key_path, key[i]), "r") as f:
                    key[i] = f.read()
            else:
                key[i] = None
        self.__pri_key, self.__pub_key = key

    def read_diary(self, path):
        if os.path.isfile(path):
            with open(path, "rb") as f:
                self.__raw_content = RSA_decrypt(f.read(), self.__pri_key)
                self.__date = os.path.basename(path).split(".")[0]
        else:
            raise FileNotFoundError("`{}` doesn't exist.".format(path))
        return self

    def read_txt(self, path):
        if os.path.isfile(path):
            with open(path, "r") as f:
                self.__raw_content = f.read()
                self.__date = os.path.basename(path).split(".")[0]
        else:
            raise FileNotFoundError("`{}` doesn't exist.".format(path))
        return self

    def to_diary(self):
        if self.__raw_content is None:
            raise ValueError("Diary hasn't been init yet")
        if not os.path.isdir("./diary"):
            os.makedirs("./diary")

        path = "./diary/{}.diary".format(self.__date)
        if not os.path.isfile(path):
            with open(path, "wb") as f:
                f.write(RSA_encrypt(self.__raw_content, self.__pub_key))
        else:
            raise FileExistsError("Diary of {} already exist.".format(self.__date))
        return self

    def to_txt(self):
        if self.__raw_content is None:
            raise ValueError("Diary hasn't been init yet")
        if not os.path.isdir("./unencrypted_diary"):
            os.makedirs("./unencrypted_diary")

        path = "./unencrypted_diary/{}.txt".format(self.__date)
        if not os.path.isfile(path):
            with open(path, "w") as f:
                f.write(self.__raw_content)
        else:
            raise FileExistsError("Diary of {} already exist.".format(self.__date))
        return self

    @staticmethod
    def convert_all(key_path, src_path="./diary"):
        for d in os.listdir(src_path):
            if d[-6:] != ".diary":
                continue
            Diary(key_path=key_path).read_diary(os.path.join(src_path, d)).to_txt()
