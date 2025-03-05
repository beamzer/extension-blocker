# Bestandsblokkeerder

Deze Windows-applicatie blokkeert het openen van gevaarlijke bestandsextensies (zoals .js) en toont een waarschuwingsvenster in plaats daarvan. Het programma verzamelt informatie over het geblokkeerde bestand en slaat deze op in een lokaal logbestand.

## Installatie

1. Installeer Python 3.8 of hoger (via Anaconda aanbevolen)
2. Installeer de benodigde dependencies:
   ```
   pip install -r requirements.txt
   ```

### Associëren van .js bestanden

Om .js bestanden te associëren met het programma:

1. Open Windows Verkenner
2. Klik met de rechtermuisknop op een .js bestand
3. Kies "Openen met" > "Kies een andere app"
4. Vink "Altijd deze app gebruiken om .js bestanden te openen" aan
5. Klik op "Meer apps" of "Andere opties"
6. Klik op "Zoeken naar een andere app op deze pc"
7. Navigeer naar de locatie van `run_blocker.bat` in de map waar u het programma heeft geïnstalleerd
8. Selecteer `run_blocker.bat`
9. Klik op "Openen"

Als u een andere locatie heeft voor uw Anaconda installatie, pas dan het pad in `run_blocker.bat` aan naar de juiste locatie van uw Python executable.

## Configuratie

Het programma slaat alle geblokkeerde bestanden op in een lokaal logbestand genaamd `file_blocker.log`. Dit bestand wordt aangemaakt in dezelfde map als het programma.

## Functionaliteit

- Blokkeert het openen van .js bestanden
- Toont een waarschuwingsvenster met:
  - Bestandsnaam
  - SHA1 hash van het bestand
  - IP-adres van de computer
  - Tijdstip van de blokkering
- Slaat alle informatie op in een lokaal logbestand
- Sluit automatisch na het sluiten van het waarschuwingsvenster
- Waarschuwingsvenster kan niet worden geminimaliseerd of gemaximaliseerd
- Waarschuwingsvenster blijft altijd bovenop andere vensters

## Logbestand

Alle geblokkeerde bestanden worden gelogd in `file_blocker.log` met de volgende informatie:
- Tijdstip van de blokkering
- Bestandsnaam
- SHA1 hash van het bestand
- IP-adres van de computer

## Testen

Om het programma te testen, kunt u het volgende commando gebruiken:
```
run_blocker.bat "pad\naar\test.js"
```

## Verwijderen van bestandsassociatie

Om de bestandsassociatie te verwijderen, kunt u het Windows Register handmatig aanpassen of de volgende PowerShell-opdracht uitvoeren:

```powershell
Remove-Item -Path "HKCU:\Software\Classes\.js" -Recurse
Remove-Item -Path "HKCU:\Software\Classes\JSFile.Blocker" -Recurse
``` 