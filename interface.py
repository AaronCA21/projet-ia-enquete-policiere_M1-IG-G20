import tkinter as tk
from tkinter import ttk, messagebox
from pyswip import Prolog

class EnquetePoliciereApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Enquête Policière - M1 IG Groupe 20")
        self.root.geometry("750x550")
        self.root.configure(bg="#f4f6f9")  # Fond général clair

        # Style ttk
        style = ttk.Style()
        style.theme_use("clam")  # Thème moderne
        style.configure("TFrame", background="#f4f6f9")
        style.configure("TLabel", background="#f4f6f9", font=("Arial", 11))
        style.configure("TButton", font=("Arial", 11, "bold"), padding=6)
        style.map("TButton",
                  background=[("active", "#004080")],
                  foreground=[("active", "white")])

        # Initialisation Prolog
        self.prolog = Prolog()
        try:
            self.prolog.consult("enquete_policiere.pl")
        except Exception as e:
            messagebox.showerror("Erreur", f"Impossible de charger le fichier Prolog : {e}")
        
        self.setup_ui()
        
    def setup_ui(self):
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill="both", expand=True)

        # Titre
        title_label = ttk.Label(main_frame, text="ENQUÊTE POLICIÈRE", 
                                font=("Arial", 20, "bold"), foreground="#004080")
        title_label.pack(pady=10)

        # Zone sélection
        select_frame = ttk.Frame(main_frame)
        select_frame.pack(pady=15, fill="x")

        ttk.Label(select_frame, text="Suspect:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.suspect_var = tk.StringVar()
        self.suspect_combo = ttk.Combobox(select_frame, textvariable=self.suspect_var, width=25)
        self.suspect_combo.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(select_frame, text="Type de crime:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.crime_var = tk.StringVar()
        self.crime_combo = ttk.Combobox(select_frame, textvariable=self.crime_var, width=25)
        self.crime_combo.grid(row=1, column=1, padx=5, pady=5)

        # Boutons
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(pady=10)

        ttk.Button(button_frame, text="Vérifier culpabilité",
                   command=self.verifier_culpabilite).grid(row=0, column=0, padx=8)
        ttk.Button(button_frame, text="Enquête complète",
                   command=self.enquete_complete).grid(row=0, column=1, padx=8)
        ttk.Button(button_frame, text="Voir preuves",
                   command=self.voir_preuves).grid(row=0, column=2, padx=8)
        ttk.Button(button_frame, text="Réinitialiser",
                   command=self.reinitialiser).grid(row=0, column=3, padx=8)

        # Cadre résultats
        result_frame = ttk.LabelFrame(main_frame, text="Résultats", padding="10")
        result_frame.pack(fill="both", expand=True, pady=10)

        self.result_text = tk.Text(result_frame, height=15, width=80, wrap=tk.WORD,
                                   font=("Consolas", 11), bg="#ffffff", fg="#222222", relief="flat")
        self.result_text.pack(side="left", fill="both", expand=True)

        scrollbar = ttk.Scrollbar(result_frame, orient="vertical", command=self.result_text.yview)
        scrollbar.pack(side="right", fill="y")
        self.result_text.configure(yscrollcommand=scrollbar.set)

        # Charger données
        self.charger_donnees()

    def charger_donnees(self):
        try:
            suspects = [str(s['X']) for s in self.prolog.query("suspect(X)")]
            self.suspect_combo['values'] = suspects
        except:
            self.suspect_combo['values'] = []
    
        try:
            crimes = [str(c['X']) for c in self.prolog.query("crime_type(X)")]
            self.crime_combo['values'] = crimes
        except:
            self.crime_combo['values'] = []
        
    def verifier_culpabilite(self):
        suspect = self.suspect_var.get()
        crime = self.crime_var.get()
        
        if not suspect or not crime:
            messagebox.showwarning("Attention", "Veuillez sélectionner un suspect et un crime.")
            return
        
        query = f"is_guilty({suspect}, {crime})"
        result = list(self.prolog.query(query))
        
        self.result_text.delete(1.0, tk.END)
        if result:
            self.result_text.insert(tk.END, f"{suspect.upper()} est COUPABLE de {crime} !\n\n")
            self.afficher_preuves(suspect, crime)
        else:
            self.result_text.insert(tk.END, f"{suspect.upper()} est NON COUPABLE de {crime}.\n\n")
            self.result_text.insert(tk.END, "Aucune preuve concluante trouvée.\n")
            
    def afficher_preuves(self, suspect, crime):
        self.result_text.insert(tk.END, "Preuves trouvées:\n")
        preuves = set()
        
        for proof in self.prolog.query(f"get_evidence({suspect}, {crime}, X)"):
            preuves.add(proof['X'])
            
        if not preuves:
            self.result_text.insert(tk.END, "- Aucune preuve disponible.\n")
        else:
            for preuve in preuves:
                self.result_text.insert(tk.END, f"- {preuve}\n")
            
    def enquete_complete(self):
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, "RESULTATS DE L'ENQUETE COMPLETE:\n\n")
    
        coupables_trouves = False

        suspects = [s['X'] for s in self.prolog.query("suspect(X)")]
        crimes = [c['Y'] for c in self.prolog.query("crime_type(Y)")]

        for suspect_nom in suspects:
            for crime_nom in crimes:
                if list(self.prolog.query(f"is_guilty({suspect_nom}, {crime_nom})")):
                    coupables_trouves = True
                    self.result_text.insert(tk.END, f"{suspect_nom.upper()} coupable de {crime_nom}\n")
                    self.afficher_preuves(suspect_nom, crime_nom)
                    self.result_text.insert(tk.END, "\n")
                
        if not coupables_trouves:
            self.result_text.insert(tk.END, "Aucun coupable identifié.\n")

    def voir_preuves(self):
        suspect = self.suspect_var.get()
        
        if not suspect:
            messagebox.showwarning("Attention", "Veuillez sélectionner un suspect.")
            return
        
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, f"PREUVES POUR {suspect.upper()}:\n\n")
        
        preuves_par_crime = {}
        
        for proof in self.prolog.query(f"get_evidence({suspect}, Crime, Preuve)"):
            crime = proof['Crime']
            preuve = proof['Preuve']
            
            if crime not in preuves_par_crime:
                preuves_par_crime[crime] = set()
            preuves_par_crime[crime].add(preuve)
            
        if not preuves_par_crime:
            self.result_text.insert(tk.END, "Aucune preuve disponible.\n")
            return
        
        for crime, preuves in preuves_par_crime.items():
            self.result_text.insert(tk.END, f"{crime.upper()}:\n")
            for preuve in preuves:
                self.result_text.insert(tk.END, f"- {preuve}\n")
            self.result_text.insert(tk.END, "\n")
            
    def reinitialiser(self):
        self.suspect_var.set('')
        self.crime_var.set('')
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, "Nouvelle enquête prête...\n")
        
def main():
    root = tk.Tk()
    app  = EnquetePoliciereApp(root)
    root.mainloop()
    
if __name__ == "__main__":
    main()
