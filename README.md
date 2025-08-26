📄 Documentação — script de monitoramento com watchdog 

1. Objetivo 

Monitorar uma pasta específica para registrar eventos de criação, modificação, exclusão e movimentação de arquivos e pastas, salvando as informações em um relatório excel. 
O objetivo principal é saber se o arquivo foi colocado na pasta no dia correto, considerando a data e hora registradas no evento do planejamento de cronograma. 

2. Funcionamento 

O script utiliza a biblioteca watchdog, que observa alterações no sistema de arquivos em tempo real. 

Eventos monitorados: 

Arquivo/pasta criado(a) 

Arquivo/pasta modificado(a) 

Arquivo/pasta deletado(a) 

Arquivo/pasta movido(a) 

 

Formato do relatório EXCEL: 

Data/hora do evento 

Tipo de evento 

Caminho do arquivo/pasta 

3. Limitações 

O watchdog não consegue inspecionar o conteúdo interno de arquivos, como um .Xlsx (excel). 
 Ou seja, ele não mostra quais células ou valores foram alterados — apenas que o arquivo foi modificado em determinado horário. 

Para analisar o conteúdo interno do excel, é necessário utilizar outras bibliotecas como pandas, openpyxl ou xlrd, fazendo a leitura e comparação dos dados antes e depois. 

 

4. Estrutura do código 

Meuhandler: classe que herda de filesystemeventhandler e define o que fazer em cada tipo de evento. 

Registrar_evento: função que grava no CSV a data/hora, tipo de evento e caminho. 

Remove_duplicidades_Excel: função que remove registros duplicados no relatório. 

Observer: observador que monitora a pasta em tempo real. 

 

5. Fluxo geral 

Definir pasta a ser monitorada (XXXX) e onde salvar o relatório (relatório Excel). 

Criar o cabeçalho do .xlsm se ele não existir. 

Iniciar o observe para monitorar a pasta. 

Quando ocorrer um evento, registrar no em relatório Excel. 

Usar a coluna data/hora para validar se o arquivo foi colocado no dia esperado. 
