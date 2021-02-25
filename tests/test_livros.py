from unittest.mock import patch
from unittest import skip
from colecao.livros import (
    consultar_livros, executar_requisicao
)

from colecao.livros import consultar_livros


@skip("Vale quando consultar livros estiver completo")
def test_consultar_livros_retorna_resultado_formato_string():
    resultado = consultar_livros("Agatha Christie")
    assert type(resultado) == str


@skip
def test_consultar_livros_chama_preparar_dados_para_requisicao_uma_vez_e_com_os_mesmos_parametros_de_consultar_livros():
    with patch("colecao.livros.preparar_dados_para_requisicao") as duble:
        consultar_livros("Agatha Christie")
        duble.assert_called_once_with("Agatha Christie")


@skip
def test_consultar_livros_chama_obter_url_usando_como_parametro_o_retorno_de_preparar_dados_para_requisicao():
    with patch("colecao.livros.preparar_dados_para_requisicao") as duble_preparar:
        dados = {"author": "Agatha Christie"}
        duble_preparar.return_value = dados
        with patch("colecao.livros.obter_url") as duble_obter_url:
            consultar_livros("Agatha Christie")
            duble_obter_url.assert_called_once_with("https://buscador", dados)


@skip
def test_consultar_livros_chama_executar_requisicao_usando_retorno_de_obter_url():
    with patch("colecao.livros.obter_url") as duble_obter_url:
        duble_obter_url.return_value = "https://buscador"
        with patch("colecao.livros.executar_requisicao") as duble_executar_requisicao:
            consultar_livros("Agatha Christie")
            duble_executar_requisicao.assert_called_once_with(
                "https://buscador")


class DubleHTTPResponse:
    def read(self):
        return b""

    def __enter__(self):
        return self


    def __exit__(self, param1, param2, param3):
        pass


def duble_de_urlopen(url, timeout):
    return DubleHTTPResponse()


def test_executar_requisicao_retorna_tipo_string():
    with patch("colecao.livros.urlopen", duble_de_urlopen):
        resultado = executar_requisicao(
            "https://buscarlivros?author=Jk+Rowlings")
        assert type(resultado) == str
