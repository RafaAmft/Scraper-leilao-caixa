import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

URL = "https://venda-imoveis.caixa.gov.br/sistema/busca-imovel.asp?sltTipoBusca=imoveis"

# Códigos das cidades de SP para teste
CIDADES_SP = {
    "3550308": "SAO PAULO",
    "3509502": "CAMPINAS", 
    "3548708": "SANTOS",
    "3543402": "RIBEIRAO PRETO"
}

def testar_cidades_sp():
    """Testa se os códigos das cidades de SP estão funcionando"""
    
    chrome_options = Options()
    chrome_options.add_argument("--window-size=1920,1080")
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    try:
        print("🚀 Testando cidades de SP...")
        
        # Acessar página inicial
        driver.get(URL)
        print("Acessando página de busca...")
        time.sleep(3)
        
        # Selecionar estado SP
        print("Selecionando estado: SP")
        select_estado = Select(driver.find_element(By.ID, "cmb_estado"))
        select_estado.select_by_value("SP")
        time.sleep(2)
        
        # Testar cada cidade
        for codigo, nome in CIDADES_SP.items():
            try:
                print(f"\n🔍 Testando cidade: {nome} (código: {codigo})")
                
                # Selecionar cidade
                select_cidade = Select(driver.find_element(By.ID, "cmb_cidade"))
                select_cidade.select_by_value(codigo)
                time.sleep(1)
                
                # Verificar se a cidade foi selecionada corretamente
                cidade_selecionada = select_cidade.first_selected_option.text
                print(f"✅ Cidade selecionada: {cidade_selecionada}")
                
                # Verificar se há opções disponíveis
                opcoes_cidade = [opcao.text for opcao in select_cidade.options]
                print(f"📋 Opções disponíveis: {opcoes_cidade}")
                
            except Exception as e:
                print(f"❌ Erro ao testar {nome}: {e}")
        
        # Salvar screenshot
        driver.save_screenshot("teste_sp_cidades.png")
        print("📸 Screenshot salvo: teste_sp_cidades.png")
        
        # Salvar HTML para análise
        with open("teste_sp_cidades.html", 'w', encoding='utf-8') as f:
            f.write(driver.page_source)
        print("📄 HTML salvo: teste_sp_cidades.html")
        
    except Exception as e:
        print(f"❌ Erro durante o teste: {e}")
        
    finally:
        print("Fechando navegador...")
        driver.quit()

if __name__ == "__main__":
    testar_cidades_sp() 