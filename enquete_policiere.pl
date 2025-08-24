% -------------------------------
% ENQUÊTE POLICIÈRE - Base de Connaissances
% -------------------------------

% Types de crimes 
crime_type(vol).
crime_type(assassinat).
crime_type(escroquerie).

% Suspects
suspect(john).
suspect(mary).
suspect(alice).
suspect(bruno).
suspect(sophie).
suspect(pierre).

% Faits pour l'enquête
% --- Affaire de VOL ---
has_motive(john, vol).
was_near_crime_scene(john, vol).
has_fingerprint_on_weapon(john, vol).

% --- Affaire d'ASSASSINAT ---
has_motive(mary, assassinat).
was_near_crime_scene(mary, assassinat).
has_fingerprint_on_weapon(mary, assassinat).

has_motive(pierre, assassinat).
was_near_crime_scene(pierre, assassinat).
eyewitness_identification(pierre, assassinat).

% --- Affaire d'ESCROQUERIE ---
has_motive(alice, escroquerie).
has_bank_transaction(alice, escroquerie).

has_bank_transaction(bruno, escroquerie).
owns_fake_identity(sophie, escroquerie).

% --------------------------------------
% RÈGLES MÉTIER
% --------------------------------------

% Règle pour le VOL
is_guilty(Suspect, vol) :-
    suspect(Suspect),
    has_motive(Suspect, vol),
    was_near_crime_scene(Suspect, vol),
    has_fingerprint_on_weapon(Suspect, vol).

% Règle pour l'ASSASSINAT
is_guilty(Suspect, assassinat) :-
    suspect(Suspect),
    has_motive(Suspect, assassinat),
    was_near_crime_scene(Suspect, assassinat),
    ( has_fingerprint_on_weapon(Suspect, assassinat)
    ; eyewitness_identification(Suspect, assassinat)
    ).

% Règle pour l'ESCROQUERIE
is_guilty(Suspect, escroquerie) :-
    suspect(Suspect),
    ( (has_motive(Suspect, escroquerie), has_bank_transaction(Suspect, escroquerie))
    ; has_bank_transaction(Suspect, escroquerie)
    ; owns_fake_identity(Suspect, escroquerie)
    ).

% Règle pour obtenir toutes les preuves d'un suspect pour un crime
get_evidence(Suspect, Crime, Preuve) :-
    (has_motive(Suspect, Crime), Preuve = 'Motif');
    (was_near_crime_scene(Suspect, Crime), Preuve = 'Presence sur lieu');
    (has_fingerprint_on_weapon(Suspect, Crime), Preuve = 'Empreinte arme');
    (eyewitness_identification(Suspect, Crime), Preuve = 'Témoin oculaire');
    (has_bank_transaction(Suspect, Crime), Preuve = 'Transaction bancaire');
    (owns_fake_identity(Suspect, Crime), Preuve = 'Fausse identité').