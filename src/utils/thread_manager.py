import threading


def use_other_thread(facturation_handler):

    thread = threading.Thread(target=facturation_handler)
    thread.daemon = True
    return thread.start()
