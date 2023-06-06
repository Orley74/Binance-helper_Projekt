<b><center>Chwaszcz Kacper - Binance-helper_Projekt_PJF </center></b>

Do prawidłowego działania potrzebny klucz API do giełdy kryptowalut Binance,
na potrzeby projektu w kodzie znajduje się mój klucz z uprawnieniami tylko do odczytu danych.


<b> UWAGA </b>
W przypadku wystąpienia błędu dotyczącego różnicy czasowej komutera i servera Binance API należy uruchomić program data_synch
i ponownie włączyć główny kod programu.

<b> Realizowane zadania:</b>
- pozyskiwanie aktualnego stanu konta użytkownika
- wyswietlanie najwększego wzrostu i bilansu użytkownika
- zmiana trybu wyświetlania (ciemny,jasny) 

- Możliwość sortowania rynku pod względem:
  > zmiany procentowej w ostatnich 24 godzinach
  > największej cenie

- Pozyskiwanie aktualnego portfela użytkownika z danymi o wartości, ilości i ceny krypto (dane odświeżane co 10 sekund)

- Przeszukiwanie rynku na podstawie:
  > wzrostu ceny w podanym czasie
 
- Dodatkowo w pliku ML jest prosty model sztucznej inteligencji do predykcji cen
  > działa na modelu sekwencyjnym Tensorflow
  > model musi byc otwierany osobno nie działa on w pełni
