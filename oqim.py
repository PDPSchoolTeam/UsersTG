import threading
import time


def thread_function(name, duration):
    for i in range(duration):
        print(f"Oqim {name}: bajarilayotgan iteratsiya {i}")  # noqa
        time.sleep(1)


# oqim - > threading # noqa

# oqim yaratish # noqa
thread1 = threading.Thread(target=thread_function, args=("A", 5))
thread2 = threading.Thread(target=thread_function, args=("B", 5))

# oqimni ishga tushirish # noqa
thread1.start()
thread2.start()

# 2 la oqim tugshini kutadi # noqa
thread1.join()
thread2.join()

print("Ikkala oqim ham bajarilishini tugatdi.")  # noqa
