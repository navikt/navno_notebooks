# Notatbøker for å analysere strukturert data på `nav.no`

Dette prosjektet inneholder notatbøker for å analysere de strukturerte data-ene
på nav.no.

Formålet med analysene er å vurdere hvordan data-ene kan brukes som en
vektordatabase.

## Komme i gang

Prosjektet bruker [`uv`](https://docs.astral.sh/uv/) og man kan installere
prosjektet, og avhengigheter, med:

```bash
uv sync --frozen
```

> [!IMPORTANT]
> Pass på å aktivere `pre-commit` med `uv run pre-commit install` første gang
> man kloner prosjektet. Dette gir en ekstra sikkerhet for at kodekvalitet blir
> vedlikeholdt mellom forskjellige maskiner, IDE-er og utviklerverktøy.

## Henvendelser
Spørsmål knyttet til koden eller prosjektet kan stilles som issues her på
GitHub.

### For Nav-ansatte

Interne henvendelser kan sendes via Slack i kanalen
[`#team-nks-ai-og-automatisering`](https://nav-it.slack.com/archives/C04MRJ9SHM4)
