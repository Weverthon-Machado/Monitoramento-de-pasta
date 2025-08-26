import os
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from datetime import datetime, timedelta
import pandas as pd

# Caminho da pasta a ser monitorada
path_para_monitorar = r'C:\Users\weverthon.machado\Dataprev\DIME - Documentos'

# Pastas para salvar os arquivos
pasta_base = r'C:\Users\weverthon.machado\OneDrive - Dataprev\Área de Trabalho\Teste Py\Base_Dados'
pasta_relatorios = r'C:\Users\weverthon.machado\OneDrive - Dataprev\Área de Trabalho\Teste Py\Relatorios'

# Garante que as pastas existam
os.makedirs(pasta_base, exist_ok=True)
os.makedirs(pasta_relatorios, exist_ok=True)

# Caminho da base histórica
arquivo_base = os.path.join(pasta_base, "base_monitoramento.xlsx")

# Garante que a base histórica exista
if not os.path.exists(arquivo_base):
    pd.DataFrame(columns=['Data', 'Hora', 'Evento', 'Caminho']).to_excel(arquivo_base, index=False)

def gerar_relatorios():
    """Gera relatórios diário, semanal e mensal a partir da base histórica."""
    if os.path.exists(arquivo_base):
        df = pd.read_excel(arquivo_base)

        # Converte a coluna Data para formato datetime
        df['Data'] = pd.to_datetime(df['Data'], format='%Y-%m-%d')

        hoje = datetime.now().date()
        inicio_semana = hoje - timedelta(days=7)
        inicio_mes = hoje.replace(day=1)

        # Filtra diário
        df_diario = df[df['Data'] == hoje]
        relatorio_diario = os.path.join(pasta_relatorios, f"relatorio_diario_{hoje}.xlsx")
        df_diario.to_excel(relatorio_diario, index=False)

        # Filtra semanal
        df_semanal = df[(df['Data'] >= inicio_semana) & (df['Data'] <= hoje)]
        relatorio_semanal = os.path.join(pasta_relatorios, f"relatorio_semanal_{inicio_semana}_a_{hoje}.xlsx")
        df_semanal.to_excel(relatorio_semanal, index=False)

        # Filtra mensal
        df_mensal = df[(df['Data'] >= inicio_mes) & (df['Data'] <= hoje)]
        relatorio_mensal = os.path.join(pasta_relatorios, f"relatorio_mensal_{inicio_mes.strftime('%Y-%m')}.xlsx")
        df_mensal.to_excel(relatorio_mensal, index=False)

        print(f"📄 Relatórios gerados:\n  Diário: {relatorio_diario}\n  Semanal: {relatorio_semanal}\n  Mensal: {relatorio_mensal}")

def registrar_evento(evento, caminho):
    """Adiciona evento na base e atualiza relatórios."""
    agora = datetime.now()
    registro = {
        'Data': agora.strftime('%Y-%m-%d'),
        'Hora': agora.strftime('%H:%M:%S'),
        'Evento': evento,
        'Caminho': caminho
    }

    # Atualiza base
    df_base = pd.read_excel(arquivo_base)
    df_base = pd.concat([df_base, pd.DataFrame([registro])], ignore_index=True)
    df_base.drop_duplicates(inplace=True)
    df_base.to_excel(arquivo_base, index=False)

    # Atualiza relatórios
    gerar_relatorios()

class MeuHandler(FileSystemEventHandler):
    def on_created(self, event):
        tipo = "Pasta criada" if event.is_directory else "Arquivo criado"
        registrar_evento(tipo, event.src_path)

    def on_deleted(self, event):
        tipo = "Pasta deletada" if event.is_directory else "Arquivo deletado"
        registrar_evento(tipo, event.src_path)

    def on_modified(self, event):
        tipo = "Pasta modificada" if event.is_directory else "Arquivo modificado"
        registrar_evento(tipo, event.src_path)

    def on_moved(self, event):
        tipo = "Pasta movida" if event.is_directory else "Arquivo movido"
        registrar_evento(tipo, f'{event.src_path} -> {event.dest_path}')

if __name__ == "__main__":
    event_handler = MeuHandler()
    observer = Observer()
    observer.schedule(event_handler, path=path_para_monitorar, recursive=True)
    observer.start()

    print(f"📂 Monitorando alterações em: {path_para_monitorar}")
    print(f"📊 Base histórica: {arquivo_base}")
    print(f"📁 Relatórios serão salvos em: {pasta_relatorios}")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n🛑 Monitoramento encerrado.")
        observer.stop()
    observer.join()
