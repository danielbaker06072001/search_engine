import tkinter
from tkinter import *
from tkinter.ttk import *
import get_index
import search


class Application(Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.create_widgets()
        self.index = False
        self.doc_dict = None
        self.path = None
        self.clean_dict = None
        self.vocab = None
        self.doc_tf = None
        self.doc_df = None 
        self.idf_dict = None
        self.tf_idf_dict = None

    # the GUI has been coded
    def create_widgets(self):
        # set the window title
        self.winfo_toplevel().title("Text Retrieval System")
        # create the GUI lables
        self.l1 = tkinter.Label(self.master, text="A simple App for text retrieval", font=("Arial", 18))
        self.l2 = tkinter.Label(self.master, text="Search Query")
        self.scrollbar = Scrollbar(self.master, orient="vertical")
        self.frame = tkinter.Frame(self.master)
        self.models = [("VSM", 1), ("BM25", 2)]
        self.code = tkinter.IntVar()
        self.code.set(1)
        self.modelCode = 1

        # set the GUI (grid) locations

        self.l1.grid(row=0, column=1, sticky=W)
        self.l2.grid(row=1, column=0)

        # set the entry field
        # the query input
        self.query_text = tkinter.Entry(self.master, width=80)

        # align the entries with the labels
        self.query_text.grid(row=1, column=1, sticky=W)  # left align

        # set the text area for display the result
        self.result = Text(self.master, width=60, yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.result.yview)
        self.scrollbar.grid(row=4, column=2)
        self.result.grid(row=4, column=1, sticky=W)
        # set the GUI style
        self.style = tkinter.ttk.Style()
        # set different conditions
        self.style.map('D.TButton', foreground=[('pressed', 'red'), ('active', 'green')],
                       background=[('pressed', '!disabled', 'black'), ('active', 'white')])
        self.index = tkinter.ttk.Button(self.master, text="Index", style="D.TButton")
        self.index.grid(row=5, column=0, sticky=W)
        # don't add a () to call the function here
        self.index["command"] = self.index_document

        # button to rank the documents given the query
        self.search = Button(self.master, text="Search", style="D.TButton")
        self.search.grid(row=1, column=3, sticky=W)
        self.search["command"] = self.rank_doc
        self.quit = Button(self.master, text="Quit", style="D.TButton", command=self.master.destroy)
        self.quit.grid(row=5, column=2, sticky=E)

        # radio button
        idx = 0
        for model, val in self.models:
            tkinter.Radiobutton(self.master, text=model, padx=20, variable=self.code, value=val, command=self.returnChoice, borderwidth=0).grid(row=6, column=idx)
            idx += 1


    # get the model code from the radio button
    def returnChoice(self):
        # implement here       
        self.modelCode = 1 if self.modelCode == 2 else 2
        return


    # rank the documents by the selected TR model
    def rank_doc(self):
        query = self.query_text.get()
        
        #---------------------------------
        
        #-------------------------------------

        # check if the index tables are build
        if self.index == False:
            self.result.insert(END, "Please index the documnents first. \n")
            return

        # use the VSM ranking
        if self.modelCode == 1:
            # implement here
            term = "\nUsing VSM to rank... Query:" + str(query)+ "\n"
            self.result.insert(END, term)
            outputs = search.rank_by_VSM(query, self.doc_dict, self.tf_idf_dict)
            for i in (outputs):
                text = "document name -- " + str(i) + ", score -- " + str(outputs[i]) +  "\n"
                self.result.insert(END, text)
            self.result.insert(END, "\n")

        # use the BM25 ranking
        if self.modelCode == 2:
            # implement here
            term = "\nUsing BM25 to rank... Query:" + str(query)+ "\n"
            self.result.insert(END, term)
            output = search.rank_by_BM25(query, self.doc_dict, self.doc_tf, self.clean_dict, self.doc_df, self.vocab)
            for i in output:
                text = "document name -- " + str(i) + ", score -- " +  str(output[i]) +  "\n"
                self.result.insert(END, text)
            self.result.insert(END, "\n")


    # Build all the inverted index tables for the ranking function
    # make sure the index tables have the same life cycle as the UI object, i.e. using self.variable to keep them in the memory
    def index_document(self):
        self.result.insert(END, "Inverted index is being built, please wait... \n")
        # implement here
        # first get the path of the folder containing all text documents
        path = get_index.get_folder()

        # Read the doc and turn into dictionary
        doc_dict = get_index.get_docDict(path)
        # As the use of doc_dict, generate vocab, clean_dict as support for generating index_document
        clean_dict = get_index.clean_text(doc_dict)
        vocab = get_index.make_vocab(clean_dict)
        
        doc_tf = get_index.get_DocTF(clean_dict, vocab)
        doc_df = get_index.get_DocDF(clean_dict, vocab)


        N = len(doc_tf.keys())
        idf_dict = get_index.inverse_DF(doc_df, vocab, N)
        
        tf_idf_dict = get_index.get_tf_idf(doc_tf, idf_dict, doc_dict, vocab)

        self.path = path
        self.doc_dict = doc_dict
        self.clean_dict = clean_dict
        self.vocab = vocab
        self.doc_tf = doc_tf
        self.doc_df = doc_df 
        self.tf_idf_dict = tf_idf_dict

        self.result.insert(END, "The document collection has been indexed. \n")
        # switch to True so now we can enter the query to rank
        self.index = True


root = Tk()
root.geometry("800x600")
app = Application(master=root)
app.mainloop()
