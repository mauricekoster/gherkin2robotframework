# language: nl
@Hallo
Functionaliteit: Voorbeelden

  Als een tester
  Wil ik Gherkin bestanden specificeren en deze vertalen naar RobotFramework bestanden
  Zodat ik het beste van beide kan gebruiken

  Achtergrond: Achtergrond informatie
    Gegeven enkele achtergrond dingen

  Voorbeeld: Groeten

    Dit is een simpele test met een eenvoudige groeter

    Gegeven een groeter
    Wanneer deze personen worden gegroet:
      | Naam  | Groet      |
      | Joe   | Hallo      |
      | Mary  | He, daar!  |
    Dan wordt de wereld een stukje beter

  Scenario: Niet zo'n leuk persoon
    Gegeven een minder leuk persoon
    Wanneer deze personen worden gegroet:
      | Naam  | Groet        |
      | Peter | Hallo, daar! |
    Dan wordt de wereld iets minder leuk

  Abstract Scenario: Saai spul
    Een omschrijving
    over meerdere regels

    Gegeven een rekensom <a> + <b>
    Wanneer dit is uitgerekend
    Dan is het antwoord: <c>

    Voorbeelden: A
      Documentatie voor sommen A
      | a  | b | c |
      | 1  | 1 | 2 |
      | 2  | 2 | 4 |
      | 1  | 2 | 3 |
      
