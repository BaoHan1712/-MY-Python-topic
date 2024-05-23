import multiprocessing
import subprocess

def run_file_1():
    subprocess.run(["python", "maindata.py"])

def run_file_2():
    subprocess.run(["python", "main.py"])

if __name__ == "__main__":

    process1 = multiprocessing.Process(target=run_file_1)
    process2 = multiprocessing.Process(target=run_file_2)

    # Bắt đầu
    process1.start()
    process2.start()

    #Chạy 
    process1.join()
    process2.join()