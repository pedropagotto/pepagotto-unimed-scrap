
import datetime
from playwright.sync_api import Playwright, sync_playwright, expect
import os
from dotenv import load_dotenv

def get_report():
    with sync_playwright() as p:
        # Abre o navegador (pode ser 'chromium', 'firefox' ou 'webkit')
        # headless=False permite ver o navegador abrindo e executando as ações
        navegador = p.chromium.launch(headless=False) 
        page = navegador.new_page()
        uri = os.getenv("SITE")
        username = os.getenv("USERNAME")
        password = os.getenv("PASSWORD")
        unimed_unit = os.getenv("UNIMED_UNIT")

        # 1. Abrir o site
        print("Acessando a página de login...")
        page.goto(uri)
        page.wait_for_timeout(1000)
        page.evaluate("() => localStorage.setItem('unimed', '192')")
        page.reload()
        page.wait_for_timeout(1000)
        # page.locator("xpath=//html/body/div[1]/div/section/div/div/div/div[3]/div/div/form/div[1]/div/div/p/div/div[1]/select").select_option(label=unimed_unit)
        page.locator("xpath=//html/body/div[1]/div/section/div/div/div/div[3]/div/div/form/div[2]/div/div/p/input").fill(username)
        page.locator("xpath=//html/body/div[1]/div/section/div/div/div/div[3]/div/div/form/div[3]/div[1]/div/div/p/input").fill(password)
        page.locator("xpath=//html/body/div[1]/div/section/div/div/div/div[3]/div/div/form/div[4]/button").click()
        page.wait_for_timeout(5000)
        page.goto("https://portalempresa.sgusuite.com.br/pem/faturas")
        page.wait_for_timeout(5000)
        page.locator("xpath=//html/body/div[1]/div/div/div/section/div[2]/div/div[3]/div[2]/div/div[1]/table/tbody/tr[1]/td[10]/div/div/div[1]/button").click()   

        page.wait_for_timeout(5000)
        
        # # O Playwright espera a ação que dispara o download (o clique no botão)
        # # e captura o evento de download simultaneamente.
        with page.expect_download() as download_info:
            page.locator("xpath=//html/body/div[1]/div/div/div/section/div[2]/div/div[3]/div[2]/div/div[1]/table/tbody/tr[1]/td[10]/div/div/div[2]/div/div/ul/li[3]").click()
        
        download = download_info.value
        
        # # Define um caminho para salvar o arquivo
        caminho_salvar = f"./downloads/relatorio_{datetime.date.today().strftime('%Y-%m-%d')}.csv"
        download.save_as(caminho_salvar)
        page.wait_for_timeout(5000)
        
        print(f"Download concluído! Arquivo salvo em: {caminho_salvar}")

        navegador.close()
        print("Processo finalizado.")