Получает данные со всех вакансий hh.ru и формирует выходящий json файл.
На вход принимает параметры из CLI, такие как кол-во страниц, ссылку, ключевое слово:
    С кол-вом страниц и файлом все понятно, а вот по поводу ссылки:
        Она должна быть с применением всех необходимых фильтров и указана на
        основную страницу поиска!
      
usage: main.py [-h] [-l LINK] [-p PAGES] [-k KEYWORD] [-f FILE]
optional arguments:
  -h, --help            show this help message and exit
  
  -l LINK, --link LINK  Paste start link on the vacancies search
  
  -p PAGES, --pages PAGES
                        Write count of examined pages
  
  -k KEYWORD, --keyword KEYWORD
                        Keyword
  
  -f FILE, --file FILE  Path to result file
    
    
 
