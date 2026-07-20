# log_setup.py

import logging

def setup_logger(name="harness", level=logging.DEBUG): # funszione per creare logger, passo il nome ed il livello del logger
    logger = logging.getLogger(name) # get logger,  singleton, ne esisterà solo uno
    if not logger.handlers:
        logger.setLevel(level) # questa è la soglia globale del logger 
        logger.propagate = False # evito la propagazione di messaggi al root e questo mi evita duplicati 
        
        # Handler terminale
        console = logging.StreamHandler() # creo uno streamhandler
        console.setLevel(logging.INFO) # imposto il livello dello streamhandler, qui vedrò tutti i messaggi di qualsiasi livello
        formatter = logging.Formatter("%(asctime)s,%(levelname)s,%(message)s") # formatto la stringa emanata 
        console.setFormatter(formatter) # aggiungo la formattazione allo stramhandler

        logger.addHandler(console) # aggiungo l'handler 'console' al logger, eseguirò la stessa azione per tutti gli altri handler 

    return logger