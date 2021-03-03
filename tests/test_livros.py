import pytest
from unittest.mock import (
    patch,
    mock_open,
    Mock,
    MagicMock,
)
from unittest import skip
from colecao.livros import (
    consultar_livros,
    executar_requisicao,
    escrever_em_arquivo,
)
from urllib.error import HTTPError


class StubHTTPResponse:
    def read(self):
        return b""

    def __enter__(self):
        return self

    def __exit__(self, param1, param2, param3):
        pass


@patch("colecao.livros.urlopen", return_value=StubHTTPResponse())
def test_consultar_livros_retorna_resultado_formato_string(stub_urlopen):
    resultado = consultar_livros("Agatha Christie")
    assert type(resultado) == str


@patch("colecao.livros.urlopen", return_value=StubHTTPResponse())
def test_consultar_livros_chama_preparar_dados_para_requisicao_uma_vez_e_com_os_mesmos_parametros_de_consultar_livros(stub_urlopen):
    with patch("colecao.livros.preparar_dados_para_requisicao") as spy_preparar_dados:
        consultar_livros("Agatha Christie")
        spy_preparar_dados.assert_called_once_with("Agatha Christie")


@patch("colecao.livros.urlopen", return_value=StubHTTPResponse())
def test_consultar_livros_chama_obter_url_usando_como_parametro_o_retorno_de_preparar_dados_para_requisicao(stub_urlopen):
    with patch("colecao.livros.preparar_dados_para_requisicao") as stub_preparar:
        dados = {"author": "Agatha Christie"}
        stub_preparar.return_value = dados
        with patch("colecao.livros.obter_url") as spy_obter_url:
            consultar_livros("Agatha Christie")
            spy_obter_url.assert_called_once_with("https://buscador", dados)


@patch("colecao.livros.urlopen", return_value=StubHTTPResponse())
def test_consultar_livros_chama_executar_requisicao_usando_retorno_de_obter_url(stub_urlopen):
    with patch("colecao.livros.obter_url") as stub_obter_url:
        stub_obter_url.return_value = "https://buscador"
        with patch("colecao.livros.executar_requisicao") as spy_executar_requisicao:
            consultar_livros("Agatha Christie")
            spy_executar_requisicao.assert_called_once_with("https://buscador")


def stub_de_urlopen(url, timeout):
    return StubHTTPResponse()


def test_executar_requisicao_retorna_tipo_string():
    with patch("colecao.livros.urlopen", stub_de_urlopen):
        print(stub_de_urlopen)
        resultado = executar_requisicao(
            "https://buscarlivros?author=Jk+Rowlings")
        assert type(resultado) == str


"""
def test_executar_requisicao_retorna_resultado_tipo_string_str():
    with patch("colecao.livros.urlopen") as duble_de_urlopen:
        print(duble_de_urlopen)
        duble_de_urlopen.return_value = StubHTTPResponse()
        resultado = executar_requisicao("https://buscarlivros?autor=Jk+Rowlings")
        assert type(resultado) == str

def test_executar_requisicao_retorna_resultado_tipo_str():
    with patch("colecao.livros.urlopen", return_value=StubHTTPResponse()):
        resultado = executar_requisicao("https://buscarlivros?author=Jk+Rowlings")
        assert type(resultado) == str


@patch("colecao.livros.urlopen", return_value=StubHTTPResponse())
def test_executar_requisicao_retorna_resultado_tipo_str(duble_de_urlopen):
    resultado = executar_requisicao("https://buscarlivros?author=Jk+Rowlings")
    assert type(resultado) == str
"""


@patch("colecao.livros.urlopen")
def test_executar_requisicao_retorna_resultado_tipo_str(duble_de_urlopen):
    duble_de_urlopen.return_value = StubHTTPResponse()
    resultado = executar_requisicao("https://buscarlivros?author=Jk+Rowlings")
    assert type(resultado) == str


class Dummy():
    pass


def stub_de_url_open_que_levanta_excessao_http_error(urlopen, timeout):
    fp = mock_open()
    fp.close = Dummy
    raise HTTPError(Dummy(), Dummy(), "mensagem de erro", Dummy(), fp)


"""
def test_executar_requisicao_loga_mensagem_de_erro_de_http_error(caplog):
    with patch("colecao.livros.urlopen", stub_de_url_open_que_levanta_excessao_http_error):
        resultado = executar_requisicao("http://")
        mensagem_de_erro = "mensagem de erro"
        assert len(caplog.records) == 1
        for registro in caplog.records:
            assert mensagem_de_erro in registro.message

   
def executar_requisicao_levanta_excecao_do_tipo_http_error():
    with patch("colecao.livro.urlopen", duble_de_url_open_que_levanta_excessao_http_error):
        with pytest.raises(HTTPError) as excecao:
            executar_requisicao("http://")
        assert "mensagem de erro" in str(excecao.value)


@patch("colecao.livros.urlopen")
def test_executar_requisicao_levanta_excecao_do_tipo_http_error(duble_de_urlopen):
    fp = mock_open
    fp.close = Dummy
    duble_de_urlopen.side_effect = HTTPError(Mock(), Mock(), "mensagem de erro", Mock(), fp)
    with pytest.raises(HTTPError) as excecao:
        executar_requisicao("http://")
        assert "messagem de erro" in str(excecao.value)
"""


@patch("colecao.livros.urlopen")
def test_executar_requisicao_loga_mensagem_de_erro_de_http_error(stub_de_urlopen, caplog):
    fp = mock_open
    fp.close = Dummy
    stub_de_urlopen.side_effect = HTTPError(
        Mock(), Mock(), "mensagem de erro", Mock(), fp)

    executar_requisicao("http://")
    assert len(caplog.records) == 1
    for registro in caplog.records:
        assert "mensagem de erro" in registro.message


class DubleLogging:
    def __init__(self):
        self._mensagens = []

    def exception(self, mensagem):
        self._mensagens.append(mensagem)
    
    @property
    def mensagens(self):
        return self._mensagens


def duble_makedirs(diretorio):
    raise OSError(f"Não foi possível criar diretório {diretorio}")


def test_escrever_em_arquivo_registra_excecao_que_nao_foi_possivel_criar_diretorio():
    arquivo = "/tmp/arquivo"
    conteudo = "dados de livros"
    duble_logging = DubleLogging()
    with patch("colecao.livros.os.makedirs", duble_makedirs):
        with patch("colecao.livros.logging", duble_logging):
            escrever_em_arquivo(arquivo, conteudo)
            assert "Não foi possível criar diretório /tmp" in duble_logging.mensagens


@patch("colecao.livros.os.makedirs")
@patch("colecao.livros.logging.exception")
@patch("colecao.livros.open", side_effect=OSError())
def test_escrever_em_arquivo_registra_erro_ao_criar_o_arquivo(stub_open, spy_exception, stub_makedirs):
    arq = "/bla/arquivo.json"
    escrever_em_arquivo(arq, "dados de livros")
    spy_exception.assert_called_once_with(f"Não foi possível criar arquivo {arq}")
